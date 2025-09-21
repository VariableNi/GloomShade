from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from math import *

class Player(FirstPersonController):
    
    def __init__(self, position: Vec3, character_class: str, safe_load: list, armor: list, hands: int):
        super().__init__(
            position=position,
            model= "Assets/obj/"+character_class,
            jump_height=2,
            texture = "Assets/textures/"+character_class,
            jump_duration=10,
            collider="box",
            speed=7,
            scale=0.5
        )

        self.player_health = 100
        self.player_mana = 100
        self.hands = hands
        self.spell = 0
        self.magic_spell_time_start = 0

        if hands >= 1 and hands <= 2:
            if hands == 1:
                self.right_hand = Entity(parent=self,model='sword',texture='sword_texture', scale=0.5, position=(0.4,0.5,0.5))
            elif hands == 2:
                self.right_hand = Entity(parent=self,model='sword',texture='sword_texture', scale=0.7, position=(0.4,0.5,0.5))
                self.left_hand = Entity(parent=self,model='sword',texture='sword_texture', scale=0.7, position=(-0.4,0.5,0.5))

        self.health_bar_red = Entity(
            model='quad',
            scale=(0.7, 0.05),
            color=color.gray,
            position=(0, 0.45, 0),
            parent=camera.ui
        )
        
        self.health_bar = Entity(
            model='quad',
            scale=(0.7, 0.05),
            color=color.red,
            position=(0, 0.45, 0),
            parent=camera.ui
        )

        self.mana_bar_gray = Entity(
            model='quad',
            scale=(0.7, 0.005),
            color=color.gray,
            position=(0, 0.42, 0),
            parent=camera.ui
        )
        
        self.mana_bar = Entity(
            model='quad',
            scale=(0.7, 0.005),
            color=color.blue,
            position=(0, 0.42, 0),
            parent=camera.ui
        )

        self.magic_circle = Entity(
            model='plane',
            texture='magic_circle',
            position=(0,-999,0),
            scale=(0,0,0)
        )
        self.magic_circle.disable()
        
        self.magic_circle_fire = Entity(
            model='cube',
            texture='fire',
            position=(0,-999,0),
            scale=(0,0,0)
        )
        self.magic_circle_fire.disable()
        
    def dis_all(self):
        self.disable()
        self.health_bar_red.disable()
        self.health_bar.disable()
        self.mana_bar.disable()
        self.mana_bar_gray.disable()
        
    def take_damage(self):
        self.player_health -= 10
        self.update_hp()
        self.x += 3
        if self.player_health <= 0:
            self.dis_all()
        
    def update_hp(self):
        self.health_bar.scale_x = (self.player_health / 100) * 0.7
        self.health_bar.x = -0.7/2 + (self.health_bar.scale_x / 2)
        
    def update_mana(self):
        if self.player_mana != 0 and self.spell != 1:
            self.magic_spell_time_start = time.time()
            self.mana_bar.scale_x = (self.player_mana / 100) * 0.7
            self.mana_bar.x = -0.7/2 + (self.mana_bar.scale_x / 2)
            
    def animate_magic_circle(self):
        if self.spell == 1:
            self.magic_spell_time_end = time.time() - self.magic_spell_time_start
            
            if self.magic_spell_time_end < 3:
                if self.magic_circle.scale != (2,2,2):
                    self.magic_circle.scale = lerp(self.magic_circle.scale, (7,0,7), time.dt * 4)
                    self.magic_circle_fire.scale = lerp(self.magic_circle_fire.scale, (6.5,6.5,0), time.dt * 4)
                    
            elif self.magic_spell_time_end > 3:
                self.magic_circle_fire.position=(999,999,999)
                self.magic_circle.scale = lerp(self.magic_circle.scale, (0,0,0), time.dt * 4)
                self.magic_circle_fire.scale = lerp(self.magic_circle_fire.scale, (0,0,0), time.dt * 4)
                
                if self.magic_circle.scale <= (0.001,0.001,0.001) and self.magic_spell_time_end > 3:
                    self.magic_circle.disable()
                    self.magic_circle_fire.disable()
                    self.spell = 0
                
    def spell_magic_circle(self, floor_, status):
        if status != 1:
            
            if mouse.world_point != None:
                hit = raycast(camera.world_position, mouse.world_point - camera.world_position, distance=100, ignore=[self])
            
                if hit.hit and hit.entity == floor_ and self.spell != 1:
                    if hasattr(self, 'magic_circle'):
                        self.magic_circle.position = hit.world_point
                        self.magic_circle_fire.position = hit.world_point
                        self.magic_circle.enable()
                        self.magic_circle_fire.enable()
                        
                    else:
                        self.magic_circle = Entity(
                            model='plane',
                            texture='magic_circle',
                            position=hit.world_point
                        )
                        self.magic_circle_fire = Entity(
                        model='cube',
                        texture='fire',
                        position=hit.world_point
                        )
                        
                    self.player_mana -= 10
                    self.update_mana()
                    self.spell = 1
            
            else:
                pass
    
    def hide_swords(self,hide):
        if hide == 0:
            if self.hands == 2:
                self.left_hand.position = (0,0.5,-0.2)
                self.left_hand.rotation_x = 90
                self.left_hand.rotation_y = 90
                self.left_hand.rotation_x = 45
            
            self.right_hand.position = (0,0.5,-0.2)
            self.right_hand.rotation_x = 90
            self.right_hand.rotation_y = 90
            self.right_hand.rotation_x = -225
        
        elif hide == 1:
            if self.hands == 2:
                self.left_hand.position = (-0.4,0.5,0.5)
                self.left_hand.rotation_x = 0
                self.left_hand.rotation_y = 0
                self.left_hand.rotation_x = 0
            
            self.right_hand.position = (0.4,0.5,0.5)
            self.right_hand.rotation_x = 0
            self.right_hand.rotation_y = 0
            self.right_hand.rotation_x = 0
            
        
    def dead(self):
        if self.y <= -10:
            self.position = (0,0,0)
            self.player_health -= 100
            self.take_damage()
    