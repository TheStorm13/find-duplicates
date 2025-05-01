import logging
import os

from src.config import DUPLICATE_FOLDER, IMAGE_EXTENSIONS
from src.core.model.image_data import ImageData

ImageData.LOAD_TRUNCATED_IMAGES = True


class ImageCollector:
    """Класс отвечает за сбор изображений из указанной директории."""

    def collect_images(self, root_directory: str) -> list[ImageData]:
        images = []  # Создаем пустой список для хранения результатов

        for root, dirs, files in os.walk(root_directory):
            # Убираем из списка обработки папки, начинающиеся с '!'
            dirs[:] = [d for d in dirs if not d.startswith('!')]

            if os.path.basename(root) == DUPLICATE_FOLDER:
                continue

            for file in files:
                if file.lower().endswith(tuple(IMAGE_EXTENSIONS)):
                    image = ImageData(image_path=os.path.join(root, file))
                    images.append(image)

        logging.info(f"Найдено изображений: {len(images)}")
        return images
