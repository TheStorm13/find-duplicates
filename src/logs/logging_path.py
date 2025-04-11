import logging
import os

from src.config import LOG_FILE_PATH  # Берем путь для логов из config.py


class LoggingPath:

    @staticmethod
    def ensure_log_directory_exists(log_file_path=LOG_FILE_PATH):
        directory = os.path.dirname(log_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Создана директория для логов.")
        logging.info("Логирование настроено успешно.")

    ensure_log_directory_exists()
