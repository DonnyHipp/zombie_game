"""
Starting Template

"""

import os
import arcade
from arcade.application import Window
import settings
from sprites.player import Player
from sprites.zombie import Zombie
import threading
import pytmx
import time
import random
# реализовать смерть персонажа
# реализовать меню
# реализовать переход с карты
# реализовать волны

class MainMenu(arcade.View):
    """Меню"""

    def on_show_view(self):
        
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):

        self.clear()
        arcade.draw_text(
            "Главное меню! нажми для начала",
            settings.SCREEN_WIDTH / 2,
            settings.SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )
        arcade.draw_text(
            "Q - стрелять. Набери 210 монет для того, чтобы выиграть!",
            settings.SCREEN_WIDTH / 2,
            settings.SCREEN_HEIGHT / 3,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        # game_view.setup()
        self.window.show_view(game_view)

class GameView(arcade.View):
    """
    Игра
    """
    
    def __init__(self):
        super().__init__()

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
        self.camera = None
        self.current_wave = 1
        self.enemy_amount = None
        self.spawn_points = None
        self.zombie_is_spawn = True
        self.check_spawn_time = 10
        self.check_wave_time = 20
        self.check_damage_time_zombie =6
        self.zombie_damage = False

    def setup(self):
        print("start_setup")
        # cцена и карта
        tmx_map = os.path.join(os.path.dirname(os.path.abspath(os.getcwd())),"resources","map","final_map.tmx")
        # tmx_map = "../resources/map/final_map.tmx"
        
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

        self.gui_camera = arcade.Camera(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)



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
        
        
        # смертельная зона
        self.check_time = 6 
        self.scene.add_sprite_list("damage")
        self.dmg_text = ""
        self.dmg_text_player = ""

    def on_show_view(self):
        self.setup()
        
        


    def on_draw(self):
        """
        отрисовка экрана
        """

        self.clear()
        self.camera.use()
        self.scene.draw()
        # self.gui_camera.use()
        self.gui_camera.use()

        
        health = f"Health: {self.player.health}"
        money = f"Money: {self.player.money}"
        arcade.draw_text(health, 10, 20, arcade.color.RED, 14)
        arcade.draw_text(money, 10, 40, arcade.color.YELLOW, 14)

        arcade.draw_text(self.dmg_text, 660, 60, arcade.color.RED, 30)
        arcade.draw_text(self.dmg_text_player, 660, 100, arcade.color.RED, 30)

    def center_camera_to_player(self):
        """
        центрирование камеры к игроку
        """
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
        механики:
            - спавн зомби
            - зомби идет к игроку
            - игрок меняет анимацию
            - зомби меняет анимацию
            - игрок стреляет
            - игрок модет давать урон зомби и получат
            - игрок модет копить деньги за устранение зомби
            - игрок модет восстановить здоровье за 10 монет автоматически
            - игрок получает урон в смертельных зонах

            Что НЕ реализовано ( но планируется ):
            - игрок должен открывать двери за деньги
            - бусты скорости, бусты здоровья, бусты силы
            - переключение виды оружия/покупка оружия
            - изменение скорости спавна зомби
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

        # идем по вем зомби и смотрим 
        for zombie in self.scene["Zombie"]:
            # идем к игроку
            zombie.move_to_player(self.player)
            # проеврка колизии с пулей
            self._check_zombie_bullet_coll(zombie,self.player.damage)
            # проверка колизии с игроком
            

            # delete зомби если мало здоровья
            if zombie.health <=0:
                self.player.money += settings.POINTS
                zombie.remove_from_sprite_lists()
        

        check_zom = arcade.check_for_collision_with_list(self.player, self.scene["Zombie"])
        # если зомби у игрока он дает урон игроку
        if check_zom:
            if self.check_damage_time_zombie >4:
                self.player.health -=self.scene["Zombie"][0].damage
                self.check_damage_time_zombie = 0
                
                if not self.dmg_text_player:
                    self.dmg_text_player = "!Damage!"
                self.zombie_damage = True
            else:
                
                self.check_damage_time_zombie += delta_time
        else:
            self.zombie_damage = False
            self.dmg_text_player = ""
            self.check_damage_time_zombie = 10

        #смертельная зоны чек
        check = arcade.check_for_collision_with_list(
            self.player, self.scene["death"]
        )

        # проверка смертельной зоны
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

        # у игрока мало здоровья, но есть деньги == +20здоровья
        if self.player.health >0 and self.player.health<30 and self.player.money>=10:
            self.player.health += 20
            self.player.money -=10
            self.dmg_text = "+20 HEALTH"

        # у игркова больше 200 монет == он выиграл
        if self.player.money >= settings.END_MONEY:
            game_win = GameOverView("win")
            self.window.show_view(game_win)
            return

        # у игрока кончилось здоровье
        if self.player.health <=0:
            game_over = GameOverView("lose")
            self.window.show_view(game_over)

        # переключение волн и спавн
        if self.enemy_amount == 0:
            if self.current_wave != 0:
                new_wave = self.current_wave + 1
                self.current_wave = new_wave if settings.WAVE_LIST.get(new_wave) else 0
            
            if self.current_wave == 0 and len(self.scene["Zombie"]) <=0:
                game_over = GameOverView("win")
                self.window.show_view(game_over)
                return
            
            if self.current_wave != 0:
                self.enemy_amount = settings.WAVE_LIST[self.current_wave]["weak"]
                self.spawn_points = self.scene.get_sprite_list(settings.WAVE_LIST[self.current_wave]["spawn"])
            
      
        else:
            if self.check_spawn_time >= 4:
                self.enemy_amount -=1
                self._zombie_spawn()
                self.check_spawn_time =0
            else:
                self.check_spawn_time += delta_time

        self.center_camera_to_player()

        self.scene.update()
        self.scene.update_animation(
            delta_time, [ "Player","Zombie"]
        )


    def _make_bullet(self):
        """
        создание пули
        """
        bullet = arcade.Sprite("../resources/bullet.png", 0.2)
        bullet.center_x = self.player.center_x + random.uniform(0,12)
        bullet.center_y = self.player.center_y + random.uniform(0,12)

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
        """
       отслеживание нажатий на кнопку
        """
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
        отслеживание  отжатия кнопки
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



    
    def _check_zombie_bullet_coll(self,zombie,damage):
        """
        проверка колизии с зомби и пулей
        """
        hit_list = None
        if hit_list:
            zombie.health -= damage


    def _zombie_spawn(self,first=None):
        """
        спавн зомби
        """
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


class GameOverView(arcade.View):
    """Class to manage the game overview"""
    
    def __init__(self,end_type:str):
        super().__init__()
        self.end_type = end_type


    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        if self.end_type == "win":
            end_text = "Ты выйграл!"
        else:
            end_text = "Ты проиграл"
        arcade.draw_text(
            f"{end_text} Кликни для рестарта или Esc - для выхода",
            settings.SCREEN_WIDTH / 2,
            settings.SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            20,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = GameView()
        self.window.show_view(game_view)

    def on_key_press(self, key,_modifiers ):
        if key == arcade.key.ESCAPE:
            self.window.close()

def main():
    """Main function"""
    window = arcade.Window(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.SCREEN_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
