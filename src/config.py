# config.py
import os

# Автоматически определяем корень проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

LOG_FILE_PATH = os.path.join(PROJECT_ROOT, 'logs', 'app.log')
DUPLICATE_FOLDER = "Duplicate"
METADATA_FILE_NAME = "duplicates_metadata.json"
IMAGE_EXTENSIONS = [".jpg", "jpeg", ".png"]