#Author: Daniel Amador dos Santos
#First game project with pygame
#Works with Python 3.4

#!!!COLOR KEY only works without alpha channel(and somehow makes sense)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#TODO: Need to do some modelling in loop scene shifting. And in all the classes and communicating methods so far
#      This surely needs some organization
COLOR_RED   = (255, 0,   0,   255)
COLOR_GREEN = (0,   180, 0,   255)
COLOR_BLUE  = (0,   0,   255, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY  = (128, 128, 128, 255)
COLOR_PCK   = (255, 0,   128)
COLOR_TRANS = (0,   0,   0,   0)

import pygame
from abc import ABCMeta, abstractmethod
import drawable
import scene

class GameManager(scene.Scene):
    def __init__(self):
        self.screen = None
        self.scenes = []
        self.active_scene = 0 #postition in the self.scenes of the current active scene
        
        self.scr_dimen = (0, 0)
        self.main_loop_on = True
        self.time_elapsed = 0
        self.clock = None
        self.font = None
        self.render_fps = True
        print("GameManager instantiated")
        
    def start_pygame(self, scr_dimen, win_caption):
        pygame.init()
        pygame.display.set_caption(win_caption)
        self.scr_dimen = scr_dimen
        self.screen = pygame.display.set_mode(self.scr_dimen, pygame.DOUBLEBUF, 32)
        
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        print("GameManager pygame initialized")
        
    
    def _render_fps(self, fps):
        if self.render_fps:
            text = "FPS: " + str(int(fps))
            fw, fh = self.font.size(text)
            surface = self.font.render(text, True, COLOR_GREEN)
            self.screen.blit(surface, (0, 0))
        
    def _process_events(self):
        #print("Event: ", self.main_loop_on)
        event_queue = pygame.event.get() 
        self.scenes[self.active_scene]._process_events(event_queue)
        for event in event_queue:
            #print(event)
            if event.type == pygame.QUIT:
                self.main_loop_on = False
            if event.type == pygame.KEYDOWN:
                #for elems in self.draw_elems:
                #    elems._process_events(event.key)
                if event.key == pygame.K_F1:
                    self.render_fps = not self.render_fps
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    self.main_loop_on = False
                    
                    
    #I'm doing this because I want to process pressed button regardless of being an event
    #or not. Events generate interruptions, and if for example I keep a key pressed,
    #e. g. a character running on a game, I want to process that
    def _process_pressed_buttons(self):
        pass
        
    def main_loop(self, start_act):#start_act is the starting active scene
        self.active_scene = start_act
        inact_mess = None
        
        while True == self.main_loop_on:
            self.scenes[self.active_scene].draw()
            self._render_fps(self.clock.get_fps())
            pygame.display.flip()
            self.time_elapsed += self.clock.tick(60)
            next_scene = self._process_events()
            self._process_pressed_buttons()
            inact_mess = self.scenes[self.active_scene].ask_inactivated()
            #print(inact_mess)
            if inact_mess != None:
                self.transition(self.locate_by_label(inact_mess))
                self.active_scene = self.locate_by_label(inact_mess)
            
    def transition(self, target_scene):
        temp_1 = self.scenes[self.active_scene].surface
        temp_black = pygame.Surface((self.screen.get_size())).convert_alpha()
        
        #fade in
        temp_black.fill((0, 0, 0, 255))
        alpha = 0
        while alpha < 254:
            temp_black.fill((0, 0, 0, alpha))
            pygame.display.flip()
            self.screen.blit(temp_1, (0, 0))
            self.screen.blit(temp_black, (0, 0))
            self._render_fps(self.get_fps())
            
            alpha += 4
            
        alpha = 255
        self.scenes[target_scene].draw()
        temp_2 = self.scenes[target_scene].surface
        
        #fade out
        while alpha >= 0:
            temp_black.fill((0, 0, 0, alpha))
            pygame.display.flip()
            self.screen.blit(temp_2, (0, 0))
            self.screen.blit(temp_black, (0, 0))
            self._render_fps(self.get_fps())
            
            alpha -= 4
    
    def insert_scene(self, scen):
        self.scenes.append(scen)
    
    def get_fps(self):
        return self.clock.get_fps()
    
    def get_elapsed_time():
        return self.time_elapsed
    
    def scene_loop(self):
        self.main_loop()
        
    def locate_by_label(self, label):
        for i in range(len(self.scenes)):
            if self.scenes[i].label == label:
                return i
        
    def draw():
        pass
        
def main():
    manager_obj = GameManager()
    manager_obj.start_pygame((800, 600), "First game")
    manager_obj.insert_scene(scene.Solid_Color(manager_obj, "white_screen", COLOR_WHITE))
    manager_obj.insert_scene(scene.Solid_Color(manager_obj, "red_screen", COLOR_RED))
    manager_obj.main_loop(0)

if __name__ == "__main__":
    main()