import random

import pygame


class Mover():
    def __init__(self, game_map):
        self.game_map = game_map
        self.starting_sprite = None
        self.ending_sprite = None
        self.atacking_unit = None
        self.defending_unit = None

    def move(self, hex_start: tuple[int, int], hex_end: tuple[int, int]):

        self.starting_sprite = self.game_map.get_hex_by_coord(hex_start)
        self.ending_sprite = self.game_map.get_hex_by_coord(hex_end)

        if self.starting_sprite.unit_on_hex and self.ending_sprite.unit_on_hex:
            self.atacking_unit = self.starting_sprite.unit_on_hex
            self.defending_unit = self.ending_sprite.unit_on_hex

            if self.atacking_unit.player_id != self.defending_unit.player_id:
                self.handle_fighting(self.atacking_unit, self.defending_unit)
            else:
                self.swap_units( hex_end, hex_start)


        elif unit := self.starting_sprite.unit_on_hex:

            self.starting_sprite.remove_unit()
            unit.grid_pos = hex_end
            self.ending_sprite.add_unit(unit)

    def swap_units(self, hex_end, hex_start):

        self.atacking_unit.grid_pos = hex_end
        self.defending_unit.grid_pos = hex_start
        self.starting_sprite.remove_unit()
        self.ending_sprite.remove_unit()
        self.starting_sprite.add_unit(self.defending_unit)
        self.ending_sprite.add_unit(self.atacking_unit)
    def handle_fighting(self, atacking_unit, defending_unit):
        if atacking_unit.grid_pos != defending_unit.grid_pos:
            defence = defending_unit.attack* (random.random()/2+0.25)
            strike =  atacking_unit.strike()
            print(defence, strike)
            atacking_unit.hp -= defence
            defending_unit.hp -= strike

            if atacking_unit.hp <=0 and defending_unit.hp <= 0:
                self.kill_all()
            elif defending_unit.hp <=0 and atacking_unit.hp >0:
                print("killing enemy", atacking_unit, defending_unit)
                self.kill_enemy()
            elif defending_unit.hp >0 and atacking_unit.hp <=0:
                self.kill_yourself()
            elif defending_unit.hp > 0 and atacking_unit.hp > 0:
                self.kill_nothing()
        else:
            pass


    def kill_all(self, ):
            self.ending_sprite.kill_unit()
            self.starting_sprite.kill_unit()
            print("double death")

    def kill_enemy(self, ):
            self.ending_sprite.kill_unit()
            self.atacking_unit.update_hp()
            self.atacking_unit.grid_pos = self.ending_sprite.grid_pos

            self.starting_sprite.remove_unit()
            self.ending_sprite.add_unit(self.atacking_unit)
            self.atacking_unit = None

    def kill_yourself(self,):
            self.defending_unit.update_hp()
            self.starting_sprite.kill_unit()

    def kill_nothing(self, ):
            self.defending_unit.update_hp()
            self.atacking_unit.update_hp()


    def move_unit(self):
        self.ending_sprite.remove_unit()
        self.unit_selected.grid_pos = self.ending_sprite.grid_pos
        self.ending_sprite.add_unit(self.unit_selected)
        self.unit_selected = None
