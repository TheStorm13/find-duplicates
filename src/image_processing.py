import logging
import os
from concurrent.futures import ThreadPoolExecutor

import imagehash
from PIL import Image
from PIL import ImageFile

from config import DUPLICATE_FOLDER, IMAGE_EXTENSIONS
from src.utils import get_optimized_thread_count

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageProcessing:

    def input_directory(self):
        directory = input()
        if os.path.isdir(directory) or directory == '':
            logging.info(f"Директория подтверждена: {directory}")
            return directory
        else:
            logging.error(f"Такой папки не существует: {directory}")
            print("Попробуйте снова.")
            self.input_directory()

    def collect_images(self, directory):
        for root, dirs, files in os.walk(directory):
            if os.path.basename(root) == DUPLICATE_FOLDER:
                continue
            for file in files:
                if file.lower().endswith(tuple(IMAGE_EXTENSIONS)):
                    yield os.path.join(root, file)

    @staticmethod
    def calculate_image_hash(filename):
        try:
            with Image.open(filename) as image:
                image.draft('L', (32, 32))
                return imagehash.dhash(image)
        except Exception as e:
            logging.error(f"Ошибка при обработке изображения {filename}: {e}")
            return None

    def process_images(self, path_images):
        #todo: сделать асинхронную обработку
        logging.info(f"Начато вычисление хэшей для {len(path_images)} изображений")
        with ThreadPoolExecutor(max_workers=get_optimized_thread_count()) as pool:
            hash_images = list(pool.map(self.calculate_image_hash, path_images))
        return [h for h in hash_images if h is not None]

    def load_directory(self):
        directory = self.input_directory()
        if not directory:
            return directory, [], []

        path_images = list(self.collect_images(directory))
        if not path_images:
            logging.info("Нет изображений для обработки.")
            return directory, [], []

        hash_images = self.process_images(path_images)
        return directory, path_images, hash_images
