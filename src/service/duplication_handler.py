import logging
from collections import defaultdict

import imagehash
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


class DuplicationHandler:
    @staticmethod
    def are_hashes_equal(hash_1: imagehash.ImageHash, hash_2: imagehash.ImageHash) -> bool:
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



    def find_duplicates(self, image_hashes: dict[str, imagehash.ImageHash]) -> list[str]:
        """
        Поиск дубликатов на основе хэшей изображений.

        :param image_hashes: Словарь с путями к изображениям и их хэшами.
        :return: Список путей к дубликатам (без первого оригинального пути для каждой группы).
        """
        # Группируем пути по значениям хэшей
        duplicates = defaultdict(list)
        for image_path, image_hash in image_hashes.items():
            duplicates[image_hash].append(image_path)
            logging.debug(f"Добавление пути {image_path} для хэша {image_hash}")

        # Возвращаем все пути, кроме первых (оригиналов)
        duplicate_paths = []
        for paths in duplicates.values():
            if len(paths) > 1:
                duplicate_paths.extend(paths[1:])  # Добавляем дубликаты (без первого пути)
                logging.debug(f"Найдены дубликаты: {paths[1:]}")

        logging.info(f"Обнаружено {len(duplicate_paths)} дубликатов")
        return duplicate_paths

