import logging
import os

from PIL import ImageFile

from src.config import DUPLICATE_FOLDER, IMAGE_EXTENSIONS

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageCollector:
    """Класс отвечает за сбор изображений из указанной директории."""

    def check_directory(self, directory):
        if not directory or not os.path.isdir(directory):
            logging.error(f"Такой папки не существует: {directory}")
            return False
        logging.info(f"Директория найдена: {directory}")
        return True

    def collect_images(self, directory: str) -> list[str]:
        path_images = []  # Создаем пустой список для хранения результатов

        for root, dirs, files in os.walk(directory):
            # Убираем из списка обработки папки, начинающиеся с '!'
            dirs[:] = [d for d in dirs if not d.startswith('!')]

            if os.path.basename(root) == DUPLICATE_FOLDER:
                continue
            for file in files:
                if file.lower().endswith(tuple(IMAGE_EXTENSIONS)):
                    path_images.append(os.path.join(root, file))

        logging.info(f"Найдено изображений: {len(path_images)}")
        return path_images
