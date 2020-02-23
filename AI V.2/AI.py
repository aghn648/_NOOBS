import random

from model import *

########################        AI no.2      ####################################################
class AI:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.path_for_my_units = None

    # this function is called in the beginning for deck picking and pre process
    def pick(self, world):
        print("pick started!")

        # preprocess
        map = world.get_map()
        self.rows = map.row_num
        self.cols = map.column_num

        # choosing the cheapest units
        all_base_units = world.base_units
        my_deck = [base_unit for base_unit in all_base_units if base_unit.ap < 5]

        # picking the chosen deck - rest of the deck will automatically be filled with random base_units
        world.choose_deck(base_units=my_deck)

        # other preprocess
        self.path_for_my_units = [world.get_first_enemy().paths_from_player[0] ,
                                    world.get_friend().paths_from_player[0]]
########################        AI no.2      ####################################################
    # it is called every turn for doing process during the game
    def turn(self, world):
        print("turn started:", world.get_current_turn())
        myself = world.get_me()
        max_ap = world.game_constants.max_ap
        selfap = myself.ap
        ch = random.randint(0,1)
        supp = 4 - world.get_current_turn()//20
        # play all of hand once your ap reaches maximum. if ap runs out, putUnit doesn't do anything
        self.units = self.unit_ap_sorter(myself.hand)
        if myself.ap >= max_ap - 1:
            while(selfap > self.units[0].ap):
                if supp:
                    supp -= 1
                    selfap -= self.units[0].ap
                    choose_unit = self.units.pop(0)
                else:
                    j = len(self.units) - 1
                    while(self.units[j].ap > selfap):
                        j -= 1
                    selfap -= self.units[j].ap
                    choose_unit = self.units.pop(j)
                world.put_unit(base_unit=choose_unit, path=self.path_for_my_units[ch])
########################        AI no.2      ####################################################
        # this code tries to cast the received spell
        received_spell = world.get_received_spell()
        if received_spell is not None:
            if received_spell.is_area_spell():
                if received_spell.target == SpellTarget.ENEMY:
                    enemy_units = world.get_first_enemy().units
                    if len(enemy_units) > 0:
                        world.cast_area_spell(center=enemy_units[0].cell, spell=received_spell)
                elif received_spell.target == SpellTarget.ALLIED:
                    friend_units = world.get_friend().units
                    if len(friend_units) > 0:
                        world.cast_area_spell(center=friend_units[0].cell, spell=received_spell)
                elif received_spell.target == SpellTarget.SELF:
                    my_units = myself.units
                    if len(my_units) > 0:
                        world.cast_area_spell(center=my_units[0].cell, spell=received_spell)
            else:
                my_units = myself.units
                if len(my_units) > 0:
                     unit = my_units[0]
                     my_paths = myself.paths_from_player
                     path = my_paths[random.randint(0, len(my_paths) - 1)]
                     size = len(path.cells)
                     cell = path.cells[int((size + 1) / 2)]
                     world.cast_unit_spell(unit=unit, path=path, cell=cell, spell=received_spell)
########################        AI no.2      ####################################################
        # this code tries to upgrade damage of first unit. in case there's no damage token, it tries to upgrade range
        if len(myself.units) > 0:
            unit = myself.units[0]
            world.upgrade_unit_damage(unit=unit)
            world.upgrade_unit_range(unit=unit)
        print("Done")
    # it is called after the game ended and it does not affect the game.
    # using this function you can access the result of the game.
    # scores is a map from int to int which the key is player_id and value is player_score
    def end(self, world, scores):
        print("end started!")
        print("My score:" ,scores[world.get_me().player_id])
    def unit_ap_sorter(self, units):
        for i in range(1, len(units)):   
            key = units[i]  
            j = i-1
            while j >=0 and key.ap < units[j].ap : 
                    units[j+1] = units[j] 
                    j -= 1
            units[j+1] = key 
        return units