import pygame
from pygame.math import Vector2 as Vec2
from functools import lru_cache

from tileset import TilesetProperties,get_tile_top_left

@lru_cache
def scale_with_cache(surface, factor):
    return pygame.transform.scale_by(surface, factor)


class Tile:
    default_tileset_properties = TilesetProperties(
        name="default",
        tilesize=Vec2(16, 16),
        tilemargin=Vec2(0, 0),
        tilespacing=Vec2(0, 0),
        tileset=pygame.Surface((16, 16)),
        color=pygame.Color(255, 0, 0),
    )
    default_scaling_factor = 1

    def __init__(
        self,
        pos,
        index: int = 0,
        tileset_properties: TilesetProperties = None,
        scaling_factor: float = None,
    ):
        super().__init__()

        self.pos = pos

        self.tileset_properties = tileset_properties if tileset_properties else self.default_tileset_properties

        self._scaling_factor = (
            scaling_factor if scaling_factor else self.default_scaling_factor
        )

        self.__scaled_image = scale_with_cache(self.image, self._scaling_factor)
        self.__rect = pygame.Rect(Vec2(0, 0), self.tilesize * self._scaling_factor)
        self.index = index

        self.i = 0

    def update(self):
        pass

    def draw(self, surface, offset:Vec2=None):
        if offset is None:
            blit_pos = (
                self.pos.elementwise() * self.tilesize.elementwise()
            )
        else:
            blit_pos = (
                offset.elementwise() * self.tilesize.elementwise()
            )
        if self.x <= -1 or blit_pos[0] > surface.get_width():
            return
        if self.y <= -1 or blit_pos[1] > surface.get_height():
            return
        if self.index == -1:
            pygame.draw.rect(
                surface,
                self.color,
                pygame.Rect(
                    blit_pos, self.tilesize
                ),
            )
        else:
            pygame.draw.rect(
                surface,
                pygame.Color(0,0,0,0),
                pygame.Rect(
                    blit_pos, self.tilesize
                ),
            )
            surface.blit(self.image, blit_pos, pygame.Rect(Vec2(self.__rect.topleft).elementwise() / self.scaling_factor, self.tilesize))

    def draw_scaled(self, surface, offset=(0, 0)):
        blit_pos = (
            self.pos.elementwise() * self.tilesize.elementwise() * self.scaling_factor
            + offset
        )
        if self.x <= -1 or blit_pos[0] > surface.get_width():
            return
        if self.y <= -1 or blit_pos[1] > surface.get_height():
            return
        if self.index == -1:
            pygame.draw.rect(
                surface,
                self.color,
                pygame.Rect(
                    blit_pos, self.tilesize.elementwise() * self.scaling_factor
                ),
            )
        else:
            surface.blit(self.__scaled_image, blit_pos, self.__rect)

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    @property
    def color(self):
        return self.tileset_properties.color
    
    @color.setter
    def color(self, value):
        self.tileset_properties.color = value

    @property
    def image(self):
        return self.tileset_properties.tileset

    @image.setter
    def image(self, value):
        self.tileset_properties.tileset = value
        self.__scaled_image = scale_with_cache(self.image, self.scaling_factor)
        self.__update_rect()

    @property
    def tilesize(self):
        return self.tileset_properties.tilesize

    @tilesize.setter
    def tilesize(self, value):
        self.tileset_properties.tilesize = value
        self.__rect.size = self.tilesize * self.scaling_factor
        self.__update_rect()

    @property
    def tilemargin(self):
        return self.tileset_properties.tilemargin

    @tilemargin.setter
    def tilemargin(self, value):
        self.tileset_properties.tilemargin = value
        self.__update_rect()

    @property
    def tilespacing(self):
        return self.tileset_properties.tilespacing

    @tilespacing.setter
    def tilespacing(self, value):
        self.tileset_properties.tilespacing = value
        self.__update_rect()

    @property
    def scaling_factor(self):
        return self._scaling_factor

    @scaling_factor.setter
    def scaling_factor(self, value):
        if 0 > value:
            raise ValueError("Scaling factor must be greater than 0")
        self._scaling_factor = value
        self.__scaled_image = scale_with_cache(self.image, self.scaling_factor)
        self.__rect.size = self.tilesize * self.scaling_factor
        self.__update_rect()

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if value == -1:
            self._index = -1
        else:
            self._index = value % self.tileset_properties.tile_count
            self.__update_rect()

    def __update_rect(self):
        top_left = get_tile_top_left(self.tileset_properties, self.index) * self.scaling_factor
        self.__rect.topleft = top_left


if __name__ == "__main__":
    import random

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tile Test")
    clock = pygame.time.Clock()
    running = True

    scale = 1
    Tile.default_color = pygame.Color(255, 0, 0)

    nature = pygame.image.load(
        "assets\\Source\\Universal\\Universal-Trees-And-Mountains.png"
    )
    buildings = pygame.image.load(
        "assets\\Source\\Universal\\Universal-Buildings-and-walls.png"
    )
    tileset1 = TilesetProperties(
        name="nature",
        tilesize=Vec2(16, 16),
        tilemargin=Vec2(0, 0),
        tilespacing=Vec2(0, 0),
        tileset=nature,
        color=pygame.Color(255, 0, 0),
    )
    tileset2 = TilesetProperties(
        name="buildings",
        tilesize=Vec2(16, 16),
        tilemargin=Vec2(0, 0),
        tilespacing=Vec2(0, 0),
        tileset=buildings,
        color=pygame.Color(255, 0, 0),
    )
    nb_tiles_x = round((screen.get_width() / 16 + 0.5) * (1 / scale))
    nb_tiles_y = round((screen.get_height() / 16 + 0.5) * (1 / scale))
    tiles = [
        Tile(
            pos=Vec2(i, j),
            index=i + j * nb_tiles_x,
            tileset_properties=random.choice([tileset1, tileset2]),
            scaling_factor=scale,
        )
        for i in range(nb_tiles_x)
        for j in range(nb_tiles_y)
    ]

    drag = False
    click_pos = Vec2(0, 0)
    offset = Vec2(0, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                scale += event.y * 0.1
                for tile in tiles:
                    tile.scaling_factor = max(0, scale)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drag = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag = False
            elif event.type == pygame.MOUSEMOTION:
                if drag:
                    offset += Vec2(event.rel)

        for tile in tiles:
            tile.update()

        screen.fill((0, 0, 0))
        for tile in tiles:
            tile.draw_scaled(screen, offset)

        pygame.display.flip()
        clock.tick(60)
