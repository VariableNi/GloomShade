import math
import arcade
from Paths import *

class ParallaxLayer:
    def __init__(self, texture_path, speed, y, scale=1):
        self.texture = arcade.load_texture(texture_path)
        self.speed = speed
        self.scale = scale
        self.y = y

        self.tile_width = self.texture.width * scale
        self.sprites = arcade.SpriteList()

    def update(self, camera_x):
        self.sprites.clear()

        # позиция слоя с параллаксом
        layer_x = camera_x * self.speed

        # левая граница экрана
        left_edge = layer_x - SCREEN_WIDTH / 2
        start_tile = math.floor(left_edge / self.tile_width)

        # рисуем с запасом
        tiles_needed = int(SCREEN_WIDTH / self.tile_width) + 3

        for i in range(tiles_needed):
            sprite = arcade.Sprite(self.texture, scale=self.scale)
            sprite.left = (start_tile + i) * self.tile_width
            sprite.center_y = self.y
            self.sprites.append(sprite)

    def draw(self):
        self.sprites.draw()


class ParallaxBackground:
    def __init__(self):
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)

    def update(self, camera_x):
        for layer in self.layers:
            layer.update(camera_x)

    def draw(self):
        for layer in self.layers:
            layer.draw()
