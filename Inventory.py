import arcade
from Paths import *

class Item:
    def __init__(self, texture, name: str, max_stack: int = 1):
        self.name = name
        self.texture = texture
        self.max_stack = max_stack
        self.count = 1
        
    def use(self):
        # Метод для использования предмета
        pass

class Inventory:
    def __init__(self, max_slots=10, slot_size=48):
        self.max_slots = max_slots
        self.slot_size = slot_size
        self.slots = [ItemSlot() for _ in range(max_slots)]
        self.visible = True
        self.offset_x = -1 * (SCREEN_WIDTH // 4.95)
        self.offset_y = -1 * (SCREEN_HEIGHT // 2.05)
        
    # -----------------------------------------------------

    def add_item(self, item: Item):
      
        for slot in self.slots:
            if slot.can_stack(item):
                slot.add_item(item)
                return True

        for slot in self.slots:
            if slot.is_empty():
                slot.add_item(item)
                return True

        return False

    # -----------------------------------------------------

    def remove_item(self, index):
        if 0 <= index < self.max_slots:
            return self.slots[index].remove_one()
        return None

    # -----------------------------------------------------

    def draw(self, player_x, player_y):
        if not self.visible:
            return
        
        start_x = player_x + self.offset_x
        start_y = player_y + self.offset_y

        for i, slot in enumerate(self.slots):
            x_d = start_x + i * (self.slot_size + 8)
            y_d = start_y
            w = self.slot_size
            h = self.slot_size
            left = x_d
            right = x_d + w
            bottom = y_d
            top = y_d + h
            
            rect = arcade.Rect(
                x=x_d,
                y=y_d,
                width=w,
                height=h,
                left=left,
                right=right,
                bottom=bottom,
                top=top
            )

            rect_texture = arcade.Rect(
                x=x_d + self.slot_size / 2,
                y=y_d + self.slot_size / 2,
                width=self.slot_size - 8,
                height=self.slot_size - 8,
                left=left,
                right=right,
                bottom=bottom,
                top=top
            )

            arcade.draw_rect_outline(
                rect,
                color=arcade.color.WHITE,
                border_width=2
            )

            if slot.is_empty():
                continue

            item = slot.item
            tex = item.texture

            arcade.draw_texture_rect(tex, rect_texture)

            # Количество
            if item.count > 1:
                arcade.draw_text(
                    str(item.count),
                    x_d + self.slot_size//3,
                    y_d - self.slot_size//2 + 4,
                    arcade.color.WHITE,
                    14,
                    bold=True
                )

class ItemSlot:
    def __init__(self):
        self.item = None

    def is_empty(self):
        return self.item is None

    def can_stack(self, item: Item):
        return (
            self.item and 
            self.item.name == item.name and 
            self.item.count < self.item.max_stack
        )

    def add_item(self, item: Item):
   
        if self.is_empty():
            self.item = item
            return True

        if self.can_stack(item):
            self.item.count += 1
            return True

        return False

    def remove_one(self):

        if self.is_empty():
            return None

        removed = Item(self.item.name, "")  
        removed.texture = self.item.texture
        removed.count = 1

        self.item.count -= 1
        if self.item.count <= 0:
            self.item = None

        return removed
    