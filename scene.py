from abc import ABCMeta, abstractmethod
import pygame
import drawable

class Scene(metaclass = ABCMeta):
    def __init__(self, manager, dimen = (0, 0)):
        self.manager = manager #reference to game manager
        self.label = ""
        self.draw_elems = []
        self.font = None
        self.active = False
        self.deactive_signal = False
        self.deact_mess = ""#indicates the label
        self.label = ""
        
        if dimen == (0, 0):
            self.surface = pygame.Surface(manager.scr_dimen).convert_alpha()
        else:
            self.surface = pygame.Surface(dimen).convert_alpha()
        
    def insert_drawable_element(self, drawable):
        self.draw_elems.append(drawable)

    #if after the scene, the program must quit, use python exit() and NOT use an inact_mess for that
    def _process_events(self, event_queue):
        for elems in self.draw_elems:
            elems._process_events(event_queue)
    
    def _process_pressed_buttons(self):
        pressed_list = pygame.key.get_pressed()
        #print("Keys list:", pressed_list)
        for elems in self.draw_elems:
            elems._process_pressed_buttons(pressed_list, self.scr_dimen)
        
    def draw(self):
        for elems in self.draw_elems:
            elems.pygame_draw_meth()
    
    @abstractmethod
    #scene loop must return the label of the next scene
    def scene_loop(self):
        pass
    
    def ask_deactivated(self):
        if self.deactive_signal == True:
            self.deactive_signal = False
            print(self.deact_mess)
            return self.deact_mess
    
class White_Screen(Scene):
    def __init__(self, manager, dimen = (0, 0)):
        super().__init__(manager, dimen)
        self.label = "white_screen"
        self.draw_elems.append(drawable.Background(0, 0, (255, 255, 255, 2), (800, 600)))
        self.draw_elems.append(drawable.Circle(50, 50, (0, 0, 200, 255), 25, self.surface))
    
    def draw(self):
        for elems in self.draw_elems:
            elems.pygame_draw_meth(self.surface)
        self.manager.screen.blit(self.surface, (0,0))
        
        
    def _process_events(self, event_queue):
        for event in event_queue:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Return pressed in Solid_Color")
                    self.active = False
                    self.deactive_signal = True
                    self.deact_mess = "red_screen"
    
    def scene_loop(self):
        self.active = True
        while self.active:
            self.draw()
        self.active = False
        return "red_screen"
    
class Red_Screen(Scene):
    def __init__(self, manager, dimen = (0, 0)):
        super().__init__(manager)
        self.label = "red_screen"
        self.draw_elems.append(drawable.Background(0, 0, (255, 0, 0, 255), (800, 600)))
    
    def draw(self):
        for elems in self.draw_elems:
            elems.pygame_draw_meth(self.surface)
        self.manager.screen.blit(self.surface, (0,0))
        
        
    def _process_events(self, event_queue):
        for event in event_queue:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.deactive_signal = True
                    exit()
    
    def scene_loop(self):
        self.active = True
        while self.active:
            self.draw()
        self.active = False
        return "red_screen"