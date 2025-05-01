import json
import logging
import os
from dataclasses import asdict

from src.core.model.replace_file import ReplaceFile


class MetadataManager:
    def __init__(self, metadata_path: str):
        """
        Инициализация менеджера для работы с метаданными.

        :param metadata_path: Путь к файлу, где будут храниться метаданные.
        """
        self.metadata_path = metadata_path

    def metadata_exists(self) -> bool:
        # todo: перенести отсюда
        """
        Проверяет существование файла метаданных.

        :return: True, если файл метаданных существует, иначе False.
        """
        return os.path.exists(self.metadata_path)

    def clean_metadata(self):
        """
        Очищает файл метаданных, если он существует.
        """
        if self.metadata_exists():
            try:
                os.remove(self.metadata_path)
                logging.info(f"Файл метаданных {self.metadata_path} очищен.")
            except Exception as e:
                logging.error(f"Ошибка при очистке файла метаданных {self.metadata_path}: {e}")
        else:
            logging.info(f"Файл метаданных {self.metadata_path} не существует. Очистка не требуется.")

    def save_metadata(self, replace_files: list[ReplaceFile]) -> None:
        """
        Сохраняет метаданные в файл.

        :param replace_file: Словарь метаданных для сохранения.
        """
        try:
            # Convert the list of ReplaceFile objects to a list of dictionaries
            data_to_save = [asdict(rf) for rf in replace_files]

            with open(self.metadata_path, "w", encoding="utf-8") as file:
                json.dump(data_to_save, file, indent=4, ensure_ascii=False)
            logging.info(f"Метаданные успешно сохранены в {self.metadata_path}.")
        except Exception as e:
            logging.error(f"Ошибка при сохранении метаданных в {self.metadata_path}: {e}")

    def load_metadata(self) -> list[ReplaceFile]:
        """
        Загружает метаданные из файла.

        :return: Словарь метаданных.
        """
        #todo: errors
        if not self.metadata_exists():
            logging.warning(f"Metadata file '{self.metadata_path}' not found.")
            return None

        try:
            with open(self.metadata_path, "r", encoding="utf-8") as file:
                # Deserialize JSON content to a list of ReplaceFile objects
                data = json.load(file)
                replace_files = [ReplaceFile(**item) for item in data]
                logging.info(f"Metadata has been successfully loaded from '{self.metadata_path}'.")
                return replace_files
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding error in metadata file '{self.metadata_path}': {e}")
        except Exception as e:
            logging.error(f"Error while loading metadata from '{self.metadata_path}': {e}")

        return None

