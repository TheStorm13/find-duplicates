import logging
import time

from PIL import ImageFile

from config import LOG_FILE_PATH
from duplication_handler import DuplicationHandler
from image_processing import ImageProcessing
from logs.logging_path import LoggingPath

ImageFile.LOAD_TRUNCATED_IMAGES = True

logging.basicConfig(
    level=logging.INFO,
    force=True,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode='w',encoding="utf-8"),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    LoggingPath.ensure_log_directory_exists()

    work_program = True


    DublicationHandler = DuplicationHandler()
    ImageProcessing = ImageProcessing()

    print("Данная программа ищет дубликаты. После нахождения они будут перенесены в папку \"Duplicate\".")
    while work_program:

        print("\nВведите путь к папке с фотографиями или нажмите Enter, чтобы завершить программу.\n" +
              r"Например: C:\Users\user\Pictures")
        start_time = time.perf_counter()
        directory, path_images, hash_images = ImageProcessing.load_directory()
        count_image = len(hash_images)
        end_time = time.perf_counter()
        logging.info(f"Время загрузки директории: {end_time - start_time:.2f} секунд.")

        if directory != '' and directory != None and count_image > 0:
            count_dublicate = DublicationHandler.remove_duplicate_images_by_hash(directory, path_images, hash_images,
                                                                                 count_image)
            print("Найдено дубликатов: ", count_dublicate)
            if count_dublicate > 0:
                print(f"Все дубликаты перенесены в папку {directory + r"\Duplicate"}.")
        elif count_image == 0 and directory != '' and directory != None:
            print("Фотографий не найдено.")
        else:
            print("Программа завершена.")
            work_program = False
            time.sleep(1)

        end_time = time.perf_counter()
        logging.info(f"Время полной работы: {end_time - start_time:.2f} секунд.")

# для .exe
# pyinstaller -F --add-data ".\.venv\Lib\site-packages\grapheme\data\grapheme_break_property.json;grapheme\data" detection_image_duplicates.py
