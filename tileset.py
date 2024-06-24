from dataclasses import dataclass

import pygame
from pygame.math import Vector2 as Vec2

@dataclass
class TilesetProperties:
    name: str
    tilesize: Vec2
    tilemargin: Vec2
    tilespacing: Vec2
    tileset: pygame.Surface
    color: pygame.Color
    