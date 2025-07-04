import logging
from collections import defaultdict
from pathlib import Path

import imagehash
from PIL import ImageFile

from core.model.image_data import ImageData

ImageFile.LOAD_TRUNCATED_IMAGES = True


class DuplicationHandler:
    @staticmethod
    def are_hashes_equal(hash_1: imagehash.ImageHash, hash_2: imagehash.ImageHash) -> bool:
        # todo: не используется. Как работает тогда обработка совпадений?
        """
        Проверяет, равны ли два хэша изображений.

        :param hash_1: Первый хэш.
        :param hash_2: Второй хэш.
        :return: True, если хэши равны, иначе False.
        """
        result = hash_1 == hash_2
        logging.debug(f"Сравнение хэшей: {hash_1} и {hash_2} - Результат: {result}")
        return result
        # return (hash_1 - hash_2)<10

    def find_duplicates(self, images: list[ImageData]) -> list[Path]:
        """
        Поиск дубликатов на основе хэшей изображений.

        :param image_hashes: Словарь с путями к изображениям и их хэшами.
        :return: Список путей к дубликатам (без первого оригинального пути для каждой группы).
        """
        # Группируем пути по значениям хэшей
        duplicates = defaultdict(list)

        for image in images:
            duplicates[image.hash].append(image.image_path)
            logging.debug(f"Добавление пути {image.image_path} для хэша {image.hash}")

        # Возвращаем все пути, кроме первых (оригиналов)
        duplicate_paths = []
        for paths in duplicates.values():
            if len(paths) > 1:
                duplicate_paths.extend(paths[1:])  # Добавляем дубликаты (без первого пути)
                logging.debug(f"Найдены дубликаты: {paths[1:]}")
        print(duplicate_paths)
        logging.info(f"Обнаружено {len(duplicate_paths)} дубликатов")
        return duplicate_paths
