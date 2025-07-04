import logging
import pathlib
from pathlib import Path
from typing import Optional

import click
from PIL import ImageFile

from config import LOG_FILE_PATH
from core.controller.duplicate_service import DuplicateService
from core.model.image_data import ImageData

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


@click.group()
@click.version_option("1.0.0")
def cli():
    """Manage your project with ease."""


@cli.command()
@click.argument('path',
                required=False,
                type=click.Path(exists=True,
                                dir_okay=True,
                                path_type=pathlib.Path,
                                resolve_path=True))
@click.option("-y", "--yes", is_flag=True, help="Автоматически подтверждать все запросы")
def find_dupl(path: Optional[Path],
              yes: bool):
    """
    Найти и переместить дубликаты изображений.

    PATH - Путь к директории, где будут найдены дубликаты.
    """
    # Установка директории по умолчанию
    path = path or Path.cwd()
    click.secho(f"Поиск дубликатов в директории: {path}", fg="blue")

    image_service = DuplicateService(path)

    # Сканирование и обработка изображений
    path_images: list[ImageData] = image_service.scan_directory(path)
    if not path_images:
        click.secho("В указанной директории не найдено изображений.", fg="yellow")
        return

    # Вычисление хэшей изображений
    image_hashes = image_service.calculate_hashes(path_images)

    # Поиск дубликатов
    duplicates = image_service.find_duplicates(image_hashes)
    if not duplicates:
        return

    # Подтверждение перед перемещением дубликатов
    if yes or click.confirm(f"Найдено {len(duplicates)} дубликатов. Хотите их переместить?"):
        image_service.move_duplicates(duplicates)
        click.echo("Дубликаты успешно перемещены.")
    else:
        click.echo("Операция отменена. Дубликаты не были перемещены.")


@cli.command()
@click.argument('path',
                required=False,
                type=click.Path(exists=True,
                                dir_okay=True,
                                path_type=pathlib.Path,
                                resolve_path=True))
def return_dupl(path):
    # Перемещение дубликатов
    path = path or Path.cwd()

    image_service = DuplicateService(path)

    image_service.return_duplicates()


if __name__ == "__main__":
    # Запуск cli.
    cli()
