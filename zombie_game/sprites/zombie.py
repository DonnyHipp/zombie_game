import os
import arcade
import settings
from .entity import Entity
import random


class Zombie(Entity):
    
    
    def __init__(self,center_x,center_y,scale,en_type):

        super().__init__()
        # self.texture = arcade.load_texture("../resources/player.png")

        base_dir = os.path.dirname(os.path.abspath(os.getcwd()))
        # self.main_path = "../resources/Zombie"
        self.main_path = os.path.join(base_dir,"resources","Zombie","")
        self.damage = 25
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
            self.health = 70
            self.mv_speed = random.uniform(0.4,1.1)
            self.damage = 7
            self.wait = 10
            self.main_path = os.path.join(self.main_path,"weak")
            # self.texture = arcade.load_texture(dr)
        elif self.en_type == "strong":
            self.mv_speed = 3
            self.damage = 10
            self.wait = 5
            self.main_path = os.path.join(self.main_path,"weak")
            # self.texture = arcade.load_texture(dr)
        else:
            self.mv_speed = 2
            self.damage = 7
            self.wait = 7
            self.main_path = os.path.join(self.main_path,"weak")
            # self.texture = arcade.load_texture(dr)
            # self.texture = arcade.load_texture(f"{self.main_path}/weak")
        

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