import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vec2

class Button:
    def __init__(self, text, rect, font, callback=lambda: None, **kwargs):
        self.text = text
        self.font = font
        self.image = pygame.Surface(rect.size)
        self.rect = rect
        
        self.text_color = (255, 255, 255)
        self.h_text_color = (255, 255, 255)
        
        self.bg_color = (32,32,32)
        self.h_bg_color = (45,45,45)
        
        self.border_color = (32,32,32)
        self.h_border_color = (8,112,194)
        self.border_width = 2
        
        
        self.callback = callback
        self.hovered = False
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.render()
  
    def on_click(self):
        if self.hovered:
            self.callback(self)
            return True
        return False
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.hovered:
            self.hovered = True
            self.render()
        elif not self.rect.collidepoint(pygame.mouse.get_pos()) and self.hovered:
            self.hovered = False
            self.render()
  
    def render(self):
        if self.hovered:
            self.image.fill(self.h_border_color)
            self.image.fill(self.h_bg_color, self.image.get_rect().inflate(-self.border_width*2, -self.border_width*2))
            text = self.font.render(self.text, True, self.h_text_color)
        else:
            self.image.fill(self.border_color)
            self.image.fill(self.bg_color, self.image.get_rect().inflate(-self.border_width*2, -self.border_width*2))
            text = self.font.render(self.text, True, self.text_color)
            
        self.image.blit(text, text.get_rect(center=self.image.get_rect().center))
  
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    button_font = pygame.font.Font(None, 30)
    buttons = [Button("Hello", pygame.Rect(i*100, j*60,100, 60), button_font, lambda b: print(f"Clicked on: {b.c};{b.l}"), l=i,c=j) for i in range(8) for j in range(10)]
    
    running = True
    while running:
        screen.fill((32,32,32))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.on_click():
                        break
        for button in buttons:
            button.update()
            screen.blit(button.image, button.rect)
        pygame.display.flip()
        clock.tick(60)