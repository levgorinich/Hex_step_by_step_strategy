

from internet_acsess.network import Network
from main_components.Map import Map
from main_components.MouseClickHandler import MouseClickHandler
from main_components.Render import Render
from main_components.User_interface import UI
from main_components.mapMovement import MapMovementTracker
from player_actions.Buttons import MenuButton
from player_actions.MoveParser import Parser
from player_actions.Spawner import Spawner
from player_actions.mover import Mover
from main_components.Player import Player

class OfflinePlayer:
    def __init__(self, window_size, internal_surface_size, id):

        self.game_map = Map(6, 6, id, 10,3, True)
        self.player = Player(id,self.game_map )
        self.player.max_moves = 100
        self.player.moves = 100
        self.mover = Mover(self.game_map)
        self.spawner = Spawner(self.game_map,)
        self.move_parser = Parser(self.mover, self.spawner, self.player)
        self.user_interface = UI(window_size, self.game_map, self.player, self.spawner)
        self.tracker = MapMovementTracker(internal_surface_size, window_size, )
        self.renderer = Render(internal_surface_size, map_movement_tracker=self.tracker, user_interface=self.user_interface)
        self.click_handler = MouseClickHandler(self.game_map, self.user_interface, self.tracker, self.mover)
