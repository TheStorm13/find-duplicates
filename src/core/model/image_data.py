from dataclasses import dataclass

import imagehash


@dataclass
class ImageData:
    image_path: str = None
    hash: imagehash.ImageHash = None
