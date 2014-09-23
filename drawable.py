import pygame
from abc import ABCMeta, abstractmethod

class DrawableElement(metaclass = ABCMeta):
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.alpha = {'alpha':255, 'fading': True}
        self.surface = None
    
    def _process_events(self, event_type):
        pass
    
    def _process_pressed_buttons(self, pressed_list, scr_dimen):
        pass
    
    def blit(self, screen):
        screen.blit(self.surface, (self.x, self.y))
    
    def process_blink(self):
        if True == self.alpha['fading']:
            self.alpha['alpha'] -= 5
        else:
            self.alpha['alpha'] += 5
        
        if self.alpha['alpha'] <= 0:
            self.alpha['fading'] = False
            self.alpha['alpha'] = 0
            
        elif self.alpha['alpha'] >= 255:
            self.alpha['fading'] = True
            self.alpha['alpha'] = 255
        
        c = self.color
        self.color = (c[0], c[1], c[2], self.alpha['alpha'])
        #print(self.color)
        
        self.pygame_draw_meth()
        
    @abstractmethod
    def pygame_draw_meth(self):
        pass

class Background(DrawableElement):
    def __init__(self, x, y, color, size):#size: tuple (w,h)
        super().__init__(x, y, color)
        self.surface = pygame.Surface(size)
        self.surface.fill(self.color)
        self.surface = self.surface.convert()
        
    def pygame_draw_meth(self):
        self.surface.fill(self.color)
        self.surface = self.surface.convert()
        
class Circle(DrawableElement):
    def __init__(self, x, y, color, radius):
        super().__init__(x, y, color)
        self.radius = radius
        self.pygame_draw_meth()
        self.reverse_dir = [False, False] 
        
    def reset_alpha(self):
        print("Entered Circle reset_alpha")
        self.alpha['alpha'] = 255
        c = self.color
        self.color = (c[0], c[1], c[2], self.alpha['alpha'])
        self.pygame_draw_meth()
        
    def _process_pressed_buttons(self, pressed_list, scr_dimen):
        #print("circle.y:", self.y)
        #print("Pressed keys list:", pressed_list)
        if pressed_list[pygame.K_w] == True or pressed_list[pygame.K_UP]:
            self.y -= 8
        if pressed_list[pygame.K_a] == True or pressed_list[pygame.K_LEFT]:
            self.x -= 8
        if pressed_list[pygame.K_s] == True or pressed_list[pygame.K_DOWN]:
            self.y += 8
        if pressed_list[pygame.K_d] == True or pressed_list[pygame.K_RIGHT]:
            self.x += 8
        
        if self.x < 0: self.x = 0
        elif self.x > scr_dimen[0] - 2 * self.radius:
            self.x = scr_dimen[0] - 2 * self.radius
        if self.y < 0: self.y = 0
        elif self.y > scr_dimen[1] - 2 * self.radius:
            self.y = scr_dimen[1] - 2 * self.radius
    
    def dull_animation(self, scr_dimen):
        if self.reverse_dir[0] == False:
            self.x += 4
        else:
            self.x -= 4
        
        if self.reverse_dir[1] == False:
            self.y += 4
        else:
            self.y -= 4
            
        if self.x > scr_dimen[0] - 2 * self.radius:
            self.x = scr_dimen[0]
            self.reverse_dir[0] = True
        
        elif self.x < 0:
            self.x = 0
            self.reverse_dir[0] = False
        
        if self.y > scr_dimen[1] - 2 * self.radius:
            self.y = scr_dimen[1]
            self.reverse_dir[1] = True
            
        elif self.y < 0:
            self.y = 0
            self.reverse_dir[1] = False
    
        #print(self.x, self.y)
    
    def pygame_draw_meth(self):
        self.surface = pygame.Surface((2 * self.radius, 2 * self.radius))
        self.surface = self.surface.convert_alpha()
        self.surface.fill(COLOR_TRANS)
        pygame.draw.circle(self.surface, self.color, 
                          (self.radius, self.radius), self.radius)
        print("Circle color: ", self.color)
        
class Text(DrawableElement):
    def __init__(self, x, y, color, text):
        super().__init__(x, y, color)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.text = text
        self.fw, self.fh = self.font.size(text)
        self.pygame_draw_meth()
        
    def pygame_draw_meth(self):
        self.surface = self.font.render(self.text, True, self.color)