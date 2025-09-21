from ursina import *

class Enemy(Entity):
    def __init__(self, position, speed, texture, model):
        super().__init__(
            model=model,
            texture='Assets/Enemys/'+texture,
            collider='box',
            y = 0.3
            
        )
        self.speed = speed

    def follow(self, player_pos):
        direction_to_player = Vec3(player_pos.x - self.x, 0, player_pos.z - self.z)
        distance = math.sqrt(direction_to_player.x ** 2 + direction_to_player.z ** 2)
        if distance > 0:
            move_vector = direction_to_player.normalized() * self.speed * time.dt
            self.position += move_vector

    def attack(self, player):
        dist = distance(player.position, self.position)
        if dist < 1 and player.enabled:
            player.take_damage()

    def take_damage(self, player):
        dist = distance(player.magic_circle_fire.position, self.position)
        if dist <= 2:
            self.disable()
            self.x = 99999999999999
            print('Baba galya KILLED')