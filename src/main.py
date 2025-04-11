import logging

from PIL import ImageFile

from src.config import LOG_FILE_PATH
from src.CLI.main_cli import cli

ImageFile.LOAD_TRUNCATED_IMAGES = True

logging.basicConfig(
    level=logging.INFO,
    force=True,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode='w', encoding="utf-8"),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    # Запуск CLI.
    cli()

# для .exe
# pyinstaller -F --add-data ".\.venv\Lib\site-packages\grapheme\data\grapheme_break_property.json;grapheme\data" detection_image_duplicates.py
