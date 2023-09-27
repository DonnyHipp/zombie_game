import arcade
import settings


class Entity(arcade.Sprite):
    
    
    def __init__(self):

        super().__init__()
        path = None
        self.main_path = f"../resources/{path}"
        self.health = 100
        self.mv_speed = 1.4
        self.walk_textures = None
        self.front_direction = 0
        self.back_direction = 1
        self.left_direction = 3
        self.right_direction = 4
        self.cur_texture = 0
        

        self.character_face_direction = self.front_direction
    def _set_idle(self):
        self.idle_texture = self.load_idle()
        self.texture = self.idle_texture[0]

    def _get_textures(self):
        walk_textures = []
        for i in range(4):
            texture = self.load_texture_pair(i)
            walk_textures.append(texture)
        return walk_textures
    
    def load_texture_pair(self,i):
        return [
            arcade.load_texture(f"{self.main_path}_lstep_{i}"),
            arcade.load_texture(f"{self.main_path}_rstep_{i}"),
        ]
    def load_idle(self):
        return [arcade.load_texture(f"{self.main_path}_idle{i}" for i in range(4))]


    def update_animation(self, delta_time: float=1/60):
        """ Handles possible animations""" 

        if self.change_y < 0 and self.character_face_direction != self.back_direction:
            self.character_face_direction = self.back_direction

        elif self.change_y > 0 and self.character_face_direction != self.front_direction:
            self.character_face_direction = self.right_direction
            
        elif self.change_x < 0 and self.character_face_direction != self.left_direction:
            self.character_face_direction = self.left_direction

        elif self.change_x > 0 and self.character_face_direction != self.right_direction:
            self.character_face_direction = self.right_direction

        

        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture[0]
            return
        
        self.cur_texture += 1
        if self.cur_texture > 2:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.character_face_direction][self.cur_texture]

        