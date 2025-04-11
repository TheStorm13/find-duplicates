import logging
import os

from PIL import ImageFile

from config import DUPLICATE_FOLDER, IMAGE_EXTENSIONS

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageCollector:
    """Класс отвечает за сбор изображений из указанной директории."""

    def check_directory(self, directory):
        # todo: Поменять проверку
        # todo: Выкидывать ошибку
        if os.path.isdir(directory) or directory == '':
            logging.info(f"Директория подтверждена: {directory}")
            return True
        else:
            logging.error(f"Такой папки не существует: {directory}")
            return False

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

        return path_images  # Возвращаем собранный список
