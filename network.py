import socket
import json

from Class_Player import Player

class Network:
    
    def __init__(self, server_addr: str, server_port: int, username: str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = server_addr
        self.port = server_port
        self.username = username
        self.recv_size = 2048
        self.id = 0
    
    def settimeout(self, value):
        self.client.settimeout(value)

    def connect(self):

        self.client.connect((self.addr, self.port))
        self.id = self.client.recv(self.recv_size).decode("utf8")
        self.client.send(self.username.encode("utf8"))

    def receive_info(self):
        try:
            msg = self.client.recv(self.recv_size)
        except socket.error as e:
            print(e)

        if not msg:
            return None

        msg_decoded = msg.decode("utf8")

        left_bracket_index = msg_decoded.index("{")
        right_bracket_index = msg_decoded.index("}") + 1
        msg_decoded = msg_decoded[left_bracket_index:right_bracket_index]

        msg_json = json.loads(msg_decoded)

        return msg_json

    def send_player(self, player: Player):
       
        player_info = {
            "object": "player",
            "id": self.id,
            "position": (player.world_x, player.world_y, player.world_z),
            "rotation": player.rotation_y,
            "joined": False,
            "left": False,
            "model": str(player.model).replace("render/scene/player/", ""),
            "texture": str(player.texture).replace("render/scene/player/", "")
        }
        player_info_encoded = json.dumps(player_info).encode("utf8")

        try:
            self.client.send(player_info_encoded)
        except socket.error as e:
            print(e)
    
    def send_spell(self, mouse, camera):
        
        spell_info = {
            "object": "spell",
            "mouse_world_point": mouse.world_point,
            "camera_world_position": camera.world_position

        }
        
        spell_info_encoded = json.dumps(spell_info).encode("utf8")

        try:
            self.client.send(spell_info_encoded)
        except socket.error as e:
            print(e)