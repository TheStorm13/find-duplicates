import logging
import os

from src.config import METADATA_FILE_NAME, DUPLICATE_FOLDER
from src.core.model.replace_file import ReplaceFile
from src.core.storage.metadata_manager import MetadataManager


class FileManager:
    def __init__(self, root_directory: str):
        self.root_directory = root_directory


    @staticmethod
    def get_base_directory():
        # todo: проверить выдает ли директорию, откуда вызывается скрипт
        return os.getcwd()

    @staticmethod
    def check_directory(directory):
        if not directory or not os.path.isdir(directory):
            logging.error(f"Такой папки не существует: {directory}")
            return False
        logging.info(f"Директория найдена: {directory}")
        return True

    @staticmethod
    def create_directory(directory_path: str, directory_name: str) -> str:
        """
        Создаёт папку для дубликатов, если она ещё не существует.

        :param directory_path: Базовая директория.
        :return: Путь к созданной или уже существующей директории.
        """
        # todo: проверка на существование директории и папки, которую хотим создать
        duplicate_dir = os.path.join(directory_path, directory_name)
        os.makedirs(duplicate_dir, exist_ok=True)
        logging.info(f"Создана директория: {directory_name}")
        return duplicate_dir

    def _move_file(self, replace_file: ReplaceFile) -> None:
        src = os.path.join(replace_file.old_file_path, replace_file.file_name)
        dst = os.path.join(replace_file.new_file_path, replace_file.file_name)
        try:
            if os.path.exists(dst):
                logging.error(f"Файл {replace_file.file_name} уже существует.")
                raise FileExistsError

            os.replace(src, dst)
            logging.debug(
                f"Файл {replace_file} перемещён "
                f"из {replace_file.old_file_path} в {replace_file.new_file_path}")
        except Exception as e:
            logging.error(
                f"Ошибка при перемещении файла {replace_file} "
                f"из {replace_file.old_file_path} в {replace_file.new_file_path}: {e}")


    def move_files(self, list_replaces: list[ReplaceFile]) -> None:

        metadata_manager = MetadataManager(os.path.join(self.root_directory, METADATA_FILE_NAME))
        for replace_file in list_replaces:
            self._move_file(replace_file)

        metadata_manager.save_metadata(list_replaces)


    # todo: есть метод для перемещения нескольких файлов.
    # todo: нужно написать еще один уровень абстракции для перемещения дубликатов и при поиске дубликатов
    def return_duplicates(self, base_directory: str) -> None:
        """
        Возвращает все дубликаты из папки для дубликатов обратно в их исходные директории.

        :param duplicates_folder: Папка, где хранятся дубликаты.
        """
        duplicate_dir = os.path.join(base_directory, DUPLICATE_FOLDER)
        metadata_manager = MetadataManager(os.path.join(duplicate_dir, METADATA_FILE_NAME))

        # Проверяем, существуют ли метаданные
        if not metadata_manager.metadata_exists():
            logging.error(f"Файл метаданных не найден в директории {duplicate_dir}.")
            return

        # Загрузка метаданных
        replace_files: list[ReplaceFile] = metadata_manager.load_metadata()
        logging.info("Будет возвращено %d файлов.>", len(replace_files))
        # Возвращаем файлы
        for replace_file in replace_files:
            self._move_file(replace_file)

        logging.info("Все возможные дубликаты возвращены на исходные позиции.")

        # Удаляем файл метаданных после возврата
        metadata_manager.clean_metadata()
