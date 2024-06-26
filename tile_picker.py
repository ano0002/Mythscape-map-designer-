import math
from typing import Callable

import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vec2

from button import Button

from tileset import TilesetProperties, get_tile_surface


class TileButton(Button):
    def __init__(
        self,
        tileset: TilesetProperties,
        tile_index: int,
        rect,
        border_width: int = 1,
        border_color: pygame.Color = pygame.Color(0, 0, 0),
        callback:Callable=lambda x: setattr(x, "active", not x.active), # type: ignore
        active=False,
        **kwargs
    ):
        super().__init__(rect, callback=callback)

        self.tileset = tileset
        self.tile_index = tile_index
        self.active = active

        self.unscaled_src = get_tile_surface(tileset, tile_index)

        self.image = pygame.transform.scale(self.unscaled_src, self.rect.size)
        self.h_image = pygame.transform.scale(self.unscaled_src, self.rect.size)
        self.h_image.fill(pygame.Color(45,45,45,0), special_flags=BLEND_RGBA_ADD)
        self.a_image = pygame.transform.scale(self.unscaled_src, self.rect.size)

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.border_width = border_width
        self.border_color = border_color

        self.draw_borders()

    def draw_borders(self):
        self.a_image = self.h_image.copy()
        pygame.draw.rect(
            self.a_image, self.border_color, Rect(0, 0, self.rect.width, self.border_width)
        )
        pygame.draw.rect(
            self.a_image,
            self.border_color,
            Rect(0, 0, self.border_width, self.rect.height),
        )
        pygame.draw.rect(
            self.a_image,
            self.border_color,
            Rect(0, self.rect.height - self.border_width, self.rect.width, self.border_width),
        )
        pygame.draw.rect(
            self.a_image,
            self.border_color,
            Rect(self.rect.width - self.border_width, 0, self.border_width, self.rect.height),
        )

    def draw(self, surface):
        if self.active:
            surface.blit(self.a_image, self.rect)
        elif self.hovered:
            surface.blit(self.h_image, self.rect)
        else:
            surface.blit(self.image, self.rect)


class TilePicker:
    def __init__(
        self, 
        rect: pygame.Rect, 
        tileset: TilesetProperties, 
        current: int = 0, 
        background_color:pygame.Color=pygame.Color(90,90,90), 
        callback:Callable=lambda x:None, 
        **kwargs
    ):
        self._rect = rect
        self.tileset = tileset
        self.current = current
        self.tile_buttons = []
        self.background_color = background_color
        self.surf = pygame.Surface(self.rect.size)
        self.surf.fill(self.background_color)
        self.callback = callback
        
        for key, value in kwargs.items():
            setattr(self, key, value)


        self.get_max_tile_btn_scale()
        self.create_tiles()

    def create_tiles(self):
        stored_current = self.value
        
        def button_clicked(button):
            parent=button.parent
            parent.value = button.tile_index
            
        for btn in self.tile_buttons:
           del btn
        self.tile_buttons = []
        adjusted_tilesize = self.tileset.tilesize.elementwise() * self.factor
        for i in range(self.tileset.tile_count):
            pos = Vec2(i % self.tile_by_line, i // self.tile_by_line).elementwise() * adjusted_tilesize + self.rect.topleft
            btn = TileButton(
                tileset=self.tileset, 
                tile_index=i, 
                rect=pygame.Rect(pos, adjusted_tilesize), 
                border_width=1,
                parent=self,
                callback=button_clicked,
                active=i == stored_current
            )
            self.tile_buttons.append(btn)

    def get_max_tile_btn_scale(self):
        if self.tileset.tilesize.x >= self.rect.width or self.tileset.tilesize.y >= self.rect.height:
            return 1
        
        # Calculates total tileset size
        total_tileset_area = (
            self.tileset.tilesize.x * self.tileset.tilesize.y * self.tileset.tile_count
        )

        # Calculates opt1
        adjusted_x = (self.rect.width % self.tileset.tilesize.x) / (
            self.rect.width / self.tileset.tilesize.x
        ) + self.tileset.tilesize.x
        adjusted_y = adjusted_x / self.tileset.aspect_ratio
        size1 = Vec2(
            self.rect.width, self.rect.height - (self.rect.height % adjusted_y)
        )
        factor1 = size1.x * size1.y / total_tileset_area

        # Calculates opt2
        adjusted_y = (self.rect.height % self.tileset.tilesize.y) / (
            self.rect.height / self.tileset.tilesize.y
        ) + self.tileset.tilesize.y
        adjusted_x = adjusted_y * self.tileset.aspect_ratio
        size2 = Vec2(self.rect.width - (self.rect.width % adjusted_x), self.rect.height)
        factor2 = size2.x * size2.y / total_tileset_area

        """
        # Draws the rectangles for debugging
        pygame.draw.rect(
            self.surf, pygame.Color(0, 0, 255), Rect(0, 0, size1.x, size1.y)
        )
        pygame.draw.rect(
            self.surf, pygame.Color(0, 255, 0), Rect(0, 0, size2.x, size2.y)
        )
        """
        
        self.factor = max(math.sqrt(min(factor1, factor2)),1)

        return self.factor

    def update(self):
        for btn in self.tile_buttons:
            btn.update()

    def on_click(self):
        for i,btn in enumerate(self.tile_buttons):
            if btn.on_click():
                self.current = i
                self.callback(self)

    def draw(self, surface):
        surface.blit(self.surf, self.rect)
        for btn in self.tile_buttons:
            btn.draw(surface)

    @property
    def tile_by_line(self):
        return max(self.rect.width // (self.tileset.tilesize.x * self.factor),1)

    @property
    def tile_by_column(self):
        return max(self.rect.height // (self.tileset.tilesize.y * self.factor),1)

    @property
    def rect(self):
        return self._rect
    
    @rect.setter
    def rect(self, value):
        if value.width <= 0 or value.height <= 0:
            raise ValueError("Width and height must be greater than 0")
        self._rect = value
        self.surf = pygame.Surface(self.rect.size)
        self.surf.fill(self.background_color)
        self.get_max_tile_btn_scale()
        self.create_tiles()

    @property
    def value(self):
        return self.current

    @value.setter
    def value(self, value):
        self.current = value
        for btn in self.tile_buttons:
            btn.active = False
        self.tile_buttons[self.current].active = True
    

if __name__ == "__main__":

    pygame.init()

    tileset = TilesetProperties(
        name="Textured Rock",
        tilesize=Vec2(16, 16),
        tilemargin=Vec2(0, 0),
        tilespacing=Vec2(0, 0),
        tileset=pygame.image.load("assets\\Biome\\Foreground\\Textured\\Rock.png"),
        color=pygame.Color(0, 0, 0, 0),
    )

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tile Button Test")

    clock = pygame.time.Clock()

    tile_button = TileButton(tileset, 16, Rect(0, 0, 64, 64), border_width=4)

    tile_picker = TilePicker(
        Rect(64, 64, 10 * 32 + 2, 5 * 32), 
        tileset,
        callback=lambda x: print(x.value)
    )
    tile_picker.get_max_tile_btn_scale()

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    tile_button.on_click()
                    tile_picker.on_click()
            elif event.type == MOUSEMOTION:
                if event.buttons[2]:
                    tile_picker.rect = Rect(tile_picker.rect.topleft, (max(event.pos[0] - tile_picker.rect.left,1), max(event.pos[1] - tile_picker.rect.top,1)))

        tile_button.update()
        tile_button.draw(screen)

        tile_picker.update()
        tile_picker.draw(screen)

        pygame.display.flip()
        clock.tick(60)
