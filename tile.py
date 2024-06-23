import pygame
from pygame.math import Vector2 as Vec2
from functools import lru_cache


@lru_cache
def scale_with_cache(surface, factor):
    return pygame.transform.scale_by(surface, factor)


class Tile:
    default_size = Vec2(16, 16)
    default_color = pygame.Color(0, 0, 0)
    default_image = pygame.Surface(default_size)
    default_image.fill((0, 255, 0))
    default_margin = Vec2(0, 0)
    default_spacing = Vec2(0, 0)
    default_scaling_factor = 1

    def __init__(
        self,
        pos,
        index: int = 0,
        color: tuple = False,
        image: pygame.Surface = False,
        tilesize: Vec2 = False,
        tilemargin: Vec2 = False,
        tilespacing: Vec2 = False,
        scaling_factor: float = False,
    ):
        super().__init__()

        self.color = color if color else self.default_color

        self._image = image if image else self.default_image
        self.pos = pos

        self._tilesize = tilesize if tilesize else self.default_size

        self._tilemargin = tilemargin if tilemargin else self.default_margin

        self._tilespacing = tilespacing if tilespacing else self.default_spacing

        self.__offset_by_tile = self.tilesize + self.tilespacing

        self.__tile_by_line = (
            self.image.get_width() - self.tilemargin[0] * 2
        ) // self.__offset_by_tile.x

        self.__tile_count = (
            self.__tile_by_line
            * (self.image.get_height() - self.tilemargin[1] * 2)
            // self.__offset_by_tile.y
        )

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
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self.__scaled_image = scale_with_cache(self.image, self.scaling_factor)
        self.__tile_by_line = (
            self.image.get_width() - self.tilemargin[0] * 2
        ) // self.__offset_by_tile.x
        self.__tile_count = (
            self.__tile_by_line
            * (self.image.get_height() - self.tilemargin[1] * 2)
            // self.__offset_by_tile.y
        )
        self.__update_rect()

    @property
    def tilesize(self):
        return self._tilesize

    @tilesize.setter
    def tilesize(self, value):
        self._tilesize = value
        self.__offset_by_tile = self.tilesize + self.tilespacing
        self.__tile_by_line = (
            self.image.get_width() - self.tilemargin[0] * 2
        ) // self.__offset_by_tile.x
        self.__rect.size = self.tilesize * self.scaling_factor
        self.__update_rect()

    @property
    def tilemargin(self):
        return self._tilemargin

    @tilemargin.setter
    def tilemargin(self, value):
        self._tilemargin = value
        self.__tile_by_line = (
            self.image.get_width() - self.tilemargin[0] * 2
        ) // self.__offset_by_tile.x
        self.__update_rect()

    @property
    def tilespacing(self):
        return self._tilespacing

    @tilespacing.setter
    def tilespacing(self, value):
        self._tilespacing = value
        self.__offset_by_tile = self.tilesize + self.tilespacing
        self.__tile_by_line = (
            self.image.get_width() - self.tilemargin[0] * 2
        ) // self.__offset_by_tile.x
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
            self._index = value % self.__tile_count
            self.__update_rect()

    def __update_rect(self):
        self.__tile_count = (
            self.__tile_by_line
            * (self.image.get_height() - self.tilemargin[1] * 2)
            // self.__offset_by_tile.y
        )

        pos_on_tileset = Vec2(
            self.index % self.__tile_by_line, self.index // self.__tile_by_line
        )

        top_left = (
            self.tilemargin
            + self.__offset_by_tile.elementwise() * pos_on_tileset.elementwise()
        ) * self.scaling_factor
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
    nb_tiles_x = round((screen.get_width() / 16 + 0.5) * (1 / scale))
    nb_tiles_y = round((screen.get_height() / 16 + 0.5) * (1 / scale))
    tiles = [
        Tile(
            pos=Vec2(i, j),
            index=i + j * nb_tiles_x,
            image=random.choice((nature, buildings)),
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
