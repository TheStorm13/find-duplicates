import imagehash

from src.service.duplication_handler import DuplicationHandler
from src.service.files.file_manager import FileManager
from src.service.image_collector import ImageCollector
from src.service.image_processing import ImageProcessing


class ImageService:
    """Сервис для обработки изображений и управления бизнес-логикой."""

    def __init__(self):
        self.base_directory = None
        self.image_collector = ImageCollector()
        self.image_processing = ImageProcessing()
        self.duplication_handler = DuplicationHandler()
        self.file_manager = FileManager()

    def scan_directory(self, base_directory):
        """
        Сканирует директорию и возвращает количество изображений.
        :param directory: Путь к директории.
        :return: Количество найденных изображений.
        """
        if self.image_collector.check_directory(base_directory):
            self.base_directory = base_directory
            path_images = self.image_collector.collect_images(self.base_directory)
            return path_images

    def calculate_hash(self, path_images):
        """
        Вычисляет хэш изображений.
        :param path_images: Путь к изображению.
        :return: Хэш изображения.
        """
        return self.image_processing.process_images(path_images)

    def find_duplicates(self, image_hashes: dict[str, imagehash.ImageHash]) -> list[str]:
        """
        Находит и перемещает дубликаты изображений.
        :param directory: Путь к директории.
        :return: Количество найденных дубликатов.
        """
        return self.duplication_handler.find_duplicates(image_hashes)

    def move_duplicates(self, duplicate_paths: list[str]) -> None:
        """
        Перемещает дубликаты изображений.
        """
        self.file_manager.move_duplicates(self.base_directory, duplicate_paths)

    def return_duplicates(self, base_directory) -> None:
        """
        Возвращает дубликаты изображений.
        """
        self.base_directory = base_directory
        self.file_manager.return_duplicates(self.base_directory)
