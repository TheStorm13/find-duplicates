import json
import logging
from dataclasses import asdict
from pathlib import Path

from core.model.replace_file import ReplaceFile


class MetadataManager:
    def __init__(self, metadata_path: Path):
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
        return self.metadata_path.exists()

    def clean_metadata(self):
        """
        Очищает файл метаданных, если он существует.
        """
        if self.metadata_exists():
            try:
                self.metadata_path.unlink()
                logging.info(f"Файл метаданных {self.metadata_path} очищен.")
            except Exception as e:
                logging.error(f"Ошибка при очистке файла метаданных {self.metadata_path}: {e}")
        else:
            logging.info(f"Файл метаданных {self.metadata_path} не существует. Очистка не требуется.")

    def save_metadata(self, replace_files: list[ReplaceFile]) -> None:
        """
        Сохраняет метаданные в файл.
        """
        try:
            # Convert ReplaceFile objects to dicts and convert Path objects to strings
            def serialize_replace_file(rf: ReplaceFile):
                data = asdict(rf)
                data['old_file_path'] = str(data['old_file_path'])
                data['new_file_path'] = str(data['new_file_path'])
                return data

            data_to_save = [serialize_replace_file(rf) for rf in replace_files]

            with open(self.metadata_path, "w", encoding="utf-8") as file:
                json.dump(data_to_save, file, indent=4, ensure_ascii=False)
            logging.info(f"Метаданные успешно сохранены в {self.metadata_path}.")
        except Exception as e:
            logging.error(f"Ошибка при сохранении метаданных в {self.metadata_path}: {e}")

    def load_metadata(self) -> list[ReplaceFile]:
        """
        Загружает метаданные из файла.
        :return: Список объектов ReplaceFile.
        """
        if not self.metadata_exists():
            logging.warning(f"Metadata file '{self.metadata_path}' not found.")
            return []

        try:
            with open(self.metadata_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                replace_files = []
                for item in data:
                    item['old_file_path'] = Path(item['old_file_path'])
                    item['new_file_path'] = Path(item['new_file_path'])
                    replace_files.append(ReplaceFile(**item))
                logging.info(f"Metadata has been successfully loaded from '{self.metadata_path}'.")
                return replace_files
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding error in metadata file '{self.metadata_path}': {e}")
        except Exception as e:
            logging.error(f"Error while loading metadata from '{self.metadata_path}': {e}")

        return []
