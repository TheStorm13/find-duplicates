import logging
import os

from src.config import METADATA_FILE_NAME, DUPLICATE_FOLDER
from src.core.storage.metadata_manager import MetadataManager


class FileManager:
    def create_duplicate_dir(self, base_directory: str) -> str:
        """
        Создаёт папку для дубликатов, если она ещё не существует.

        :param base_directory: Базовая директория.
        :return: Путь к созданной или уже существующей директории.
        """

        duplicate_dir = os.path.join(base_directory, DUPLICATE_FOLDER)
        os.makedirs(duplicate_dir, exist_ok=True)
        logging.info(f"Создана директория для дубликатов: {duplicate_dir}")
        return duplicate_dir

    def _move_file(self, src_path: str, dst_dir: str) -> None:
        """
        Перемещает файл из src_path в указанную директорию.

        :param src_path: Путь к исходному файлу.
        :param dst_dir: Путь к директории назначения.
        """

        try:
            filename = os.path.basename(src_path)
            dst_path = os.path.join(dst_dir, filename)
            os.replace(src_path, dst_path)
            logging.debug(f"Файл {src_path} перемещён в {dst_path}")
        except Exception as e:
            logging.error(f"Ошибка при перемещении файла {src_path} в {dst_dir}: {e}")

    def move_duplicates(self, base_directory: str, duplicates: list[str]) -> None:
        """
        Перемещает дубликаты в указанную директорию.

        :param duplicates: Словарь с группами дубликатов.
        :param duplicate_dir: Директория для хранения дубликатов.
        """
        duplicate_dir = self.create_duplicate_dir(base_directory)

        metadata_manager = MetadataManager(os.path.join(duplicate_dir, METADATA_FILE_NAME))
        original_paths = {}

        for duplicate_path in duplicates:
            self._move_file(duplicate_path, duplicate_dir)
            file_name = os.path.basename(duplicate_path)
            original_paths[os.path.join(duplicate_dir, file_name)] = duplicate_path
        logging.info(f"Дубликаты успешно перемещены в директорию: {duplicate_dir}")

        # Сохраняем информацию об исходных путях для возврата
        metadata_manager.save_metadata(original_paths)

    # todo: есть метод для перемещения до этого
    def _return_file_to_original_location(self, current_path: str, original_path: str) -> None:
        """
        Возвращает дубликат на его исходное место.

        :param current_path: Текущий путь файла в папке дубликатов.
        :param original_path: Исходный путь файла.
        """
        try:
            # Проверка, существует ли файл на оригинальном пути
            if os.path.exists(original_path):
                logging.warning(f"Файл {original_path} уже существует. Добавляю суффикс '_duplicate'.")
                base, ext = os.path.splitext(original_path)
                original_path = f"{base}_duplicate{ext}"

            # Перемещаем файл обратно
            os.replace(current_path, original_path)
            logging.debug(f"Файл {current_path} возвращён в {original_path}")

        except Exception as e:
            logging.error(f"Ошибка при возврате файла {current_path} в {original_path}: {e}")

    # todo: есть метод для перемещения нескольких файлов.
    # todo: нужно написать еще один уровень абстракции для перемещения дубликатов и при поиске дубликатов

    def return_duplicates(self, base_directory: str) -> None:
        """
        Возвращает все дубликаты из папки для дубликатов обратно в их исходные директории.

        :param duplicates_folder: Папка, где хранятся дубликаты.
        """
        duplicate_dir = os.path.join(base_directory, "Duplicate")
        metadata_manager = MetadataManager(os.path.join(duplicate_dir, METADATA_FILE_NAME))

        # Проверяем, существуют ли метаданные
        if not metadata_manager.metadata_exists():
            logging.error(f"Файл метаданных не найден в директории {duplicate_dir}.")
            return

        # Загрузка метаданных
        original_paths = metadata_manager.load_metadata()
        logging.info("Будет возвращено %d файлов.>", len(original_paths))
        # Возвращаем файлы
        for current_path, original_path in original_paths.items():
            if os.path.exists(current_path):
                self._return_file_to_original_location(current_path, original_path)
            else:
                logging.warning(f"Файл {current_path} отсутствует в папке дубликатов. Пропускаю.")

        logging.info("Все возможные дубликаты возвращены на исходные позиции.")

        # Удаляем файл метаданных после возврата
        metadata_manager.clean_metadata()
