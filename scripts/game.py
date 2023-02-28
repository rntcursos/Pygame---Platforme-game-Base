import pygame
from scripts.camera import Camera
from scripts.fade import Fade
from scripts.obj import Obj
from scripts.player import Player
from scripts.settings import *
from scripts.ui import Ui


class Game:

    def __init__(self):
        self.maps = [MAP1, MAP2, MAP3]
        self.active = True
        self.current_level = 0
        self.level = Level(self.maps[self.current_level])
       
    def events(self,event):
        self.level.events(event)

    def draw(self):
        self.level.draw()

    def level_manager(self):
        if self.level.active_level == False and self.level.gameover == False:
            self.current_level += 1
            self.level = Level(self.maps[self.current_level])
        elif self.level.active_level == True and self.level.gameover == True:
            self.active = False

    def update(self):
        self.level_manager()
        self.level.update()

class Level:

    def __init__(self, worldmap):

        self.display = pygame.display.get_surface()
        self.all_sprites = Camera()
        self.colision_sprites = pygame.sprite.Group()

        self.active_level = True
        self.gameover = False

        self.fade = Fade(5)
        self.finish = Obj("assets/title/finish.png",[0,0], [self.all_sprites])
        self.player = Player([100,128], [self.all_sprites], self.colision_sprites)

        self.worldmap = worldmap
        self.generate_map()
    
        self.hud_ui = Ui()

    def generate_map(self):

        for row_index, row in enumerate(self.worldmap):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if col == "X":
                    Obj("assets/title/tile.png",[x,y], [self.all_sprites, self.colision_sprites])
                elif col == "C":
                    self.finish.rect.x = x
                    self.finish.rect.y = y
                elif col == "P":
                    self.player.rect.x = x
                    self.player.rect.y = y

    def events(self, event):
        pass
    
    def next_stage(self):
        if self.player.rect.colliderect(self.finish.rect):
            self.active_level = False

    def reset_position(self):
        if self.player.rect.y > HEIGHT:
            self.player.rect.x = 0
            self.player.rect.y = 0
            self.hud_ui.lifes -= 1
        
        if self.hud_ui.lifes <= 0:
            self.gameover = True

    def draw(self):
        self.all_sprites.costum_draw(self.player)
        self.hud_ui.draw()
        self.fade.draw()

    def update(self):
        self.all_sprites.update()
        self.next_stage()
        self.reset_position()
        self.hud_ui.update()



    



