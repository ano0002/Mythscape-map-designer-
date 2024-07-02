import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vec2

from mapClass import Map
from button import TextButton, ImgButton
from tile_picker import TilePicker
from file_picker import FilePicker

class Main():
    def __init__(self, 
                 size:Vec2,
                 clock:pygame.time.Clock=pygame.time.Clock(),
                 screen_size:Vec2=Vec2(1920,1080),
                 config_file:str=""
                ) -> None:
        self.display = pygame.display.set_mode(size, RESIZABLE)
        self.clock = clock
        self.ui = []
        self.maps = []
        self.current_map_index = None
        self.windowed_size = size
        self.screen_size = screen_size
        self.running = False
        
        self.primary_color = (8,112,194)
        self.text_color = (255,255,255)
        self.bg_color = (32,32,32)
        self.h_bg_color = (45,45,45)
        self.font=pygame.font.Font("Assets/RetroGaming.ttf", 13)
        
        self.config_file = config_file
        
        self.top_toolbar_actions = {
            "New": self.new_map,
            "Open": self.open_map,
            "Save": self.save_map,
            "Save As": self.save_as_map,
            "Export": self.export_map,
        }
        self.tools = {
            "brush": 0,
            "eraser": 1,
            "bucket": 2,
            "cursor": 3
        }
        
        
        self.setup()
    
    
    def setup(self):
        self.load_config()
        self.setup_ui()
        self.setup_map()
    
    def load_config(self):
        if self.config_file=="": return
        pass
    
    def setup_ui(self):
        self.setup_toolbar()
    
    def setup_toolbar(self):
        # Top toolbar
        top_btn_width = 80
        top_btn_height = 30
        for i, name in enumerate(self.top_toolbar_actions.keys()):
            self.ui.append(TextButton(
                font=self.font,
                text=name,
                rect=pygame.Rect(i*top_btn_width, 0, top_btn_width, top_btn_height),
                callback=self.top_toolbar_actions[name],
                text_color=self.text_color,
                h_text_color=self.text_color,
                bg_color=self.bg_color,
                h_bg_color=self.h_bg_color,
                border_color=self.bg_color,
                h_border_color=self.primary_color,
                ))
            
        # Bottom toolbar
        btn_margin = Vec2(15,10)
        btn_spacing = 0
        btn_side = 40
        fill=btn_side*(1/4)
        for i, name in enumerate(self.tools.keys()):
            self.ui.append(ImgButton(
                img=pygame.image.load(f"Assets/UI/{name}.png"),
                rect=pygame.Rect(i*(btn_side+btn_spacing)+btn_margin.x, top_btn_height+btn_margin.y, btn_side, btn_side),
                callback=self.tool_select_callback,
                spacing=Vec2(fill, fill),
                bg_color=self.bg_color,
                h_bg_color=self.h_bg_color,
                name=name
                ))
    def setup_map(self):
        pass
    
    def tool_select_callback(self, button):
        print(f"Clicked on: {button.name}")
    
    def run(self):
        self.running = True
        while self.running:
            self.process_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == VIDEORESIZE:
                if not self.display.get_flags() & FULLSCREEN:
                    self.windowed_size = event.size
            elif event.type == KEYDOWN:
                if event.key == K_F11:
                    if self.display.get_flags() & FULLSCREEN:
                        self.display = pygame.display.set_mode(self.windowed_size, RESIZABLE)
                    else:
                        self.display = pygame.display.set_mode(self.screen_size, FULLSCREEN)
            elif event.type == MOUSEBUTTONDOWN:
                for ui in self.ui:
                    if ui.on_click():
                        break
        
        
    def update(self):
        for ui in self.ui:
            ui.update()
        if self.current_map_index is not None:
            self.maps[self.current_map_index].update()
        
    def draw(self):
        self.display.fill(self.bg_color)
        if self.current_map_index is not None:
            self.maps[self.current_map_index].draw(self.display)
        for ui in self.ui:
            ui.draw(self.display)
    
    def new_map(self,b):
        pass
    
    def open_map(self,b):
        pass
    
    def save_map(self,b):
        pass
    
    def save_as_map(self,b):
        pass
    
    def export_map(self,b):
        pass
        
    
    
if __name__ == "__main__":
    
    pygame.init()

    running = True
    infoObject = pygame.display.Info()
    w,h=infoObject.current_w,infoObject.current_h
    windowed_size = (w//(4/3), h//(4/3))

    main = Main(windowed_size,screen_size=(w,h))
    main.run()