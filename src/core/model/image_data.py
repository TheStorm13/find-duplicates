from dataclasses import dataclass
from pathlib import Path

import imagehash


@dataclass
class ImageData:
    image_path: Path = None
    hash: imagehash.ImageHash = None
