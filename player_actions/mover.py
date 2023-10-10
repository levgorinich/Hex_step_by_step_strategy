import random
import logging
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
        distance = self.game_map.calculate_distance(self.starting_sprite, self.ending_sprite)
        print(self.game_map.calculate_distance(self.starting_sprite, self.ending_sprite))
        if self.starting_sprite.unit_on_hex and self.ending_sprite.unit_on_hex:
            self.atacking_unit = self.starting_sprite.unit_on_hex
            self.defending_unit = self.ending_sprite.unit_on_hex


            if self.atacking_unit.player_id != self.defending_unit.player_id and  distance ==1:
                self.handle_fighting(self.atacking_unit, self.defending_unit)
            elif distance <= min(self.atacking_unit.stamina, self.defending_unit.stamina):
                self.swap_units( hex_end, hex_start, distance)


        elif unit := self.starting_sprite.unit_on_hex:

            self.starting_sprite.remove_unit()

            unit.move(hex_end, distance)
            print("in mover", unit.hexes_viewed)
            for hex in unit.hexes_viewed:
                hex.hide_hex()
            unit.hexes_viewed=[]
            if unit.player_id == self.game_map.player_id:
                self.game_map.coordinate_range(self.ending_sprite, unit.discovery_range)
                unit.hexes_viewed = self.game_map.view_range(self.ending_sprite, unit.view_range)
            self.ending_sprite.add_unit(unit)

    def swap_units(self, hex_end, hex_start, distance):

        logging.debug("swap units attacking", self.atacking_unit, self.defending_unit)
        self.atacking_unit.move(hex_end, distance)
        self.defending_unit.move(hex_start, distance)
        self.starting_sprite.remove_unit()
        self.ending_sprite.remove_unit()
        self.starting_sprite.add_unit(self.defending_unit)
        self.ending_sprite.add_unit(self.atacking_unit)
        self.game_map.actions.append("<move"+str(self.ending_sprite.grid_pos)+ ","+str(self.starting_sprite.grid_pos)+">")
    def handle_fighting(self, atacking_unit, defending_unit):
        if atacking_unit.grid_pos != defending_unit.grid_pos:
            defence = defending_unit.defend()
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
            logging.debug("kill all")
            self.ending_sprite.kill_unit()
            self.starting_sprite.kill_unit()
            print("double death")

    def kill_enemy(self, ):
            logging.debug("kill enemy")
            self.ending_sprite.kill_unit()
            self.atacking_unit.update_hp()
            self.atacking_unit.move(self.ending_sprite.grid_pos, 0)

            self.starting_sprite.remove_unit()
            self.ending_sprite.add_unit(self.atacking_unit)
            self.atacking_unit = None

    def kill_yourself(self,):
            logging.debug("kill yourself")
            self.defending_unit.update_hp()
            self.starting_sprite.kill_unit()

    def kill_nothing(self, ):
            logging.debug("kill nothing")
            self.defending_unit.update_hp()
            self.atacking_unit.update_hp()



