from abc import ABCMeta, abstractmethod
import pygame

class Scene(metaclass = ABCMeta):
    def __init__(self, manager):
        self.manager = manager #reference to game manager
        self.draw_elems = []
        self.font = None
        self.active = False
        self.surface = None
        
    def insert_drawable_element(self, drawable):
        self.draw_elems.append(drawable)

    def _process_events(self):
        pass
    
    def _process_pressed_buttons(self):
        pressed_list = pygame.key.get_pressed()
        #print("Keys list:", pressed_list)
        for elems in self.draw_elems:
            elems._process_pressed_buttons(pressed_list, self.scr_dimen)
    
    @abstractmethod
    def draw():
        pass
    
    @abstractmethod
    def scene_loop(self):
        pass
    
class Solid_Color(Scene):
    def __init__(self, manager, color):
        super().__init__(manager)
        self.surface = pygame.Surface((self.manager.screen.get_size())).convert()
        self.surface.fill(color)
    
    def draw(self):
        self.manager.screen.blit(self.surface, (0,0))
        
    def scene_loop(self):
        while self.active:
            self.draw()