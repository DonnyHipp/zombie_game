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
        self.left_direction = 2
        self.right_direction = 3
        self.cur_texture = 0
        self.update_per_frame = 6

        self.character_face_direction = self.front_direction
        
    def _set_idle(self):
        # print(f"{self.main_path}_idle_{i}" for i in range(4))
        idle_texture = self.load_idle()
        return idle_texture
        

    def _get_textures(self):
        walk_textures = []
        for i in range(4):
            texture = self.load_texture_set(i)
            walk_textures.append(texture)
        return walk_textures
    
    def load_texture_set(self,i):
        res = [arcade.load_texture(f"{self.main_path}_lstep_{i}.png")] * self.update_per_frame + [arcade.load_texture(f"{self.main_path}_idle_{i}.png")] * self.update_per_frame + [arcade.load_texture(f"{self.main_path}_rstep_{i}.png")] * self.update_per_frame + [arcade.load_texture(f"{self.main_path}_idle_{i}.png")] * self.update_per_frame 

        return res
    def load_idle(self):
        return [arcade.load_texture(f"{self.main_path}_idle_{i}.png") for i in range(4)]


    def update_animation(self, delta_time):
        """ Handles possible animations""" 

        if self.change_y < 0 and self.character_face_direction != self.back_direction:
            if self.change_x == 0:
                self.character_face_direction = self.back_direction
            
        elif self.change_y > 0 and self.character_face_direction != self.front_direction:
            if self.change_x ==0:
                self.character_face_direction = self.front_direction
            
        elif self.change_x < 0 and self.character_face_direction != self.left_direction:
            self.character_face_direction = self.left_direction
            
        elif self.change_x > 0 and self.character_face_direction != self.right_direction:
            self.character_face_direction = self.right_direction
            
        

        if self.change_x == 0 and self.change_y == 0:
            if self.character_face_direction == self.front_direction:
                self.texture = self.idle_texture[0]
            if self.character_face_direction == self.back_direction:
                self.texture = self.idle_texture[1]
            if self.character_face_direction == self.left_direction:
                self.texture = self.idle_texture[2]
            if self.character_face_direction == self.right_direction:
                self.texture = self.idle_texture[3]
            return
        
        self.cur_texture += 1
        if self.cur_texture > self.update_per_frame *4 -1:
            self.cur_texture = 0
        # print(self.character_face_direction,self.cur_texture)
        self.texture = self.walk_textures[self.character_face_direction][self.cur_texture]

        