import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vec2

from typing import List

from layer import Layer
from entity import Entity
from tileset import TilesetProperties

class Map:
    def __init__(self,
                 size:Vec2,
                 tilesets:List[TilesetProperties],
                 layers:List[Layer],
                 entities:List[Entity],
                 active_layer:int=-1,
                 display_offset:Vec2=Vec2(0,0),
                 display_scale:float=1.0,
                 default_tileset_index:int=0):
        self.size = size
        self.tilesets = tilesets
        self.layers = layers
        self.entities = entities
        self.active_layer = active_layer
        self.display_offset = display_offset
        self.display_scale = display_scale
        self.default_tileset_index = default_tileset_index
        
    def draw(self,surface:pygame.Surface):
        for layer in self.layers:
            layer.draw(surface,self.display_offset)
        for entity in self.entities:
            entity.draw(surface,self.display_offset)
        
    def update(self):
        for layer in self.layers:
            layer.update()
        for entity in self.entities:
            entity.update()
    
    @property
    def active_layer(self):
        return self._active_layer
    
    @active_layer.setter
    def active_layer(self,value:int):
        if value == -1:
            for layer in self.layers:
                layer.active = False
            self._active_layer = -1
        elif value < len(self.layers):
            for i,layer in enumerate(self.layers):
                layer.active = i == value
            self._active_layer = value
        else:
            raise IndexError("Layer index out of range")
    
    @property
    def display_offset(self):
        return self._display_offset
    
    @display_offset.setter
    def display_offset(self,value:Vec2):
        self._display_offset = value
        for layer in self.layers:
            layer.offset = value
        for entity in self.entities:
            entity.offset = value
    
    @property
    def display_scale(self):
        return self._display_scale
    
    @display_scale.setter
    def display_scale(self,value:float):
        self._display_scale = max(0.001,value)
        for layer in self.layers:
            layer.scaling_factor = self._display_scale
        for entity in self.entities:
            entity.scaling_factor = self._display_scale
    
    def append_layer(self,layer:Layer=None,active:bool=True,index:int=-1):
        if layer is None:
            tileset = self.tilesets[self.default_tileset_index]
            layer = Layer(
                pos=Vec2(0,0),
                size=self.size,
                scaling_factor=self.display_scale,
                offset=self.display_offset,
                active=active,
                tileset_properties=tileset
            )
            layer.selected_index = 16
        if index == -1:
            self.layers.append(layer)
        else:
            self.layers.insert(index,layer)
        if active:
            self.active_layer = len(self.layers) - 1
    
    def append_entity(self,entity:Entity):
        self.entities.append(entity)
    
    @property
    def is_tile_layer_active(self):
        return self.active_layer != -1
    
    def export(self,format="jpg"):
        return NotImplemented

    def __str__(self):
        return "Map with {} layers and {} entities".format(len(self.layers),len(self.entities))+\
                "\nActive layer: {}".format(self.active_layer)+\
                "\nTilesets nb: {}".format(len(self.tilesets))

if __name__=="__main__":
    import glob
    
    map_size = Vec2(50,50)
    
    tilesets = []
    root = "assets\\Biome\\Foreground\\"
    for tileset in glob.glob(root+"*\\*.png"):
        properties = TilesetProperties(
            name=".".join(tileset[len(root):].split(".")[:-1]).replace("\\"," "),
            tilesize=Vec2(16,16),
            tilemargin=Vec2(0,0),
            tilespacing=Vec2(0,0),
            tileset=pygame.image.load(tileset),
            color=pygame.Color(0,0,0,0)
            )
        tilesets.append(properties)
        print(properties.name)
    
    layers = []
    entities = []
    
    my_map = Map(
        map_size,
        tilesets,
        layers,
        entities
        )
    
    print(my_map)
    
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Map")
    clock = pygame.time.Clock()
    
    drag = False
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                my_map.display_scale += event.y * 0.1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drag = True
                elif event.button == 3:
                    if my_map.is_tile_layer_active:
                        my_map.layers[my_map.active_layer].add_tile()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag = False
            elif event.type == pygame.MOUSEMOTION:
                if drag:
                    my_map.display_offset += Vec2(event.rel)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    my_map.active_layer = (my_map.active_layer + 1) % len(my_map.layers)
                    
                elif event.key == K_RIGHT:
                    if my_map.is_tile_layer_active:
                        my_map.layers[my_map.active_layer].selected_index += 1
                    
                elif event.key == K_LEFT:
                    if my_map.is_tile_layer_active:
                        my_map.layers[my_map.active_layer].selected_index -= 1
                
                elif event.key == K_UP:
                    my_map.default_tileset_index = (my_map.default_tileset_index + 1) % len(my_map.tilesets)
                    print(my_map.tilesets[my_map.default_tileset_index].name)
                    
                elif event.key == K_DOWN:
                    my_map.default_tileset_index = (my_map.default_tileset_index - 1) % len(my_map.tilesets)
                    print(my_map.tilesets[my_map.default_tileset_index].name)
                
                elif event.key == K_KP_PLUS:
                    my_map.append_layer()
                    print(my_map)
                    
        my_map.update()

        screen.fill((0, 0, 0))
        my_map.draw(screen)

        pygame.display.flip()
        clock.tick(60)