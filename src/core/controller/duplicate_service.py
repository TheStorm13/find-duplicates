from pathlib import Path

from config import DUPLICATE_FOLDER
from core.image_prossesing.duplication_handler import DuplicationHandler
from core.image_prossesing.image_processing import ImageProcessing
from core.model.image_data import ImageData
from core.model.replace_file import ReplaceFile
from core.storage.file_manager import FileManager
from core.storage.image_collector import ImageCollector


class DuplicateService:
    """Сервис для обработки изображений и управления бизнес-логикой."""

    def __init__(self, base_directory: Path ):
        self.base_directory = base_directory
        self.image_collector = ImageCollector()
        self.image_processing = ImageProcessing()
        self.duplication_handler = DuplicationHandler()
        self.file_manager = FileManager(base_directory)

    def scan_directory(self, base_directory: Path) -> list[ImageData] | None:
        """
        Сканирует директорию и возвращает количество изображений.
        :param directory: Путь к директории.
        :return: Количество найденных изображений.
        """
        if not FileManager.check_directory(base_directory):
            return None

        return self.image_collector.collect_images(self.base_directory)

    def calculate_hashes(self, images: list[ImageData]) -> list[ImageData]:
        """
        Вычисляет хэш изображений.
        :param path_images: Путь к изображению.
        :return: Хэш изображения.
        """
        return self.image_processing.calculate_hashes_multithreaded(images)

    def find_duplicates(self, images: list[ImageData]) -> list[Path]:
        """
        Находит и перемещает дубликаты изображений.
        :param directory: Путь к директории.
        :return: Количество найденных дубликатов.
        """
        return self.duplication_handler.find_duplicates(images)

    def move_duplicates(self, duplicate_paths: list[Path]) -> None:
        """
        Перемещает дубликаты изображений.
        """
        duplicate_dir = FileManager.create_directory(self.base_directory, DUPLICATE_FOLDER)
        replace_files = [
            ReplaceFile(
                old_file_path=path.parent,
                file_name=path.name,
                new_file_path=duplicate_dir
            )
            for path in duplicate_paths
        ]

        self.file_manager.move_files(replace_files)

    def return_duplicates(self) -> None:
        """
        Возвращает дубликаты изображений.
        """

        self.file_manager.return_duplicates()
