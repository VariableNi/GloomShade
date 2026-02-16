import arcade
from Paths import *

class HealthBar:
    def __init__(
        self,
        entity,
        scale,                   
        height=10,              
        width=100,                        
        padding=1,              
        fg_color=arcade.color.RED,
        border_color=arcade.color.BLACK,
                 
    ):
        
        self.entity = entity
        self.height = int(height * scale)
        
        if self.entity.type == 'player':
            self.offset_y = int(-1 * (SCREEN_HEIGHT * 0.416))
            self.width = int(SCREEN_WIDTH*0.4143)
        
        else:
            self.offset_y = (self.entity.height - height*2)
            self.width = int(width * scale)

        self.padding = padding * scale
        self.fg_color = fg_color
        self.border_color = border_color

    def draw(self):

        score_hp = (self.entity.cur_health / self.entity.max_health) * 100

        if score_hp <= 70 and score_hp > 30:
            self.fg_color = arcade.color.YELLOW_ORANGE

        elif score_hp <= 30:
            self.fg_color = arcade.color.RED

        else:
            self.fg_color = arcade.color.GREEN_YELLOW
    
        center_x = self.entity.center_x
        center_y = self.entity.center_y + self.offset_y + 20

        bottom = center_y - self.height // 2
        top = center_y + self.height // 2

        inner_bottom = bottom + self.padding
        inner_top = top - self.padding

        health_ratio = max(0, self.entity.cur_health / self.entity.max_health)
        health_width = int(self.width * health_ratio)
        new_left = center_x - health_width // 2
        new_right = center_x + health_width // 2

        if self.entity.type == 'player':
            arcade.draw_lrbt_rectangle_filled(
                new_left, new_right, inner_bottom, inner_top, self.fg_color
            )

            arcade.draw_text(
                    str(self.entity.cur_health),
                    center_x,
                    inner_bottom,
                    arcade.color.WHITE,
                    15,
                    bold=True
                )
        else:
            if self.entity.cur_health < self.entity.max_health:
        
                arcade.draw_lrbt_rectangle_filled(
                    new_left, new_right, inner_bottom, inner_top, self.fg_color

                )
