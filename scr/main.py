import multiprocessing as mp
import time

from PIL import ImageFile

from duplication_handler import DuplicationHandler
from image_processing import ImageProcessing

ImageFile.LOAD_TRUNCATED_IMAGES = True


if __name__ == "__main__":
    work_program = True

    DublicationHandler = DuplicationHandler()
    ImageProcessing = ImageProcessing()
    print(mp.cpu_count())
    print("Данная программа ищет дубликаты. После нахождения они будут пенесены в папку \"Duplicate\".")
    while work_program:
        print("\nВведите путь к папке с фотографиями или нажмите Enter, чтобы завершить программу.\n" +
              r"Например: C:\Users\user\Pictures")
        directory, path_images, hash_images = ImageProcessing.uploadDirectory()
        count_image = len(hash_images)

        if directory != '' and directory != None and count_image > 0:
            count_dublicate = DublicationHandler.deleteDublicatedImagesHash(directory, path_images, hash_images, count_image)
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