import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vec2

class Button:
    default_img = pygame.Surface((100, 50))
    default_img.fill((255, 255, 255))
    default_h_img = pygame.Surface((100, 50))
    default_h_img.fill((200, 200, 200))
    
    def __init__(self, rect, surf:pygame.Surface=None, h_surf:pygame.Surface=None, callback=lambda: None, **kwargs):
        self.image = surf if surf else self.default_img
        self.h_image = h_surf if h_surf else self.default_h_img
        self.rect = rect
        
        self.callback = callback
        self.hovered = False
        for key, value in kwargs.items():
            setattr(self, key, value)
  
    def on_click(self):
        if self.hovered:
            self.callback(self)
            return True
        return False
            
    def draw(self, surface):
        if self.hovered:
            surface.blit(self.h_image, self.rect)
        else:
            surface.blit(self.image, self.rect)
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not self.hovered:
            self.hovered = True
        elif not self.rect.collidepoint(mouse_pos) and self.hovered:
            self.hovered = False
  
class TextButton(Button):
    def __init__(self, text, rect, font, callback=lambda: None, **kwargs):
        super().__init__(rect, callback=callback)
        
        self.text = text
        self.font = font
        self.rect = rect
        
        self.text_color = (255, 255, 255)
        self.h_text_color = (255, 255, 255)
        
        self.bg_color = (32,32,32)
        self.h_bg_color = (45,45,45)
        
        self.border_color = (32,32,32)
        self.h_border_color = (8,112,194)
        self.border_width = 2
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.recalculate_bounds()
        self.render()
        self.__setattr__ = self.attr_setter
  
    def attr_setter(self, key, value):
        super().__setattr__(key, value)
        if key in ["rect"]:
            self.recalculate_bounds()
            self.render()
        if key in ["text", "font", "text_color", "h_text_color", "bg_color", "h_bg_color", "border_color", "h_border_color", "border_width"]:
            self.render()
  
    def recalculate_bounds(self):
        self.image = pygame.Surface(self.rect.size)
        self.h_image = pygame.Surface(self.rect.size)
  
    def render(self):
        self.h_image.fill(self.h_border_color)
        self.h_image.fill(self.h_bg_color, self.image.get_rect().inflate(-self.border_width*2, -self.border_width*2))
        text = self.font.render(self.text, True, self.h_text_color)
        self.h_image.blit(text, text.get_rect(center=self.h_image.get_rect().center))
    
        self.image.fill(self.border_color)
        self.image.fill(self.bg_color, self.image.get_rect().inflate(-self.border_width*2, -self.border_width*2))
        text = self.font.render(self.text, True, self.text_color)            
        self.image.blit(text, text.get_rect(center=self.image.get_rect().center))
  
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    button_font = pygame.font.Font(None, 30)
    buttons = [TextButton(
            text="Hello", 
            rect=pygame.Rect(i*100, j*60,100, 60), 
            font=button_font, 
            callback=lambda b: print(f"Clicked on: {b.c};{b.l}"), 
            l=i,
            c=j
        ) for i in range(8) for j in range(10)]
    
    running = True
    while running:
        screen.fill((32,32,32))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        if button.on_click():
                            break
        for button in buttons:
            button.update()
            button.draw(screen)
        pygame.display.flip()
        clock.tick(60)