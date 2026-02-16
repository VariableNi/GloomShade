import arcade
from Paths import *

SWORD_TEXTURE = arcade.load_texture(
    inventory_icon + "swords/sword.png"
)

#PLAYER--------------------------------------
KNIGHT_TEXTURE_LOAD = arcade.load_texture(
    animation_character+'knight/Knight_1/Idle1.png'
)

KNIGHT_TEXTURE = animation_character+'knight/Knight_1/Idle1.png'

WALK_SPRITE = arcade.load_animated_gif(
    animation_character+ "knight/Knight_1/walk.gif"
)

RUN_SPRITE = arcade.load_animated_gif(
    animation_character+ "knight/Knight_1/run.gif"
)

IDLE_SPRITE = arcade.load_animated_gif(
    animation_character+ "knight/Knight_1/Idle.gif"
)

ATTACK_SPRITE = arcade.load_animated_gif(
    animation_character+ "knight/Knight_1/attack.gif"
)

#MAP_R1--------------------------------------
BACKGROUND_forest = BACKGROUND_IMAGE_PATH+'nature_3/4.png'
BACKGROUND_sky = BACKGROUND_IMAGE_PATH+'nature_3/1.png'
BACKGROUND_mountains = BACKGROUND_IMAGE_PATH+'nature_3/2.png'






