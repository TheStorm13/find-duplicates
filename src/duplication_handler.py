import logging
import os
from collections import defaultdict

from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


class DuplicationHandler:
    @staticmethod
    def are_hashes_equal(hash_1, hash_2):
        return hash_1 == hash_2
        # return (hash_1 - hash_2)<10

    def create_duplicate_dir(self, base_directory):
        """
        Создаёт папку для дубликатов, если она ещё не существует.
        """
        duplicate_dir = os.path.join(base_directory, "Duplicate")
        os.makedirs(duplicate_dir, exist_ok=True)
        return duplicate_dir

    def move_file(self, src_path, dst_dir):
        """
        Перемещает файл из src_path в указанную директорию.
        """
        try:
            filename = os.path.basename(src_path)
            dst_path = os.path.join(dst_dir, filename)
            os.replace(src_path, dst_path)
        except Exception as e:
            logging.error(f"Ошибка при перемещении файла {src_path} в {dst_dir}: {e}")

    def find_duplicates(self, image_hashes, image_paths):
        """
        Поиск дубликатов на основе хэшей изображений.
        Возвращает словарь с ключами (хэши) и путями дубликатов.
        """
        duplicates = defaultdict(list)
        for idx, image_hash in enumerate(image_hashes):
            duplicates[image_hash].append(image_paths[idx])
        return {h: p for h, p in duplicates.items() if len(p) > 1}

    def remove_duplicate_images_by_hash(self, directory, image_paths, image_hashes, count_images):
        duplicate_dir = self.create_duplicate_dir(directory)
        duplicates_count = 0

        # Найти дубликаты
        duplicates = self.find_duplicates(image_hashes, image_paths)

        # Обработка дубликатов
        for hash_value, paths in duplicates.items():
            # Сохраняем только первое изображение, остальные перемещаем
            for duplicate_path in paths[1:]:
                self.move_file(duplicate_path, duplicate_dir)
                duplicates_count += 1

        return duplicates_count
