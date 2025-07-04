import logging
from pathlib import Path

from config import DUPLICATE_FOLDER, IMAGE_EXTENSIONS
from core.model.image_data import ImageData

ImageData.LOAD_TRUNCATED_IMAGES = True


class ImageCollector:
    """Класс отвечает за сбор изображений из указанной директории."""

    def collect_images(self, root_directory: Path) -> list[ImageData]:
        images: list[ImageData] = []

        for path in root_directory.rglob('*'):
            # Пропускаем всё, что находится в папке-дубликате
            if DUPLICATE_FOLDER in path.parts:
                continue

            if any(part.startswith('!') for part in path.parts):
                continue

            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
                image = ImageData(image_path=path)
                images.append(image)

        logging.info(f"Найдено изображений: {len(images)}")
        return images
