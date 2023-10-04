"""
Starting Template

"""
import asyncio
import arcade
import settings
from sprites.player import Player
from sprites.zombie import Zombie
import threading
import pytmx
import time
import random
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# SCREEN_TITLE = "Starting Template"
# реализовать пули  - DONE
# реализовать стены - DONE
# нарисовать все тайлы
# реализовать появление зомби
# реализовать колизию с зомби
# реализовать смерть персонажа
# реализовать меню
# реализовать переход с карты
# реализовать волны


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """
    
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.physics_engine = None
        self.player = None
        self.scene = None
        self.tile_map = None
        self.shoot_pressed = False
        self.can_shoot = False
        self.shoot_timer = 0
        self.h_box = None
        arcade.set_background_color(arcade.color.BABY_BLUE_EYES)
        self.gui_camera = None
        self.zombie =None
        self.poison_damage = 5

        self.current_wave = 1
        self.enemy_amount = None
        self.spawn_points = None
        self.zombie_is_spawn = True
        self.check_spawn_time = 10
        self.check_wave_time = 20
        self.check_damage_time_zombie =6
        


    def setup(self):

        # cцена и карта
        tmx_map = "../resources/map/final_map.tmx"
        
        layer_options = {
            "Walls": {
                "use_spatial_hash": True,
            },
            "death": {
                "use_spatial_hash": True,
            },
            "spawn1": {
                "use_spatial_hash": True,
            },
            "spawn2": {
                "use_spatial_hash": True,
            },
            "spawn3": {
                "use_spatial_hash": True,
            },
            "Doors": {
                "use_spatial_hash": True,
            },
        }
        self.tile_map = arcade.tilemap.TileMap(map_file=tmx_map, scaling=1,layer_options=layer_options)
        
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # спрайт игрока
        self.player = Player(300,300,1,"AR")
        
        self.scene.add_sprite("Player", self.player)


        # спрайт противников
        self.enemy_amount = settings.WAVE_LIST[self.current_wave]["weak"]
        self.spawn_points = self.scene.get_sprite_list(settings.WAVE_LIST[self.current_wave]["spawn"])
        self._zombie_spawn()


        # игровая камера
        self.camera = arcade.Camera(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(self.width, self.height)

        

        # ядро физики
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant=0, walls=self.scene["Walls"],
        )

        # оружие
        self.can_shoot = True
        self.shoot_timer = 0
        self.scene.add_sprite_list("Bullet",)
        

        # добавляем коллизии
        
        # сцена
        
        # смертельная зона
        self.check_time = 6 
        self.scene.add_sprite_list("damage")
        self.dmg_text = ""
        self.dmg_text_player = ""

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()

        
        self.camera.use()
        self.scene.draw()
        # self.gui_camera.use()
        self.gui_camera.use()

        
        health = f"Health: {self.player.health}"
        arcade.draw_text(health, 10, 20, arcade.color.RED, 14)
        arcade.draw_text(self.dmg_text, 660, 60, arcade.color.RED, 30)
        arcade.draw_text(self.dmg_text_player, 660, 100, arcade.color.RED, 30)

    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered,speed=0.1)

        
    def on_update(self, delta_time:float):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        
        self.physics_engine.update()


        if self.shoot_pressed:
            if self.can_shoot:
                self._make_bullet()
            else:
                self.shoot_timer += 1
                
                if self.shoot_timer == self.player.bulbreak:
                    self.can_shoot = True
                    self.shoot_timer = 0
                    
        for bullet in self.scene["Bullet"]:
            self._check_bullet_coll(bullet)



        for zombie in self.scene["Zombie"]:
            self._check_zombie_wall_coll(zombie)
            zombie.move_to_player(self.player)
            self._check_zombie_bullet_coll(zombie,self.player.damage)
            check = arcade.check_for_collision_with_list(zombie, self.scene["Player"])
            if check:
                if self.check_damage_time_zombie >10:
                    self.player.health -=zombie.damage
                    self.check_damage_time_zombie = 0
                    if not self.dmg_text_player:
                        self.dmg_text_player = "!Damage!"
                else:
                    self.check_damage_time_zombie += delta_time
            else:
                self.dmg_text_player = ""
                self.check_damage_time_zombie = 10
            
            if zombie.health <=0:
                self.player.money += 100
                print(self.player.money)
                zombie.remove_from_sprite_lists()
        


        #смертельная зоны чек
        check = arcade.check_for_collision_with_list(
            self.player, self.scene["death"]
        )


        if check:
            if self.check_time >5:
                self.player.health -=self.poison_damage
                self.check_time = 0
                if not self.dmg_text:
                    self.dmg_text = "!Damage!"
            else:
                self.check_time += delta_time
        else:
            self.dmg_text = ""
            self.check_time = 6


        # переключение волн
        if self.enemy_amount == 0 and len(self.scene["Zombie"])<=0:
            new_wave = self.current_wave + 1
            self.current_wave = new_wave if settings.WAVE_LIST.get(4) else 0
            if self.current_wave == 0:
                arcade.exit()
                return
            self.enemy_amount = settings.WAVE_LIST[self.current_wave]["weak"]
            self.spawn_points = settings.WAVE_LIST[self.current_wave]["spawn"]
        else:
            if self.check_spawn_time >= 10:
                self.enemy_amount -=1
                self._zombie_spawn()
                self.check_spawn_time =0
            else:
                self.check_spawn_time += delta_time



        dor_check = arcade.check_for_collision_with_list(self.player,self.scene["Doors"])
        if dor_check:
            print(dor_check)
            if self.player.money >=100:
                self.player.money -= 100
                self.player.center_y += 60
            else:
                self.player.center_y -= 10
                self.player.change_y = 0

        self.center_camera_to_player()

        self.scene.update()
        self.scene.update_animation(
            delta_time, [ "Player","Zombie"]
        )


    def _make_bullet(self):
        bullet = arcade.Sprite("../resources/bullet.png", 0.2)
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y

        if self.player.character_face_direction == self.player.front_direction:
            bullet.change_y = self.player.shoot_speed
        elif self.player.character_face_direction == self.player.back_direction:
            bullet.change_y = -self.player.shoot_speed
        elif self.player.character_face_direction == self.player.left_direction:
            bullet.change_x = -self.player.shoot_speed
            bullet.change_angle = 90
        elif self.player.character_face_direction == self.player.right_direction:
            bullet.change_x = self.player.shoot_speed

        self.scene.add_sprite("Bullet",bullet)
        self.can_shoot = False
        
        
        


    def on_key_press(self, key, key_modifiers):

        if (key == arcade.key.UP or key == arcade.key.W):
            self.player.change_y = self.player.mv_speed
        elif (key == arcade.key.DOWN or key == arcade.key.S):
            self.player.change_y = -self.player.mv_speed
        elif (key == arcade.key.RIGHT or key == arcade.key.D):
            self.player.change_x = self.player.mv_speed
        elif (key == arcade.key.LEFT or key == arcade.key.A):
            self.player.change_x = -self.player.mv_speed
        if key == arcade.key.Q:
            self.shoot_pressed = True


    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 0
 
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0

        if key == arcade.key.Q:
            self.shoot_pressed = False


    def _check_zombie_wall_coll(self,zombie):
        check = arcade.check_for_collision_with_list(
            zombie, self.scene["Walls"]
        )
        if check:
            if zombie.change_x > 0:
                pass
    
    
    def _check_zombie_bullet_coll(self,zombie,damage):
        # hit_list = arcade.check_for_collision_with_lists(zombie,self.scene["Bullet"],method=0)
        hit_list = None
        if hit_list:
            zombie.health -= damage


    def _zombie_spawn(self,first=None):
        start_zombie_point = self.spawn_points[round(random.randint(0,len(self.spawn_points)-1))]
        zombie = Zombie(start_zombie_point.center_x,start_zombie_point.center_y,1.3,"weak")
        self.scene.add_sprite("Zombie",zombie)
        


    def _check_bullet_coll(self,bullet):
        hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene["Walls"],
                    self.scene["Zombie"]

                ],
            )
        
        if hit_list:
            for hit in hit_list:
                if type(hit) == Zombie:
                    hit.health -= self.player.damage
            bullet.remove_from_sprite_lists()

def main():
    """ Main method """
    game = MyGame(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()