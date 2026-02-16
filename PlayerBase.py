import arcade
from Health_bar import HealthBar
from Inventory import Inventory
import os
import math
from Paths import *
from main_assets import *
from abc import ABC, abstractmethod


class PlayerBase(arcade.Sprite, ABC):

    def __init__(self, wall_list):
        super().__init__()

        self.wall_list = wall_list
        self.scale = 1

        # ───── Movement ─────
        self.move_left = False
        self.move_right = False
        self.attacking = False
        self.want_jump = False
        self.on_ground = False
        self.run = False
        self.stay = True

        self.walk_speed = 5
        self.run_speed = 12
        self.jump_force = JUMP_FORCE

        self.facing_right = True

        # ───── Combat ─────
        self.attack_cooldown = 10
        self.attack_range = 64

        # ───── Stats ─────
        self.max_health = 100
        self.cur_health = 100
        self.type = 'player'

        self.invetory = Inventory()
        self.health_bar = HealthBar(self, 0.5 * 2)
    
    def regonizer_key(self, key):
        if key == arcade.key.A:
            self.move_left = True
        if key == arcade.key.D:
            self.move_right = True
        if key == arcade.key.SPACE:
            self.want_jump = True
        if key == arcade.key.LSHIFT:
            self.run = True

    def stop_recognize(self, key):
        if key == arcade.key.A:
            self.move_left = False
        if key == arcade.key.D:
            self.move_right = False
        if key == arcade.key.SPACE:
            self.want_jump = False
        if key == arcade.key.LSHIFT:
            self.run = False
    
    def update(self, delta_time):

        self.change_x = 0
        speed = self.run_speed if self.run else self.walk_speed

        if self.move_left:
            self.change_x -= speed
        if self.move_right:
            self.change_x += speed

        if self.change_x > 0:
            self.facing_right = True
        elif self.change_x < 0:
            self.facing_right = False

        self.scale_x = abs(self.scale_x) if self.facing_right else -abs(self.scale_x)

        if self.want_jump and self.on_ground:
            self.change_y = self.jump_force
            self.on_ground = False
        
        self.update_animation(delta_time)

        self.change_y -= GRAVITY

        super().update()

        self.resolve_ground_collision()
    
    def resolve_ground_collision(self):
        self.on_ground = False
        for wall in arcade.check_for_collision_with_list(self, self.wall_list):
            if self.change_y <= 0:
                self.bottom = wall.top
                self.change_y = 0
                self.on_ground = True
    
    @abstractmethod
    def attack(self, *args, **kwargs):
        pass
    
    def attacked(self, damage):

        if self.cur_health <= 0:
            pass
        
        else:
            self.cur_health -= damage 


