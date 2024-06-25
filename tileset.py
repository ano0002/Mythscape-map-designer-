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
    
    @property
    def offset_by_tile(self):
        return self.tilesize + self.tilespacing
    
    @property
    def tile_by_line(self):
        return int((self.tileset.get_width() - self.tilemargin.x * 2) // self.offset_by_tile.x)
    
    @property
    def tile_by_column(self):
        return int((self.tileset.get_height() - self.tilemargin.y * 2) // self.offset_by_tile.y)
    
    @property
    def tile_count(self):
        return int(self.tile_by_line * self.tile_by_column)

    @property
    def aspect_ratio(self):
        return self.tilesize.x / self.tilesize.y

    def to_tileset_coords(self, tile_index: int) -> Vec2:
        return Vec2(
            tile_index % self.tile_by_line, tile_index // self.tile_by_line
        )


def get_tile_top_left(tileset: TilesetProperties, tile_index: int) -> Vec2:
    pos_on_tileset = tileset.to_tileset_coords(tile_index)
    
    return (tileset.tilemargin + pos_on_tileset).elementwise() * tileset.offset_by_tile


def get_tile_rect(tileset: TilesetProperties, tile_index: int) -> pygame.Rect:
    top_left = get_tile_top_left(tileset, tile_index)
    
    return pygame.Rect(top_left, tileset.tilesize)


def get_tile_surface(tileset: TilesetProperties, tile_index: int) -> pygame.Surface:
    return tileset.tileset.subsurface(get_tile_rect(tileset, tile_index))