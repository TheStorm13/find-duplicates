import os

from src.config import DUPLICATE_FOLDER
from src.core.image_prossesing.duplication_handler import DuplicationHandler
from src.core.image_prossesing.image_processing import ImageProcessing
from src.core.model.image_data import ImageData
from src.core.model.replace_file import ReplaceFile
from src.core.storage.file_manager import FileManager
from src.core.storage.image_collector import ImageCollector


class DuplicateService:
    """Сервис для обработки изображений и управления бизнес-логикой."""

    def __init__(self):
        self.base_directory = None
        self.image_collector = ImageCollector()
        self.image_processing = ImageProcessing()
        self.duplication_handler = DuplicationHandler()
        self.file_manager = None

    def scan_directory(self, base_directory: str) -> list[ImageData] | None:
        """
        Сканирует директорию и возвращает количество изображений.
        :param directory: Путь к директории.
        :return: Количество найденных изображений.
        """
        if FileManager.check_directory(base_directory):
            self.base_directory = base_directory
            self.file_manager = FileManager(self.base_directory)
            images = self.image_collector.collect_images(self.base_directory)
            return images
        return None

    def calculate_hashes(self, images: list[ImageData]) -> list[ImageData]:
        """
        Вычисляет хэш изображений.
        :param path_images: Путь к изображению.
        :return: Хэш изображения.
        """
        return self.image_processing.calculate_hashes_multithreaded(images)

    def find_duplicates(self, images: list[ImageData]) -> list:
        """
        Находит и перемещает дубликаты изображений.
        :param directory: Путь к директории.
        :return: Количество найденных дубликатов.
        """
        return self.duplication_handler.find_duplicates(images)

    def move_duplicates(self, duplicate_paths: list[str]) -> None:
        """
        Перемещает дубликаты изображений.
        """
        duplicate_dir = FileManager.create_directory(self.base_directory, DUPLICATE_FOLDER)
        replace_files = []
        for path in duplicate_paths:
            replace_file = ReplaceFile(old_file_path=os.path.dirname(path),
                                       file_name=os.path.basename(path),
                                       new_file_path=duplicate_dir
                                       )
            replace_files.append(replace_file)

        self.file_manager.move_files(replace_files)

    def return_duplicates(self, base_directory) -> None:
        """
        Возвращает дубликаты изображений.
        """
        self.base_directory = base_directory
        self.file_manager.return_duplicates(self.base_directory)
