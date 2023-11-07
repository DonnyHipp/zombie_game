import os
import arcade
import settings
from .entity import Entity



class Player(Entity):
    
    
    def __init__(self,center_x,center_y,scale,weapon):

        super().__init__()
        base_dir = os.path.dirname(os.path.abspath(os.getcwd()))
        # self.main_path = "../resources/Player/player"
        self.main_path = os.path.join(base_dir,"resources","Player","player")
        self.damage = settings.PLAYER_DAMAGE
        self.center_x = center_x
        self.center_y = center_y
        self.scale = scale
        self.money = 20
        self.weapon = weapon

        self.shoot_speed = None
        self.bulbreak = None

        self.change_weapon(weapon)
        self.idle_texture = self._set_idle()
        self.texture = self.idle_texture[0]
        self.walk_textures = self._get_textures()
        self.set_hit_box(self.texture.hit_box_points)


    def change_weapon(self,weapon):
        if weapon not in settings.WEAPON_LIST:
            self.weapon = "AR"
        else:
            self.weapon = weapon
        self.shoot_speed = settings.WEAPON_LIST[self.weapon]["speed"]
        self.bulbreak =  settings.WEAPON_LIST[self.weapon]["bullet_break"]
        # Handles the player textures.
       