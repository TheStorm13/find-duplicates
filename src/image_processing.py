import logging
import multiprocessing as mp
import os
from concurrent.futures import ThreadPoolExecutor

import imagehash
from PIL import Image
from PIL import ImageFile

from config import DUPLICATE_FOLDER, IMAGE_EXTENSIONS

ImageFile.LOAD_TRUNCATED_IMAGES = True


# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler(LOG_FILE_PATH, mode='w'),
#         logging.StreamHandler()
#     ]
# )


class ImageProcessing:

    def input_directory(self):
        directory = input()
        if os.path.isdir(directory) or directory == '':
            logging.info(f"Директория подтверждена: {directory}")
            return directory
        else:
            logging.error(f"Такой папки не существует: {directory}")
            self.input_directory()

    @staticmethod
    def calculate_image_hash(filename):
        try:
            with Image.open(filename) as image:
                image.draft('L', (32, 32))
                return imagehash.dhash(image)
        except Exception as e:
            logging.error(f"Ошибка при обработке изображения {filename}: {e}")
            return None

    def load_directory(self):
        path_images = []
        hash_images = []

        directory = self.input_directory()
        if not directory:
            return directory, hash_images

        for root, dirs, files in os.walk(directory):

            if os.path.basename(root) == DUPLICATE_FOLDER:
                continue
            for file in files:
                if file.lower().endswith(tuple(IMAGE_EXTENSIONS)):
                    path_images.append(os.path.join(root, file))

        count_image = len(path_images)
        print(f"Найдено фотографий: {count_image}")
        logging.info(f"Найдено изображений: {count_image}")

        if count_image == 0:
            return directory, path_images, hash_images

        with ThreadPoolExecutor(max_workers=mp.cpu_count() + 4) as pool:
            for hash_image in pool.map(self.calculate_image_hash, path_images):
                hash_images.append(hash_image)

            # hash_images.extend(pool.map(putHash, path_images))

        return directory, path_images, hash_images
