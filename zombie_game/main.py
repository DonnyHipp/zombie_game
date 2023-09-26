"""
Starting Template

"""
import asyncio
import arcade
import settings
from sprites.player import Player
import threading
import pytmx
import time
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# SCREEN_TITLE = "Starting Template"
# реализовать пули  
# реализовать стены
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
        arcade.set_background_color(arcade.color.BABY_BLUE_EYES)

    def setup(self):

        # cцена и карта
        tmx_map = "../resources/map/final_map.tmx"

        layer_options = {
            "Walls": {
                "use_spatial_hash": False,
            },
        }
        self.tile_map = arcade.tilemap.TileMap(map_file=tmx_map, scaling=1,layer_options=layer_options)
        
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # arcade.Scene.from_tilemap(map_object=tmx_map, layer="Tile Layer 1", scaling=1.0)

        # спрайт игрока
        self.player = Player(200,200,0.1,"AR")
        self.scene.add_sprite("Player", self.player)

        # спрайт противников


        # игровая камера
        self.camera = arcade.Camera(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        
        

        # ядро физики
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant=0, walls=self.scene["Walls"]
        )

        # оружие
        self.can_shoot = True
        self.shoot_timer = 0
        self.scene.add_sprite_list("Bullet")

        # добавляем коллизии
        
        # сцена
        


    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()

        self.camera.use()

        # self.gui_camera.use()
        self.scene.draw()

        output = f"Score: {1}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

        self.physics_engine.update()




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

        
    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """


        
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


        # physic update
        self.physics_engine.update()
        self.center_camera_to_player()
        self.scene.update()
            

    def _check_bullet_coll(self,bullet):
        hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene["Walls"],

                ],
            )
        if hit_list:
            bullet.remove_from_sprite_lists()


    def _make_bullet(self):
        bullet = arcade.Sprite("../resources/bullet.png", 0.2)
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y
        bullet.change_y = self.player.shoot_speed
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

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()