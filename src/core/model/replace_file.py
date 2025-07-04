from dataclasses import dataclass
from pathlib import Path


@dataclass
class ReplaceFile:
    old_file_path: Path
    new_file_path: Path
    file_name: str

    @property
    def old_full_path(self) -> Path:
        """Полный путь к оригинальному файлу."""
        return self.old_file_path / self.file_name

    @property
    def new_full_path(self) -> Path:
        """Полный путь к новому местоположению файла."""
        return self.new_file_path / self.file_name