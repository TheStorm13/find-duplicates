import os
import time
import multiprocessing as mp
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor
import imagehash
from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageProcessing:

    def inputDirectory(self):
        directory = input()
        if os.path.isdir(directory) or directory == '':
            return directory
        else:
            print("Такой папки не существует. Попробуте ввести еще раз или нажмите Enter, чтобы завершить программу.")
            self.inputDirectory()


    def putHash(self,filename):
        image = Image.open(filename)
        image.draft('L', (32, 32))
        return imagehash.dhash(image)

    def uploadDirectory(self):
        path_images = []
        hash_images = []
        directory = self.inputDirectory()
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
        with alive_bar(count_image, title="Подготавливаем фотографии   ") as bar:
            with ThreadPoolExecutor(max_workers=mp.cpu_count() + 4) as pool:
                for hash_image in pool.map(self.putHash, path_images):
                    hash_images.append(hash_image)
                    bar()
                # hash_images.extend(pool.map(putHash, path_images))

        return directory, path_images, hash_images