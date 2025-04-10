import multiprocessing as mp
import os
from concurrent.futures import ThreadPoolExecutor

import imagehash
from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageProcessing:

    def input_directory(self):
        directory = input()
        if os.path.isdir(directory) or directory == '':
            return directory
        else:
            print("Такой папки не существует. Попробуйте ввести еще раз или нажмите Enter, чтобы завершить программу.")
            self.input_directory()

    @staticmethod
    def calculate_image_hash(filename):
        try:
            with Image.open(filename) as image:
                image.draft('L', (32, 32))
                return imagehash.dhash(image)
        except Exception as e:
            print(f"Ошибка при обработке изображения {filename}: {e}")
            return None

    def load_directory(self):
        path_images = []
        hash_images = []
        directory = self.input_directory()
        if directory == '' or directory == None:
            return directory, hash_images

        for root, dirs, files in os.walk(directory):
            for file in files:
                if root != directory + r"\Duplicate" and file[-4:].lower() in (".jpg", "jpeg", ".png"):
                    path_images.append(root + '\\' + file)

        count_image = len(path_images)
        print(f"Найдено фотографий: {count_image}")
        if count_image == 0:
            return directory, path_images, hash_images

        with ThreadPoolExecutor(max_workers=mp.cpu_count() + 4) as pool:
            for hash_image in pool.map(self.calculate_image_hash, path_images):
                hash_images.append(hash_image)

            # hash_images.extend(pool.map(putHash, path_images))

        return directory, path_images, hash_images
