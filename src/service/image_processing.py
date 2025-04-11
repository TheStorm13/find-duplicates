import logging
from concurrent.futures import ThreadPoolExecutor

import click
import imagehash
from PIL import Image
from PIL import ImageFile

from src.utils import get_optimized_thread_count

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageProcessing:

    def calculate_image_hash(self, image_path):
        try:
            with Image.open(image_path) as image:
                image.draft('L', (32, 32))
                return image_path, imagehash.dhash(image)
        except Exception as e:
            logging.error("Ошибка обработки изображения '%s': %s", image_path, e)
            return image_path, None

    def calculate_hashes_single_thread(self, image_paths: list[str]) -> dict[str, imagehash.ImageHash]:
        """
         Синхронная обработка изображений.
         Возвращает словарь, где ключ — путь к изображению, а значение — вычисленный хэш.

         :param image_paths: Список путей к изображениям
         :return: Словарь {путь_к_изображению: хэш}
         """

        logging.info(f"Начато вычисление хэшей")

        # Прогрессбар для отображения статуса обработки
        with click.progressbar(image_paths, length=len(image_paths), show_eta=True,
                               label='Обработка изображений') as bar:
            hash_images = []
            for image_path in bar:
                result = self.calculate_image_hash(image_path)
                hash_images.append(result)

        # Формирование словаря из успешных результатов
        return {path: hash_value for path, hash_value in hash_images if hash_value is not None}

    def calculate_hashes_multithreaded(self, image_paths: list[str]) -> dict[str, imagehash.ImageHash]:
        """
        Синхронная обработка изображений.
        Возвращает словарь, где ключ — путь к изображению, а значение — вычисленный хэш.

        :param image_paths: Список путей к изображениям
        :return: Словарь {путь_к_изображению: хэш}
        """

        logging.info(f"Начато вычисление хэшей")

        # Оптимальное количество потоков
        max_workers = get_optimized_thread_count()

        with click.progressbar(image_paths, length=len(image_paths), show_eta=True,
                               label='Обработка изображений') as bar:
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                hash_images = []
                for result in pool.map(self.calculate_image_hash, image_paths):
                    hash_images.append(result)
                    bar.update(1)

        # Формирование словаря из успешных результатов
        return {path: hash_value for path, hash_value in hash_images if hash_value is not None}
