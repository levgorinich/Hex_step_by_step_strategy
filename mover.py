import pygame


class Mover():
    def __init__(self, game_map):
        self.game_map = game_map
        self.starting_sprite = None
        self.ending_sprite = None
        self.atacking_unit = None
        self.defending_unit = None

    def move(self, hex_start: tuple[int, int], hex_end: tuple[int, int]):
        self.starting_sprite = self.game_map.hexes.hexes_dict[hex_start]
        self.ending_sprite = self.game_map.hexes.hexes_dict[hex_end]

        if self.starting_sprite.unit_on_hex and self.ending_sprite.unit_on_hex:
            self.atacking_unit = self.starting_sprite.unit_on_hex
            self.defending_unit = self.ending_sprite.unit_on_hex
            print(self.atacking_unit.player_id, self.defending_unit.player_id)
            if self.atacking_unit.player_id != self.defending_unit.player_id:
                self.handle_fighting(self.atacking_unit, self.defending_unit)
            else:
                self.atacking_unit.grid_pos = hex_end
                self.defending_unit.grid_pos = hex_start
                self.starting_sprite.remove_unit()
                self.ending_sprite.remove_unit()
                self.starting_sprite.add_unit(self.defending_unit)
                self.ending_sprite.add_unit(self.atacking_unit)

        elif unit := self.starting_sprite.unit_on_hex:

            self.starting_sprite.remove_unit()
            unit.grid_pos = hex_end
            self.ending_sprite.add_unit(unit)

    def handle_fighting(self, atacking_unit, defending_unit):
        if atacking_unit.grid_pos != defending_unit.grid_pos:
            self.kill_all(atacking_unit, defending_unit)
            self.kill_enemy(atacking_unit, defending_unit)
            self.kill_yourself(atacking_unit, defending_unit)
            self.kill_nothing(atacking_unit, defending_unit)
        else:
            pass

    def kill_all(self, atacking_unit, defending_unit):
        if (defending_unit.health_bar.hp - atacking_unit.attack <= 0
                and atacking_unit.health_bar.hp - defending_unit.attack <= 0):
            self.ending_sprite.kill_unit()
            self.starting_sprite.kill_unit()
            print("double death")

    def kill_enemy(self, atacking_unit, defending_unit):
        if (defending_unit.health_bar.hp - atacking_unit.attack <= 0
                and atacking_unit.health_bar.hp - defending_unit.attack > 0):
            self.ending_sprite.kill_unit()
            self.atacking_unit.update(defending_unit.attack)

            self.atacking_unit.grid_pos = self.ending_sprite.grid_pos

            self.starting_sprite.remove_unit()
            self.ending_sprite.add_unit(self.atacking_unit)
            self.atacking_unit = None

    def kill_yourself(self, atacking_unit, defending_unit):
        if (defending_unit.health_bar.hp - atacking_unit.attack > 0
                and atacking_unit.health_bar.hp - defending_unit.attack <= 0):
            defending_unit.update(atacking_unit.attack)
            self.starting_sprite.kill_unit()

    def kill_nothing(self, atacking_unit, defending_unit):
        if (defending_unit.health_bar.hp - atacking_unit.attack > 0
                and atacking_unit.health_bar.hp - defending_unit.attack > 0):
            defending_unit.update(atacking_unit.attack)
            atacking_unit.update(defending_unit.attack)
            print("last case")

    def move_unit(self):

        self.ending_sprite.remove_unit()
        self.unit_selected.grid_pos = self.ending_sprite.grid_pos
        self.ending_sprite.add_unit(self.unit_selected)
        self.unit_selected = None
