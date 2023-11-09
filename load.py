import os
import sys

import pygame

__all__ = []


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level():
    filename = "data/map.txt"
    with open(filename, "r") as mapfile:
        level_map = [line.strip() for line in mapfile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, ".")), level_map))
