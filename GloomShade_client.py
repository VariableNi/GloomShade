from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from Class_Player import Player
from Class_Inventory import Inventory, Status_window
from Class_Enemy import Enemy
from Class_object import *
from network import Network

import threading
import socket
import os
import sys

#global_varibles
HIDE_SWORD = 0
STATUS_INVENTORY = 0
LIST_ENEMY = []
LIST_EVENTS = []
username = input("Enter your username: ")

    
while True:
    server_addr = '26.234.87.24'
    server_port = '5000'

    try:
        server_port = int(server_port)
    except ValueError:
        print("\nThe port you entered was not a number, try again with a valid port...")
        continue

    n = Network(server_addr, server_port, username)
    n.settimeout(5)

    error_occurred = False

    try:
        n.connect()
    except ConnectionRefusedError:
        print("\nConnection refused! This can be because server hasn't started or has reached it's player limit.")
        error_occurred = True
    except socket.timeout:
        print("\nServer took too long to respond, please try again...")
        error_occurred = True
    except socket.gaierror:
        print("\nThe IP address you entered is invalid, please try again with a valid address...")
        error_occurred = True
    finally:
        n.settimeout(None)

    if not error_occurred:
        break

def receive():
    while True:
        try:
            info = n.receive_info()
        except Exception as e:
            print(e)
            continue

        if not info:
            print("Server has stopped! Exiting...")
            sys.exit()
        
        if info["object"] == "player":
            player_id = info["id"]

            if info["joined"]:
                new_player = Other_player(ursina.Vec3(*info["position"]), player_id, info["username"], info["model"], info["texture"])
                other_players.append(new_player)
                continue

            player = None

            for p in other_players:
                if p.id == player_id:
                    player = p
                    break

            if not player:
                continue

            if info["left"]:
                other_players.remove(player)
                ursina.destroy(player)
                continue

            player.world_position = ursina.Vec3(*info["position"])
            player.rotation_y = info["rotation"]
        
        elif info["object"] == "spell":
            LIST_EVENTS.append(info["mouse"], info["camera"])

def input(key):
    global STATUS_INVENTORY, LIST_ENEMY, HIDE_SWORD

    if key == 'i':
        
        if STATUS_INVENTORY == 0:
            inventory.enable()
            status_window.enable()
            STATUS_INVENTORY = 1
            player.on_disable()
            player.rotation_y += 180
    
        elif STATUS_INVENTORY == 1:
            inventory.disable()
            status_window.disable()
            STATUS_INVENTORY = 0
            player.on_enable()
            player.rotation_y -= 180
    
    # if key == 'left mouse down':
    #     if mouse.x > -0.26 and mouse.x <= 0.235 and mouse.y < -0.01 and mouse.y >= -0.28:
    #             print("Yeah, its work")
           
                
    elif key == ']':
        
        test_enemy = Enemy((0, 0, 0), 5, 'BabaGalya/Galya', 'cube')
        LIST_ENEMY.append(test_enemy)
        # error_message = Text('<red>Баба Галя нападает', origin=(-1,-5.5), x=-.5, scale=2)
        # sound.play()
    
    elif key == 'left mouse down':
        player.spell_magic_circle(floor_, STATUS_INVENTORY)
        
        try:
            n.send_spell(mouse, camera)
        
        except Exception as e:
            pass
    
    elif key == 'e':
        player.hide_swords(HIDE_SWORD)
        
        if HIDE_SWORD == 0:
            HIDE_SWORD = 1
        else:
            HIDE_SWORD = 0
        
    elif key == 'scroll up':
        if camera.z < 0:
            camera.z += 0.5
            
    elif key == 'scroll down':
        if camera.z > -10:
            camera.z -= 0.5
        
def update():
    global prev_pos, prev_dir, LIST_EVENTS
    for enemy in LIST_ENEMY:
        enemy.follow(player.position)
        enemy.attack(player)
        enemy.take_damage(player)
        
    player.dead()
    player.animate_magic_circle()
    
    if prev_pos != player.world_position or prev_dir != player.world_rotation_y:
            n.send_player(player)
    
    prev_pos = player.world_position
    prev_dir = player.world_rotation_y
    
    if LIST_EVENTS != []:
        print(LIST_EVENTS)
        other_players[0].spell_magic_circle(floor_, STATUS_INVENTORY, LIST_EVENTS[0], LIST_EVENTS[1])
        player.animate_magic_circle()
        LIST_EVENTS = []
        
app = Ursina()
window.borderless = False
window.title = "GloomShade"
window.exit_button.visible = False 
window.cog_button.visible = False
window.cog_menu.visible = False

floor_ = Entity(model='plane', texture='grass', scale=123, collider='box', position=(0,0,0))
sky = Sky()
player = Player((10, 9, 5), "hammer", "good", [False], 2)
inventory = Inventory()
status_window = Status_window()
other_players = []
prev_pos = player.world_position
prev_dir = player.world_rotation_y

# sound = Audio(  
#     sound_file_name='Assets/Enemys/BabaGalya/sound.mp3',  # Поиск в папке assets  
#     volume=1,  # Полный объём  
#     loop=False,  # Не повторять  
#     autoplay=False,  # Играть немедленно  
# )

inventory.disable()  
inventory.append(['weapons', 'magic', '001'])

status_window.disable()
camera.z = -10

def main():
    msg_thread = threading.Thread(target=receive, daemon=True)
    msg_thread.start()
    app.run()

if __name__ == "__main__":
    main()