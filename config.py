# config.py
import os

# Автоматически определяем корень проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

LOG_FILE_PATH = os.path.join(PROJECT_ROOT, 'src', 'logs', 'app.log')
DUPLICATE_FOLDER = "Duplicate"
IMAGE_EXTENSIONS = [".jpg", "jpeg", ".png"]