import json
import logging
import os


class MetadataManager:
    def __init__(self, metadata_file: str):
        """
        Инициализация менеджера для работы с метаданными.

        :param metadata_file: Путь к файлу, где будут храниться метаданные.
        """
        self.metadata_file = metadata_file

    def metadata_exists(self) -> bool:
        """
        Проверяет существование файла метаданных.

        :return: True, если файл метаданных существует, иначе False.
        """
        return os.path.exists(self.metadata_file)

    def clean_metadata(self):
        """
        Очищает файл метаданных, если он существует.
        """
        if self.metadata_exists():
            try:
                os.remove(self.metadata_file)
                logging.info(f"Файл метаданных {self.metadata_file} очищен.")
            except Exception as e:
                logging.error(f"Ошибка при очистке файла метаданных {self.metadata_file}: {e}")
        else:
            logging.info(f"Файл метаданных {self.metadata_file} не существует. Очистка не требуется.")

    def save_metadata(self, metadata: dict) -> None:
        """
        Сохраняет метаданные в файл.

        :param metadata: Словарь метаданных для сохранения.
        """
        try:
            with open(self.metadata_file, "w", encoding="utf-8") as file:
                json.dump(metadata, file, indent=4, ensure_ascii=False)
            logging.info(f"Метаданные успешно сохранены в {self.metadata_file}.")
        except Exception as e:
            logging.error(f"Ошибка при сохранении метаданных в {self.metadata_file}: {e}")

    def load_metadata(self) -> dict:
        """
        Загружает метаданные из файла.

        :return: Словарь метаданных.
        """
        if not os.path.exists(self.metadata_file):
            logging.error(f"Файл метаданных {self.metadata_file} не найден.")
            return {}

        try:
            with open(self.metadata_file, "r", encoding="utf-8") as file:
                metadata = json.load(file)
                logging.info(f"Метаданные успешно загружены из {self.metadata_file}.")
                return metadata
        except Exception as e:
            logging.error(f"Ошибка при загрузке метаданных из {self.metadata_file}: {e}")
            return {}
