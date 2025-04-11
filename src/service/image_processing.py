import asyncio
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

    def process_images(self, image_paths: list[str]) -> dict[str, imagehash.ImageHash]:
        """
        Синхронная обработка изображений.
        Возвращает словарь, где ключ — путь к изображению, а значение — вычисленный хэш.

        :param image_paths: Список путей к изображениям
        :return: Словарь {путь_к_изображению: хэш}
        """

        logging.info(f"Начато вычисление хэшей для {len(image_paths)} изображений")

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

    async def process_images_async(self, image_paths: list[str]) -> dict[str, imagehash.ImageHash]:

        """
        Асинхронная обработка изображений с вычислением хэшей.
        Возвращает словарь {путь к изображению: хэш}, исключая неуспешно обработанные.

        :param image_paths: список путей к изображениям
        :return: словарь {путь_к_изображению: хэш}
        """
        logging.info(f"Начато вычисление хэшей для {len(image_paths)} изображений")

        # Оптимальное количество потоков
        max_workers = get_optimized_thread_count()

        # Асинхронная обработка изображений с помощью пула потоков
        async def handle_image_in_pool(image_path):
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(pool, self.calculate_image_hash, image_path)

        # Создание пула потоков
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            # Обработка изображений и сбор результатов
            tasks = [handle_image_in_pool(path) for path in image_paths]
            results = await asyncio.gather(*tasks)

        # Фильтр успешных хэшей
        return {path: hash_value for path, hash_value in results if hash_value is not None}
