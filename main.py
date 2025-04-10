import os
import time
import multiprocessing as mp
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor
import imagehash
from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


def inputDirectory():
    directory = input()
    if os.path.isdir(directory) or directory == '':
        return directory
    else:
        print("Такой папки не существует. Попробуте ввести еще раз или нажмите Enter, чтобы завершить программу.")
        inputDirectory()


def putHash(filename):
    image = Image.open(filename)
    image.draft('L', (32, 32))
    return imagehash.dhash(image)


def uploadDirectory():
    path_images = []
    hash_images = []
    directory = inputDirectory()
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
            for hash_image in pool.map(putHash, path_images):
                hash_images.append(hash_image)
                bar()
            # hash_images.extend(pool.map(putHash, path_images))

    return directory, path_images, hash_images


def isDuplicateHash(hash_1, hash_2):
    return hash_1 == hash_2
    # return (hash_1 - hash_2)<10


def deleteDublicatedImagesHash(directory, path_images, hash_images, count_images):
    directory_dublicate = directory + r"\Duplicate"
    os.makedirs(directory_dublicate, exist_ok=True)
    count_dublicate = 0
    i, j = 0, 0
    with alive_bar(count_images, title="Ищем дубликаты              ") as bar:
        while (i < len(hash_images)):
            j = i + 1
            while (j < len(hash_images)):
                if (isDuplicateHash(hash_images[i], hash_images[j])):
                    count_dublicate += 1
                    new_path_image = directory_dublicate + path_images[j][path_images[j].rfind('\\'):]
                    os.replace(path_images[j], new_path_image)
                    hash_images.pop(j)
                    path_images.pop(j)
                    bar()
                else:
                    j += 1
            i += 1
            bar()
    return count_dublicate


if __name__ == "__main__":
    work_program = True
    print(mp.cpu_count())
    print("Данная программа ищет дубликаты. После нахождения они будут пенесены в папку \"Duplicate\".")
    while work_program:
        print("\nВведите путь к папке с фотографиями или нажмите Enter, чтобы завершить программу.\n" +
              r"Например: C:\Users\user\Pictures")
        directory, path_images, hash_images = uploadDirectory()
        count_image = len(hash_images)

        if directory != '' and directory != None and count_image > 0:
            count_dublicate = deleteDublicatedImagesHash(directory, path_images, hash_images, count_image)
            print("Найдено дубликатов: ", count_dublicate)
            if count_dublicate > 0:
                print(f"Все дубликаты перенесены в папку {directory + r"\Duplicate"}.")
        elif count_image == 0 and directory != '' and directory != None:
            print("Фотографий не найдено.")
        else:
            print("Программа завершена.")
            work_program = False
            time.sleep(1)

# для .exe
# pyinstaller -F --add-data ".\.venv\Lib\site-packages\grapheme\data\grapheme_break_property.json;grapheme\data" detection_image_duplicates.py