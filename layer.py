import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vec2

from tile import Tile

class Layer:
        
    def __init__(self, pos:Vec2, size:Vec2, tilesize:Vec2, tilemargin:Vec2, tilespacing:Vec2, scaling_factor:float, color:pygame.Color, tileset:pygame.Surface, offset:Vec2=Vec2(0,0), active:bool=False):
        self.pos = pos
        self.size = size
        self.tilesize = tilesize
        self.tilemargin = tilemargin
        self.tilespacing = tilespacing
        self._scaling_factor = scaling_factor   
        self.tileset = tileset
        self.color = color
        self.active = active
        self.offset = offset
        self.place_holder_tile = Tile(Vec2(0, 0), 2, self.color, self.tileset, self.tilesize, self.tilemargin, self.tilespacing, self.scaling_factor)
        self.__rect = pygame.Rect(self.pos, self.size.elementwise() * self.tilesize.elementwise())
        self.__surf = pygame.Surface(self.__rect.size)
        self.__scaled_surf = pygame.transform.scale_by(self.__surf, self.scaling_factor)
        
    def draw(self, surface:pygame.Surface, offset:Vec2=None):
        if offset is None:
            offset = self.offset
        surface.blit(self.__scaled_surf, self.pos + offset)
        if self.active:
            vec_mouse = Vec2(pygame.mouse.get_pos())-offset
            tile_size = self.tilesize.elementwise() * self.scaling_factor
            placeholder_pos = vec_mouse - \
                vec_mouse.elementwise() % tile_size + \
                    offset
            self.place_holder_tile.draw_scaled(surface,offset=placeholder_pos)
    
    def draw_tile(self, tile,pos:Vec2=None):
        if pos is None:
            tile.draw(self.__surf)
        else:
            tile.draw(self.__surf, pos)
        self.render_scaled_surf()

    def random_fill(self):
        for i in range(int(self.size.x)):
            for j in range(int(self.size.y)):
                self.draw_tile(Tile(Vec2(i, j), 2, self.color, self.tileset, self.tilesize, self.tilemargin, self.tilespacing, self.scaling_factor))

    def update(self):
        pass

    @property
    def scaling_factor(self):
        return self._scaling_factor
    
    @scaling_factor.setter
    def scaling_factor(self, value):
        self._scaling_factor = value
        self.place_holder_tile.scaling_factor = value
        self.render_scaled_surf()

    @property
    def selected_index(self):
        return self.place_holder_tile.index
    
    @selected_index.setter
    def selected_index(self, value):
        self.place_holder_tile.index = value

    def render_scaled_surf(self):
        self.__scaled_surf = pygame.transform.scale_by(self.__surf, self.scaling_factor)

    def add_tile(self,tile:Tile=None,offset:Vec2=None):
        if offset is None:
            offset = self.offset
        if tile:
            self.draw_tile(tile)
        else:
            vec_mouse = Vec2(pygame.mouse.get_pos())-offset
            tile_size = self.tilesize.elementwise() * self.scaling_factor
            placeholder_pos = ((vec_mouse - \
                vec_mouse.elementwise() % tile_size).elementwise() / self.scaling_factor).elementwise() // self.tilesize
            
            self.draw_tile(self.place_holder_tile,pos=placeholder_pos)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tile Test")
    clock = pygame.time.Clock()
    running = True

    scale = 1
    drag = False
    click_pos = Vec2(0, 0)
    offset = Vec2(0, 0)
    buildings = pygame.image.load(
        "assets\\Source\\Universal\\Universal-Buildings-and-walls.png"
    )
    layer = Layer(Vec2(0, 0), Vec2(40,40), Vec2(16,16), Vec2(0,0), Vec2(0,0), scale, pygame.Color(0, 0, 0, 0), buildings, Vec2(0), True)
    layer.random_fill()
    layer.selected_index = 5
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                scale += event.y * 0.1
                layer.scaling_factor = scale
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drag = True
                elif event.button == 3:
                    layer.add_tile()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag = False
            elif event.type == pygame.MOUSEMOTION:
                if drag:
                    offset += Vec2(event.rel)
                    layer.offset = offset
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    layer.active = not layer.active
                elif event.key == K_UP:
                    layer.selected_index += 1
                elif event.key == K_DOWN:
                    layer.selected_index -= 1

        layer.update()

        screen.fill((0, 0, 0))
        layer.draw(screen)

        pygame.display.flip()
        clock.tick(60)