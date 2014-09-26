from abc import ABCMeta, abstractmethod
import pygame

class Scene(metaclass = ABCMeta):
    def __init__(self, manager, label):
        self.manager = manager #reference to game manager
        self.label = label
        self.draw_elems = []
        self.font = None
        self.active = False
        self.inactive_signal = False
        self.inact_mess = ""#indicates the label
        self.surface = None
        
    def insert_drawable_element(self, drawable):
        self.draw_elems.append(drawable)

    #if after the scene, the program must quit, use python exit() and NOT use an inact_mess for that
    def _process_events(self, event_queue):
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
    #scene loop must return the label of the next scene
    def scene_loop(self):
        pass
    
    def ask_inactivated(self):
        if self.inactive_signal == True:
            self.inactive_signal = False
            print(self.inact_mess)
            return self.inact_mess
    
class Solid_Color(Scene):
    def __init__(self, manager, label, color):
        super().__init__(manager, label)
        self.surface = pygame.Surface((self.manager.screen.get_size())).convert()
        self.surface.fill(color)
    
    def draw(self):
        self.manager.screen.blit(self.surface, (0,0))
        
        
    def _process_events(self, event_queue):
        for event in event_queue:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Return pressed in Solid_Color")
                    self.active = False
                    self.inactive_signal = True
                    self.inact_mess = "red_screen"
    
    def scene_loop(self):
        self.active = True
        while self.active:
            self.draw()
        self.active = False
        return "red_screen"