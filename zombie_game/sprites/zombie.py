import arcade
import settings
from entity import Entity


class Player(Entity):
    
    
    def __init__(self,center_x,center_y,scale,en_type):

        super().__init__()
        # self.texture = arcade.load_texture("../resources/player.png")

        self.main_path = "../resources/Zombie"
        self.damage = 25
        self.center_x = center_x
        self.center_y = center_y
        self.scale = scale
        self.en_type = en_type

        self.shoot_speed = None
        self.bulbreak = None

        self.__detect_type()

        self._set_idle()
        
        self.walk_textures = self._get_textures()

        
        
        self.health = 100
        self.mv_speed = 2
        self.bullet_damage = 25
        self.center_x = center_x
        self.center_y = center_y
        self.scale = scale

        self.shoot_speed = None
        self.bulbreak = None



    def __detect_type(self):
        if self.en_type == "weak":
            self.mv_speed = 1
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
            self.texture = arcade.load_texture("../resources/player.png")
        # Handles the player textures.
       

        # self.idle_sprite = load_texture_pair("Sprites/player.png")

        # self.walk_textures = []
        # for i in range(1,2,1):
        #     texture = load_texture_pair("Sprites/player_move_"+str(i)+".png")
        #     self.walk_textures.append(texture)

    # def update_animation(self, delta_time: float=1/60):
    #     """ Handles possible animations""" 

    #     if self.change_x < 0 and self.character_face_direction == self.face_right:
    #         self.character_face_direction = self.face_left
    #     elif self.change_x > 0 and self.character_face_direction == self.face_left:
    #         self.character_face_direction = self.face_right
    #     if self.change_x == 0 and self.change_y == 0:
    #         self.texture = self.idle_sprite[0]
    #         return
    #     if self.current_texture > 2 * self.updates_per_frame:
    #         self.current_texture = 0
    #     self.texture = self.walk_textures[self.current_texture // self.updates_per_frame][self.character_face_direction]

    # def take_damage(self,damage_taken):
    #     """ Handles damage taken and health point reduction. """

    #     self.damage_taken = damage_taken
    #     self.health -= self.damage_taken