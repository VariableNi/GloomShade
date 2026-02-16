import arcade
from Player import Player
from Enemy import Enemy
from Health_bar import HealthBar
from random import randint
from Inventory import *
import math
from Paths import *
from main_assets import *
from Knight_class import *
from ParallaxLayers import *

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

        #player -----------------------------------     
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        # self.player = Player(ENGINEER_TEXTURE, self.wall_list)
        self.player = Knight(self.wall_list)
        # self.player.invetory.add_item(sword)
        # self.player.invetory.add_item(sword2)
        # self.player.invetory.add_item(sword3)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.attack_direction = (0, 0)
        self.attacking = False

        self.camera = arcade.Camera2D()
        self.ui_camera = arcade.Camera2D()
        self.set_mouse_visible(False)
        
        #floor------------------------------------
        
        floor = arcade.SpriteSolidColor(
        width=5000,
        height=40,
        color=arcade.color.WHITE
                    )
        floor.center_x = 2500
        floor.center_y = 20
        
        floor1 = arcade.SpriteSolidColor(
        width=5000,
        height=40,
        color=arcade.color.WHITE
                    )
        floor1.center_x = 200
        floor1.center_y = 0
        self.wall_list.append(floor)
        self.wall_list.append(floor1)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
        self.player,
        self.wall_list,
        gravity_constant=GRAVITY
        )

        #enemy------------------------------------

        self.enemy_list = arcade.SpriteList()
        max_enemys = 3
        ranger_enemys = []

        for i in range (0, max_enemys):

            class_enemy = ['range', 'melee', 'tank']

            class_enemy = class_enemy[randint(0, 2)]
            
            enemy = Enemy(KNIGHT_TEXTURE, class_enemy, randint(0, 1000), self.wall_list)
            enemy.setup_ai(self.player_list, ranger_enemys)
            self.enemy_list.append(enemy) 

            if class_enemy == 'range':
                ranger_enemys.append(enemy)
        
        #items-------------------------------------
        sword = Item(
            name="Меч",
            texture=SWORD_TEXTURE,
            max_stack=10
        )

        sword2 = Item(
            name="Меч2",
            texture=SWORD_TEXTURE,
            max_stack=10
        )

        sword3 = Item(
            name="Меч3",
            texture=SWORD_TEXTURE,
            max_stack=10
        )

        #game--------------------------------------
        self.background = ParallaxBackground()

        self.background.add_layer(
            ParallaxLayer(BACKGROUND_sky, 0.12, y=SCREEN_HEIGHT * 0.6)
        )
        self.background.add_layer(
            ParallaxLayer(BACKGROUND_mountains, 0.25, y=SCREEN_HEIGHT * 0.35)
        )
        self.background.add_layer(
            ParallaxLayer(BACKGROUND_forest, 0.5, y=SCREEN_HEIGHT * 0.25)
        )
       
        arcade.schedule(self.update, 1/60)
    
    def screen_to_world(self, x, y):
        return (
            x + self.camera.position[0] - self.width / 2,
            y + self.camera.position[1] - self.height / 2
        )
    
    def on_mouse_motion(self, x, y, dx, dy):
        self._mouse_x = x
        self._mouse_y = y

        world_x, world_y = self.screen_to_world(x, y)

        dx = world_x - self.player.center_x
        dy = world_y - self.player.center_y

        angle = math.degrees(math.atan2(dy, dx))
        #self.player.angle = angle

    def on_mouse_press(self, x, y, button, modifiers):
        
        if button == arcade.MOUSE_BUTTON_LEFT:

            world_x, world_y = self.screen_to_world(x, y)

            dx = world_x - self.player.center_x
            dy = world_y - self.player.center_y

            self.attack_direction = (dx, dy)
            self.attacking = True
            self.player.attack(self.enemy_list, dx, dy)

        if button == arcade.MOUSE_BUTTON_RIGHT:
            
            self.player.throw_bottle()
            
    def on_key_press(self, key, modifiers):

        self.player.regonizer_key(key)
           
    def on_key_release(self, key, modifiers):
        
        self.player.stop_recognize(key)
    
    def on_draw(self):
        self.clear()
        
        self.camera.use()
        self.background.draw()
        self.wall_list.draw()
        self.player_list.draw() 
        self.enemy_list.draw()
        self.player.bottle_list.draw()

        for enemy in self.enemy_list:
            enemy.health_bar.draw()
            enemy.draw()

        self.player.invetory.draw(self.player.position[0],
                                    self.player.position[1])
        self.player.health_bar.draw()
        
        self.ui_camera.use()
        mouse_x, mouse_y = self._mouse_x, self._mouse_y

        arcade.draw_circle_outline(
            mouse_x,
            mouse_y,
            10, 
            arcade.color.WHITE
        )
        
        arcade.draw_circle_filled(
            mouse_x, 
            mouse_y, 
            3, 
            arcade.color.WHITE
        )
        self.camera.use()

    def update(self, delta_time):
        
        self.player_list.update()
        self.enemy_list.update()
                
        self.physics_engine.update()
        self.player.bottle_list.update()  

        for bottle in self.player.bottle_list:
            if bottle.is_active:
       
                hit_list = arcade.check_for_collision_with_list(bottle, self.enemy_list)
                for enemy in hit_list:
                    enemy.attacked(20, self.player)  # урон от взрыва
                    bottle.explode()

        self.camera.position = (self.player.center_x, self.player.center_y)
        
        self.background.update(self.camera.position[0])


if __name__ == "__main__":
    game = Game()
    arcade.run()