import arcade
from Health_bar import HealthBar
from Inventory import Inventory
import os
import math
from Paths import *
from main_assets import *

class Player(arcade.Sprite):
    def __init__(self, filename, wall_list):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден")
        super().__init__(filename, scale=0.5)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.attack_cooldown = 0 
        self.attack_range = 64  
        self.damage = 10
        self.max_health = 100
        self.cur_health = 100
        self.type = 'player'
        self.health_bar = HealthBar(self, self.scale[0]*2)
        self.invetory = Inventory()
        self.counter_kills = 0
        self.move_left = False
        self.move_right = False
        self.run = False
        self.facing_right = True
        self.scale = 0.5
        self.on_ground = False
        self.want_jump = False
        self.wall_list = wall_list
        self.walk_sprite = WALK_SPRITE
        self.run_sprite = RUN_SPRITE
    
    def regonizer_key(self, key):
        global MOVEMENT_SPEED_PLAYER
        
        if key == arcade.key.A:
            self.move_left = True

        if key == arcade.key.D:
            self.move_right = True
        
        if key == arcade.key.P:
            print(self.counter_kills)
        
        if key == arcade.key.SPACE:
            self.want_jump = True
        
        if key == arcade.key.LSHIFT:
            self.run = True
            MOVEMENT_SPEED_PLAYER = 12
            
    def stop_recognize(self, key):
        global MOVEMENT_SPEED_PLAYER
        
        if key == arcade.key.A:
            self.move_left = False
            
        if key == arcade.key.D:
            self.move_right = False

        if key == arcade.key.SPACE:
            self.want_jump = False
        
        if key == arcade.key.LSHIFT:
            self.run = False
            MOVEMENT_SPEED_PLAYER = 5
    
    def attack(self, enemys, dx, dy):
        if self.attack_cooldown <= 0:
            # self.gif_sprite = arcade.load_animated_gif(engineer_attack+"attack.gif")
            length = math.sqrt(dx**2 + dy**2)

            if length > 0:
                direction = (dx / length, dy / length)

            for enemy in enemys:
                
                distance = math.sqrt(
                    (enemy.center_x - self.center_x)**2 +
                    (enemy.center_y - self.center_y)**2
                )
                if distance < self.attack_range:  
        
                    enemy.attacked(self.damage, self)
    
    def update_animation(self, delta_time):

        moving = self.move_left or self.move_right

        if moving and self.run != True:
            self.walk_sprite.update_animation(delta_time)
            self.texture = self.walk_sprite.texture
        
        if moving and self.run == True:
            self.run_sprite.update_animation(delta_time)
            self.texture = self.run_sprite.texture
    
    def attacked(self, damage):

        if self.cur_health <= 0:
            pass
        
        else:
            self.cur_health -= damage 
    
    def update(self, delta_time):
                
        self.change_x = 0
        
        if self.move_left:
            self.change_x -= MOVEMENT_SPEED_PLAYER
        
        if self.move_right:
            self.change_x += MOVEMENT_SPEED_PLAYER
            
        if self.change_x > 0:
            self.facing_right = True
            
        elif self.change_x < 0:
            self.facing_right = False
            
        self.scale_x = abs(self.scale_x) if self.facing_right else -abs(self.scale_x)
        
        self.update_animation(delta_time)
        
        if self.want_jump and self.on_ground:
            self.change_y = JUMP_FORCE
            self.on_ground = False

        self.change_y -= GRAVITY
        
        super().update() 
        self.on_ground = False
        
        collisions = arcade.check_for_collision_with_list(self, self.wall_list)
        
        for wall in collisions:
            if self.change_y <= 0:
                self.bottom = wall.top
                self.change_y = 0
                self.on_ground = True




