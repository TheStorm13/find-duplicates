from pathlib import Path
from typing import List, Final

# Определение корня проекта (более надежный способ)
PROJECT_ROOT: Final[Path] = Path(__file__).parent.resolve()

# Пути к файлам и директориям
LOG_DIR: Final[Path] = PROJECT_ROOT / "logs"
LOG_FILE_PATH: Final[Path] = LOG_DIR / "app.log"
DUPLICATE_FOLDER: Final[str] = "Duplicate"
METADATA_FILE_NAME: Final[str] = "duplicates_metadata.json"
IMAGE_EXTENSIONS: Final[List[str]] = [".jpg", ".jpeg", ".png"]

# Создаем директорию для логов, если она не существует
LOG_DIR.mkdir(exist_ok=True)
