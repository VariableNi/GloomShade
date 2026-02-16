import arcade
from Health_bar import HealthBar
import os
from EnemyAI import *
from Paths import *
from main_assets import *

class Enemy(arcade.Sprite):
    def __init__(self, filename, class_enemy, center_x, wall_list):
        
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден")
        
        super().__init__(filename, scale=1)
        self.center_x = center_x
        self.center_y = SCREEN_HEIGHT // 2
        self.attack_range = 64  
        self.damage = 5
        self.max_health = 100
        self.cur_health = 100
        self.type = 'enemy'
        self.health_bar = HealthBar(self, self.scale[0]*2)
        self.target = None
        self.attack_cooldown = 0
        self.vision_range = 100
        self.ai = None
        self.change_x = 0
        self.change_y = 0
        self.melee_range = 360
        self.class_enemy = class_enemy
        self.players = None
        self.walk_sprite = WALK_SPRITE
        self.on_ground = False
        self.move_left = False
        self.move_right = False
        self.facing_right = True
        self.wall_list = wall_list

    def setup_ai(self, players, rangers):
        
        if self.class_enemy == 'range':
            self.ai = RangeEnemyAI(players)
        
        elif self.class_enemy == 'tank':
           self.ai = TankEnemyAI(players, rangers)
        
        else:
            self.ai = MeleeEnemyAI(players) 
        
        self.players = players
    
    def attacked(self, damage, id_player):

        if self.cur_health <= 0:
            self.cur_health = 0
            self.kill()
            id_player.counter_kills += 1
        
        else:
            self.cur_health -= damage
    
    def draw(self):

        arcade.draw_text(
                    str(self.class_enemy),
                    self.center_x,
                    self.center_y,
                    arcade.color.RED,
                    14,
                    bold=True
                )
    
    def update_animation(self, delta_time):

        if self.change_x != 0 or self.change_y != 0:
            self.walk_sprite.update_animation(delta_time)
            self.texture = self.walk_sprite.texture


    def update(self, delta_time):
        
        if self.change_x > 0:
            self.facing_right = True
            
        elif self.change_x < 0:
            self.facing_right = False
            
        self.scale_x = -abs(self.scale_x) if self.facing_right else abs(self.scale_x)

        self.update_animation(delta_time)
        
        self.change_y -= GRAVITY
        
        super().update()
        
        collisions = arcade.check_for_collision_with_list(self, self.wall_list)
        
        for wall in collisions:
            if self.change_y <= 0:
                self.bottom = wall.top
                self.change_y = 0
                self.on_ground = True

        if self.ai:
            self.ai.update(self)

