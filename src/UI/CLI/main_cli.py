import click

from src.logs.logging_path import LoggingPath
from src.service.image_service import ImageService

LoggingPath.ensure_log_directory_exists()
image_service = ImageService()


@click.group()
def cli():
    """
    Утилита для работы с изображениями.

    Позволяет сканировать директории, находить и перемещать дубликаты.
    """

    pass


@cli.command()
@click.argument('directory', type=click.Path(exists=True))
def find_dupl(directory):
    """
    Найти и переместить дубликаты изображений.

    DIRECTORY - Путь к директории, где будут найдены дубликаты.
    """

    # Сканирование директории
    path_images = image_service.scan_directory(directory)
    if not path_images:
        return

    # Вычисление хэшей изображений
    image_hashes = image_service.calculate_hash(path_images)

    # Поиск дубликатов
    duplicates = image_service.find_duplicates(image_hashes)
    if not duplicates:
        return

    # Подтверждение перед перемещением дубликатов
    if click.confirm("Найдено {} дубликатов. Хотите их переместить?".format(len(duplicates)), default=True):
        image_service.move_duplicates(duplicates)
        print("Дубликаты успешно перемещены.")
    else:
        print("Операция отменена. Дубликаты не были перемещены.")


@cli.command()
@click.argument('directory', type=click.Path(exists=True))
def return_dupl(directory):
    # Перемещение дубликатов
    image_service.return_duplicates(directory)
