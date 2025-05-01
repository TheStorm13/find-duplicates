from dataclasses import dataclass


@dataclass
class ReplaceFile:
    old_file_path: str
    new_file_path: str
    file_name: str
