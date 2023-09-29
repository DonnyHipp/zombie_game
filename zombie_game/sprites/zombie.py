import arcade
import settings
from .entity import Entity
import random

class Zombie(Entity):
    
    
    def __init__(self,center_x,center_y,scale,en_type):

        super().__init__()
        # self.texture = arcade.load_texture("../resources/player.png")

        self.main_path = "../resources/Zombie"
        self.force = 25
        self.center_x = center_x
        self.center_y = center_y
        self.scale = scale
        self.en_type = en_type

        self.__detect_type()
        self.idle_texture = self._set_idle()
        self.texture = self.idle_texture[0]
        self.walk_textures = self._get_textures()


        self.set_hit_box(self.texture.hit_box_points)

    def __detect_type(self):
        if self.en_type == "weak":
            self.health = 100
            self.mv_speed = random.random() 
            self.force = 5
            self.wait = 10
            self.main_path = f"{self.main_path}/weak"
        elif self.en_type == "strong":
            self.mv_speed = 3
            self.force = 10
            self.wait = 5
            self.main_path = f"{self.main_path}/weak"
        else:
            self.mv_speed = 2
            self.force = 7
            self.wait = 7
            self.texture = arcade.load_texture(f"{self.main_path}/weak")
        

    def move_to_player(self,player):
        if self.center_x < player.center_x-(player.width/2):
            self.change_x = self.mv_speed
        elif self.center_x > player.center_x+(player.width/2):
            self.change_x = -self.mv_speed
        else:
            self.change_x = 0

        if self.center_y < player.center_y-(player.height/2):
            self.change_y = self.mv_speed
        elif self.center_y > player.center_y+(player.height/2):
            self.change_y = -self.mv_speed
        else:
            self.change_y = 0


# class Wave():
#     WAVE_LIST = []

#     def __init__(self,current_wave,points,enemy) -> None:
#         self.points = points
#         self.wave_num = self._set_wave(num)

#     def _set_wave(self,wave):
#         self.wave = wave
#         self.change_wave()

#     def _set_enemy_amount(self,wave):
#         self.enemy_amount = get_enemy_amount
        
    
#     def __get_enemy_amount():
#         return sum([i["weak"] for _, i in  self.WAVE_LIST.items()])


#     def __change_wave(self):
#         pass


    