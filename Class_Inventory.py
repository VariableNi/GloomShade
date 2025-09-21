from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from Class_object import Object
import Data

class Inventory(Entity):
    def __init__(self, width=5, height=8):
        super().__init__(
            parent = camera.ui,
            model=Quad(radius=.015),
            scale = (0.5, 0.8),
            origin = (-0.5, 0.5),
            position = (0.38, 0.47),
            texture = 'white_cube',
            texture_scale = (width, height),
            color = color.dark_gray
        )
        
        self.width = width
        self.height = height
        self.item_parent = Entity(parent=self, scale=(1/5, 1/8))
        
        # for key, value in kwargs.items():
        #     setattr(self, key, value)
    
    def find_free_spot(self):
        
        for y in range(self.height):
            for x in range(self.width):
                grid_positions = [(int(child.x*self.texture_scale[0]), int(child.y*self.texture_scale[1])) for child in self.children]
                
                if not (x, -y) in grid_positions:
                    return x, y
        
    def append(self, item):
        
            x, y = self.find_free_spot()
        
            icon = Draggable(
                   parent=self,
                   model='quad',
                   texture = 'Assets/'+item[0]+'/'+item[1]+'/'+item[2]+'/'+item[2],
                   origin=(-0.5, 0.5),
                   scale_x = 1/self.texture_scale[0],
                   scale_y = 1/self.texture_scale[1],
                   color= color.random_color(),
                   x = x * 1/self.texture_scale[0],
                   y = -y * 1/self.texture_scale[1],
                   z = -1)
            
            if item[0] == "weapons":
                info_of_item = (Data.weapon[item[1]])[item[2]]
                name = info_of_item[0].replace('_', '').title()
                icon.tooltip = Tooltip(name+"\n"+item[0]+"\n"+info_of_item[1]+"\nAttack: "+
                                       str(info_of_item[2])+"\nMana: "+
                                       str(info_of_item[3]))
                icon.tooltip.background.color = color.hsv(0, 0, 0, 0.8)
            
            def drop_item():
                trash = Object((camera.x+1.5, camera.y+2, camera.z+0.5), 'Assets/'+
                               item[0]+'/'+item[1]+
                               '/'+item[2]+'/'+item[2], 
                               'Assets/'+item[0]+'/'+
                               item[1]+'/'+item[2]+'/'+item[2])
            
            def wear():
                pass
                
            def drag():
                icon.org_pos = (icon.x, icon.y)
                icon.z = -1
                
            def drop():
                icon.x = int((icon.x + (icon.scale_x / 2)) * self.width) / self.width
                icon.y = int((icon.y - (icon.scale_y / 2)) * self.height) / self.height
                icon.z = -1
    
                if icon.x < 0 or icon.x >= 1 or icon.y > 0 or icon.y <= -1:
                    
                    if icon.x > -1.2 and icon.x < -0.2 and icon.y < -0.5 and icon.y > -0.87:
                        print("Yeah, its work")
                        icon.tooltip.background.color = color.hsv(1, 2, 0, 0.2)
                    
                    else:
                        icon.position = (icon.org_pos)
                        icon.enabled = False
                        drop_item()
                        return
                
                for c in self.children:
                    if c == icon:
                        continue
                    
                    if c.x == icon.x and c.y == icon.y:
                        c.position = icon.org_pos
                        
            icon.drag = drag
            icon.drop = drop
            
class Status_window(Entity):
    def __init__(self, width=5, height=8, **kwargs):
        super().__init__(
            parent = camera.ui,
            model='cube',
            scale = (0.5, 0.8),
            origin = (-0.5, 0.5),
            position = (-0.88, 0.47),
            texture = 'white_cube',
            
            color = color.dark_gray
        )