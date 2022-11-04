import os

from PIL import Image


def get_image_path(file_name: str) -> str:
    return os.path.join("static", "images", file_name)


def get_image(file_name: str) -> Image.Image:
    return Image.open(get_image_path(file_name))
