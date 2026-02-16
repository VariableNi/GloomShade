from PlayerBase import *
import arcade
from main_assets import *
from Health_bar import HealthBar
from Inventory import Inventory
import math

class Knight(PlayerBase):

    def __init__(self, wall_list):
        super().__init__(wall_list)
        self.texture = arcade.load_texture(KNIGHT_TEXTURE)

        self.damage = 15
        self.attack_range = 80
        self.counter_kills = 0
        self.attack_cooldown = 0
        self.attack_duration = 1000

        # self.walk_anim = EngineerWalk()
        # self.run_anim = EngineerRun()
        
        self.walk_anim = WALK_SPRITE
        self.run_anim = RUN_SPRITE
        self.idle_anim = IDLE_SPRITE
        self.attack_anim = ATTACK_SPRITE
        self.throwing = False
        self.bottle_list = arcade.SpriteList()

    def update_animation(self, delta_time):
        moving = self.move_left or self.move_right
        attack = self.attacking
        
        if attack:
        # Играем анимацию атаки
            self.attack_anim.update_animation(delta_time)
            self.texture = self.attack_anim.texture

            # Уменьшаем cooldown и проверяем завершение атаки
            self.attack_cooldown -= 1
            if self.attack_cooldown <= 0:
                self.attacking = False  # атака закончилась

        elif moving:
            # Ходьба/бег
            anim = self.run_anim if self.run else self.walk_anim
            anim.update_animation(delta_time)
            self.texture = anim.texture

        else:
            # Простои
            self.idle_anim.update_animation(delta_time)
            self.texture = self.idle_anim.texture

    def attack(self, enemies, dx, dy):
        if self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_cooldown = self.attack_duration 

            for enemy in enemies:
                if arcade.get_distance_between_sprites(self, enemy) < self.attack_range:
                    enemy.attacked(self.damage, self)
                    
            self.attack_cooldown = 30

    def throw_bottle(self):
        if self.throwing:
            return

        self.throwing = True

        start_x = self.center_x
        start_y = self.center_y
        velocity = 700 # начальная скорость

        # Создаём бутылку с учётом стороны броска
        if self.facing_right:
            bottle = Bottle(start_x + 1, start_y, velocity)  # бросок вправо
        else:
            bottle = Bottle(start_x - 1, start_y, velocity)  # бросок влево
            bottle.vx *= -1  # инвертируем горизонтальную скорость

        self.bottle_list.append(bottle)
        arcade.schedule(self.reset_throw, 1.0)

    def reset_throw(self, _):
        self.throwing = False

class Bottle(arcade.Sprite):
    def __init__(self, start_x, start_y, velocity):
        super().__init__(BOTTLE_TEXTURE, scale=0.1)
        self.center_x = start_x
        self.center_y = start_y
        self.velocity = velocity
        self.gravity = -20  # гравитация (можно уменьшить для игры)
        self.time = 0.3
        self.is_active = True
        FIXED_ANGLE_DEGREES = 30 # угол броска (можно подобрать)
        FIXED_ANGLE_RADIANS = math.radians(FIXED_ANGLE_DEGREES)
        
        # Фиксированные компоненты скорости (рассчитываются сразу)
        self.vx = velocity * math.cos(FIXED_ANGLE_RADIANS)
        self.vy = velocity * math.sin(FIXED_ANGLE_RADIANS)


    def update(self, delta_time):
        self.time += delta_time
        self.center_x += self.vx * delta_time
        self.center_y += (self.vy * delta_time + 0.5 * self.gravity * self.time**2)

        # Проверка на столкновение с землёй
        if self.center_y < 50:
            self.explode()  # остановка или взрыв

    def explode(self):
        self.is_active = False
        self.kill()  # удаляем из списка спрайтов





            