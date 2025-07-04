import logging
from pathlib import Path

from config import METADATA_FILE_NAME, DUPLICATE_FOLDER
from core.model.replace_file import ReplaceFile
from core.storage.metadata_manager import MetadataManager


class FileManager:
    def __init__(self, root_directory: Path):
        self.root_directory = root_directory

    @staticmethod
    def check_directory(directory: Path) -> bool:
        if not directory.exists() or not directory.is_dir():
            logging.error(f"Такой папки не существует: {directory}")
            return False
        logging.info(f"Директория найдена: {directory}")
        return True

    @staticmethod
    def create_directory(directory_path: Path, directory_name: str) -> Path:
        """
        Создаёт папку для дубликатов, если она ещё не существует.

        :param directory_path: Базовая директория.
        :return: Путь к созданной или уже существующей директории.
        """
        # todo: проверка на существование директории и папки, которую хотим создать
        duplicate_dir = directory_path / directory_name
        duplicate_dir.mkdir(parents=True, exist_ok=True)
        logging.info(f"Создана директория: {directory_name}")
        return duplicate_dir

    def _move_file(self, replace_file: ReplaceFile) -> None:
        src = replace_file.old_file_path / replace_file.file_name
        dst = replace_file.new_file_path / replace_file.file_name
        try:
            if dst.exists():
                logging.error(f"Файл {replace_file.file_name} уже существует.")
                raise FileExistsError

            src.replace(dst)
            logging.debug(
                f"Файл {replace_file.file_name} перемещён "
                f"из {replace_file.old_file_path} в {replace_file.new_file_path}")
        except Exception as e:
            logging.error(
                f"Ошибка при перемещении файла {replace_file} "
                f"из {replace_file.old_file_path} в {replace_file.new_file_path}: {e}")

    def move_files(self, list_replaces: list[ReplaceFile]) -> None:

        duplicate_dir = self.root_directory / DUPLICATE_FOLDER
        metadata_path = duplicate_dir / METADATA_FILE_NAME
        metadata_manager = MetadataManager(metadata_path)

        for replace_file in list_replaces:
            self._move_file(replace_file)

        metadata_manager.save_metadata(list_replaces)

    # todo: есть метод для перемещения нескольких файлов.
    # todo: нужно написать еще один уровень абстракции для перемещения дубликатов и при поиске дубликатов
    def return_duplicates(self) -> None:
        """
        Возвращает все дубликаты из папки для дубликатов обратно в их исходные директории.

        :param duplicates_folder: Папка, где хранятся дубликаты.
        """
        duplicate_dir = self.root_directory / DUPLICATE_FOLDER
        metadata_path = duplicate_dir / METADATA_FILE_NAME
        metadata_manager = MetadataManager(metadata_path)

        # Проверяем, существуют ли метаданные
        if not metadata_manager.metadata_exists():
            logging.error(f"Файл метаданных не найден в директории {duplicate_dir}.")
            return

        # Загрузка метаданных
        replace_files: list[ReplaceFile] = metadata_manager.load_metadata()
        logging.info("Будет возвращено %d файлов.>", len(replace_files))

        # Создаем новые ReplaceFile объекты с поменянными путями
        return_files = []
        for replace_file in replace_files:
            # Создаем новый объект с поменянными путями
            return_file = ReplaceFile(
                old_file_path=replace_file.new_file_path,  # текущее расположение (папка дубликатов)
                new_file_path=replace_file.old_file_path,  # оригинальное расположение
                file_name=replace_file.file_name
            )
            return_files.append(return_file)

        # Возвращаем файлы
        for replace_file in return_files:
            self._move_file(replace_file)

        logging.info("Все возможные дубликаты возвращены на исходные позиции.")

        # Удаляем файл метаданных после возврата
        metadata_manager.clean_metadata()
