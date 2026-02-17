from ursina import *
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from ursina import mouse
import math

# Настройки
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Diablo-like RPG"

# Замените на свои пути к текстурам
PLAYER_TEXTURE = 'assets/animations/characters/knight/Knight_1/Idle1.png'
ENEMY_TEXTURE = 'assets/animations/characters/knight/Knight_1/Idle1.png'
BOTTLE_TEXTURE = 'assets/textures/inventory/items/skills/poisen.png'
SWORD_TEXTURE = 'assets/textures/inventory/items/swords/sword.png'

class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = 'quad'
        self.texture = PLAYER_TEXTURE
        self.scale = (1, 1)
        self.position = (0, 0, 0)
        self.speed = 5
        self.health = 100
        self.inventory = []
        self.bottle_list = []

    # def input(self, key):
    #     if key == 'w':
    #         self.z += self.speed * time.dt
    #     elif key == 's':
    #         self.z -= self.speed * time.dt
    #     elif key == 'a':
    #         self.x -= self.speed * time.dt
    #     elif key == 'd':
    #         self.x += self.speed * time.dt

    def attack(self, enemies, dx, dy):
        for enemy in enemies:
            dist = distance(self.position, enemy.position)
            if dist < 2:
                enemy.health -= 20
                if enemy.health <= 0:
                    enemy.disable()

    def throw_bottle(self, mouse_pos):
        bottle = Entity(
            model='sphere',
            color=color.amber,
            scale=0.3,
            position=self.position + (0, 1, 0),
            add_to_scene_entities=False
        )
        bottle.direction = mouse_pos - self.position
        bottle.velocity = 10
        bottle.gravity = -5
        bottle.time = 0
        bottle.is_active = True
        self.bottle_list.append(bottle)

class Enemy(Entity):
    def __init__(self, texture, class_type, x, z, player):  # ← добавили player
        super().__init__()
        self.model = 'quad'
        self.texture = texture
        self.scale = (1, 1)
        self.x = x
        self.z = z
        self.y = 0.5
        self.class_type = class_type
        self.health = 50 if class_type == 'melee' else 30
        self.max_health = self.health
        self.health_bar = HealthBar(parent=self, bar_color=color.red)
        # Сохраняем ссылку на игрока
        self.player = player  # ← сохраняем

    def update(self):
        dist = distance(self.position, self.player.position)
        if dist > 2:
            direction = (self.player.position - self.position).normalized()
            self.position += direction * 0.1 * time.dt

class Game():
    def __init__(self):
        super().__init__()
        self.app = Ursina()
        mouse.enabled = True
        window.title = SCREEN_TITLE
        window.borderless = False
        window.exit_button.visible = False
        window.fps_counter.enabled = True

        # Настройка камеры
        camera.rotation = (30, -45, 0)
        camera.position = (0, 20, -10)

        # Игрок
        self.player = Player(texture=PLAYER_TEXTURE)
        self.player.y = 0.5

        # Враги
        self.enemies = []
        for i in range(3):
            class_type = random.choice(['range', 'melee', 'tank'])
            x = random.uniform(-10, 10)
            z = random.uniform(-10, 10)
            enemy = Enemy(ENEMY_TEXTURE, class_type, x, z, self.player)
            self.enemies.append(enemy)

        # Пол
        Entity(
            model='plane',
            texture='white_cube',
            scale=(100),
            color=color.light_gray,
            y=-0.1,
            collider='box'
        )

        # Инвентарь
        self.inventory_items = []
        for i in range(3):
            item = Entity(
                model='cube',
                texture=SWORD_TEXTURE,
                scale=0.2,
                position=(-5 + i * 0.5, 1, -8),
                parent=scene
            )
            self.inventory_items.append(item)

        # Курсор
        self.cursor = Cursor(parent=camera, color=color.cyan)

        # HUD (здоровье)
        self.health_text = Text(
            text=f'HP: {self.player.health}',
            position=(-0.7, 0.4),
            scale=2,
            parent=camera.ui
        )

    def input(self, key):

        if key == 'left mouse down':
            mouse_pos = Vec3(mouse.x, 0, mouse.y)
            self.player.attack(self.enemies, mouse_pos.x, mouse_pos.z)
            print("gugugaga")

        if key == 'right mouse down':
            mouse_pos = Vec3(mouse.x, 0, mouse.y)
            self.player.throw_bottle(mouse_pos)
        else:
            self.player.input(key)

    def update(self):
        # Обновление врагов
        for enemy in self.enemies:
            enemy.update()
            if enemy.health <= 0 and enemy in self.enemies:
                self.enemies.remove(enemy)
                destroy(enemy)

        # Обновление бутылок
        for bottle in self.player.bottle_list:
            if bottle.is_active:
                bottle.time += time.dt
                bottle.y += bottle.velocity * time.dt
                bottle.position += bottle.direction * 0.1 * time.dt
                bottle.y += bottle.gravity * bottle.time * time.dt

                for enemy in self.enemies:
                    if distance(bottle.position, enemy.position) < 1:
                        enemy.health -= 20
                        destroy(bottle)
                        self.player.bottle_list.remove(bottle)
                        break

                if abs(bottle.x) > 20 or abs(bottle.z) > 20:
                    destroy(bottle)
                    self.player.bottle_list.remove(bottle)

        # Камера следит за игроком
        camera.position = self.player.position + Vec3(0, 15, -10)
        camera.look_at(self.player.position)

        # Обновление текста здоровья
        self.health_text.text = f'HP: {int(self.player.health)}'

if __name__ == '__main__':
    game = Game()
    game.app.run()
