SCREEN_TITLE = "Zombie game"

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 704
ANIMATION_TIME = 10

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

GRAVITY = 0
# PLAYER_JUMP_SPEED = 20


WEAPON_LIST = {
        "AR": {
            "speed": 30,
            "bullet_break":4
        },

    }
WAVE_LIST= {
        1: {
            "weak": 9,
            "strong":1
        },
         3: {
            "weak": 12,
            "strong":8
        },
         3: {
            "weak": 20,
            "strong":10
        },
        

    }
