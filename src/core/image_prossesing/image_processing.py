import dataclasses
import logging
from concurrent.futures import ThreadPoolExecutor

import click
import imagehash
from PIL import Image
from PIL import ImageFile

from core.model.image_data import ImageData
from utils import get_optimized_thread_count

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageProcessing:

    def calculate_image_hash(self, image: ImageData) -> ImageData:
        try:
            with Image.open(image.image_path) as image_file:
                image_file.draft('L', (32, 32))
                return dataclasses.replace(image, hash=imagehash.dhash(image_file))
        except Exception as e:
            logging.error("Ошибка при вычисления хеша '%s': %s", image.image_path, e)
            return None

    def calculate_hashes_single_thread(self, images: list[ImageData]) -> list[ImageData]:
        """
         Синхронная обработка изображений.
         Возвращает словарь, где ключ — путь к изображению, а значение — вычисленный хэш.

         :param image_paths: Список путей к изображениям
         :return: Словарь {путь_к_изображению: хэш}
         """

        logging.info(f"Начато вычисление хэшей")

        # Прогрессбар для отображения статуса обработки
        with click.progressbar(images, length=len(images), show_eta=True,
                               label='Обработка изображений') as bar:
            images_with_hash = []
            for image in bar:
                result = self.calculate_image_hash(image)
                images_with_hash.append(result)

        return images_with_hash

    def calculate_hashes_multithreaded(self, images: list[ImageData]) -> list[ImageData]:
        """
        Синхронная обработка изображений.
        Возвращает словарь, где ключ — путь к изображению, а значение — вычисленный хэш.

        :param images: Список путей к изображениям
        :return: Словарь {путь_к_изображению: хэш}
        """

        logging.info(f"Начато вычисление хэшей")

        # Оптимальное количество потоков
        max_workers = get_optimized_thread_count()

        with click.progressbar(images, length=len(images), show_eta=True,
                               label='Обработка изображений') as bar:
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                images_with_hash = []
                for result in pool.map(self.calculate_image_hash, images):
                    images_with_hash.append(result)
                    bar.update(1)

        return images_with_hash
