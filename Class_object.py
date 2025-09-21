from ursina import *
import ursina

class Object(Entity):
    
    def __init__(self, position: Vec3, model: str, texture: str):
        super().__init__(
            position=position,
            model=model,
            texture = texture,
            collider='box',
            scale=0.3
        )
    
    def gravity(self):
        
        if self.y >= 0.3:
            self.y -= 0.1 + time.dt
            
    def update(self):
        self.gravity()

class Other_player(ursina.Entity):
    def __init__(self, position: ursina.Vec3, identifier: str, username: str, model: str, texture: str):
        super().__init__(
            position=position,
            model=model,
            origin_y=-0.5,
            collider="box",
            texture=texture,
            color=ursina.color.color(0, 0, 1),
            scale=0.5
        )

        self.name_tag = ursina.Text(
            parent=self,
            text=username,
            position=ursina.Vec3(0, 1.3, 0),
            scale=ursina.Vec2(5, 3),
            billboard=True,
            origin=ursina.Vec2(0, 0)
        )

        self.health = 100
        self.id = identifier
        self.username = username
        
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
                    
    def spell_magic_circle(self, floor_, status, mouse_pos, camera_pos):
        if status != 1:
            
            if mouse_pos.world_point != None:
                hit = raycast(camera_pos.world_position, mouse_pos.world_point - camera_pos.world_position, distance=100, ignore=[self])
            
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
                        
            
            else:
                pass
        
