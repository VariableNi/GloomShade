import arcade
from Paths import *

class EnemyAI:
    def __init__(self, players, vision_range=100):
        self.players = players  
        self.target = None
        self.attack_cooldown = 0
        self.vision_range = vision_range
         
    def update(self, enemy):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if not self.target or not self.check_target_validity(enemy):
            self.target = self.find_closest_target(enemy)
            
        if self.target:
            distance_squared = self.calculate_distance(enemy, self.target)
            self.handle_target(enemy, distance_squared)
        
    def find_closest_target(self, enemy):
        closest_target = None
        closest_distance = float('inf')
        
        for player in self.players:
            distance_squared = self.calculate_distance(enemy, player)
            if distance_squared < closest_distance:
                closest_distance = distance_squared
                closest_target = player
                
        return closest_target
    
    def calculate_distance(self, entity1, entity2):
        dx = entity1.center_x - entity2.center_x
        dy = entity1.center_y - entity2.center_y
        return dx**2 + dy**2
    
    def check_target_validity(self, enemy):
        return self.target is not None and \
               self.calculate_distance(enemy, self.target) <= self.vision_range**2

    def move_towards_target(self, enemy, target):
        
        dx = target.center_x - enemy.center_x
        dy = target.center_y - enemy.center_y
        distance = (dx**2 + dy**2)**0.5
        
        if distance == 0:
            enemy.change_x = 0
            enemy.change_y = 0
            return

        dx /= distance
        dy /= distance
        
        speed = MOVEMENT_SPEED
        
        enemy.change_x = dx * speed
        # enemy.change_y = dy * speed

    def attack(self, enemy):
        if self.attack_cooldown == 0:
            if self.target:
                self.target.attacked(enemy.damage)
                self.attack_cooldown = 100
        else:
            self.attack_cooldown -= 1

class MeleeEnemyAI(EnemyAI):
    def __init__(self, players, attack_range=100):
        super().__init__(players)
        self.attack_range = attack_range

    def handle_target(self, enemy, distance_squared):

        max_distance = self.vision_range**2
        vision_range = max_distance * 20
        
        if distance_squared <= max_distance:
               
            if enemy.change_x == 0 and enemy.change_y == 0:

                if self.attack_cooldown == 0:

                    self.attack(enemy)
                    self.attack_cooldown = 100

                else:
                    self.attack_cooldown -= 1
                    
            else:
                    
                enemy.change_x = 0
                enemy.change_y = 0
        else:
       
            if distance_squared <= vision_range:
                self.move_towards_target(enemy, self.target)
            
            elif distance_squared > vision_range:
                enemy.change_x = 0
                enemy.change_y = 0

class RangeEnemyAI(EnemyAI):
    def __init__(self, players, attack_range=400, shoot_cooldown=5):
        super().__init__(players)
        self.attack_range = attack_range
        self.shoot_cooldown = shoot_cooldown

    def handle_target(self, enemy, distance_squared):

        min_distance = enemy.melee_range**2
        max_distance = self.attack_range**2
        vision_range = max_distance * 3
        
        if distance_squared <= max_distance:
            if distance_squared < min_distance:
               
                self.move_away_from_target(enemy, self.target)
            else:
               
                if enemy.change_x == 0 and enemy.change_y == 0:

                    if self.shoot_cooldown == 0:
                        self.attack(enemy)
                        self.shoot_cooldown = 100

                    else:
                        self.shoot_cooldown -= 1
                    
                else:
                    
                    enemy.change_x = 0
                    enemy.change_y = 0
        else:
       
            if distance_squared <= vision_range:
                self.move_towards_target(enemy, self.target)
            
            elif distance_squared > vision_range:
                enemy.change_x = 0
                enemy.change_y = 0

    def move_away_from_target(self, enemy, target):
    
        dx = enemy.center_x - target.center_x
        dy = enemy.center_y - target.center_y
        distance = (dx**2 + dy**2)**0.5
        
        if distance == 0:
            enemy.change_x = 0
            enemy.change_y = 0
            return
        
        dx /= distance
        dy /= distance
        
        speed = MOVEMENT_SPEED
        
        enemy.change_x = dx * speed
        # enemy.change_y = dy * speed

class TankEnemyAI(EnemyAI):
    def __init__(self, players, ranged_enemies, protection_distance=TANK_PROTECTION_DISTANCE):
        super().__init__(players)
        self.ranged_enemies = ranged_enemies  # список ranged-врагов, которых надо прикрывать
        self.protection_distance = protection_distance

    def handle_target(self, enemy, distance_squared):
        if not self.target:
            return

        # 1. Находим «фронтальную» точку: перед ranged-врагами по направлению к цели
        front_position = self.calculate_front_position(enemy)

        # 2. Двигаемся в эту точку
        self.move_towards_position(enemy, front_position)

        # 3. Атакуем, если цель близко
        if distance_squared <= self.vision_range**2:
            self.attack(enemy)

    def calculate_front_position(self, tank):
        """
        Вычисляет позицию перед ranged-врагами по направлению к текущей цели.
        """
        if not self.ranged_enemies or not self.target:
            return (tank.center_x, tank.center_y)

        # Находим центр масс ranged-врагов
        total_x = 0
        total_y = 0
        count = 0
        for re in self.ranged_enemies:
        
            total_x += re.center_x
            total_y += re.center_y
            count += 1

        if count == 0:
            return (tank.center_x, tank.center_y)

        center_x = total_x / count
        center_y = total_y / count

        # Вектор от центра ranged-врагов к цели
        dx = self.target.center_x - center_x
        dy = self.target.center_y - center_y
        distance = (dx**2 + dy**2)**0.5

        if distance == 0:
            return (center_x)

        # Нормализуем вектор
        dx /= distance
        dy /= distance

        # Позиция перед ranged-врагами на расстоянии `protection_distance`
        front_x = center_x + dx * self.protection_distance
        front_y = center_y + dy * self.protection_distance

        return (front_x, front_y)

    def move_towards_position(self, enemy, position):
       
        target_x, target_y = position
        dx = target_x - enemy.center_x
        dy = target_y - enemy.center_y
        distance = (dx**2 + dy**2)**0.5

        if distance == 0:
            enemy.change_x = 0
            enemy.change_y = 0
            return

        # Нормализуем вектор движения
        dx /= distance
        dy /= distance

        speed = MOVEMENT_SPEED
        enemy.change_x = dx * speed
        #enemy.change_y = dy * speed
