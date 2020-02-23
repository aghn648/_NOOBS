import random

from model import *

########################        AI no.1      ####################################################

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

        # choosing all flying units
        all_base_units = world.base_units
        my_deck = [base_unit for base_unit in all_base_units if base_unit.is_flying]

        # picking the chosen deck - rest of the deck will automatically be filled with random base_units
        world.choose_deck(base_units=my_deck)
        self.id = world.get_me().player_id
        enemyMap = { 0:3, 3:0, 1:2, 2:1}
        enemy_id = enemyMap.get(self.id, None)
        enemy = world.get_player_by_id(enemy_id)
        # other preprocess
        self.path_for_my_units = [world.get_shortest_path_to_cell(cell = enemy.king.center, from_player = world.get_me())]
########################        AI no.1      ####################################################

    # it is called every turn for doing process during the game
    def turn(self, world):
        print("turn started:", world.get_current_turn())

        myself = world.get_me()
        max_ap = world.game_constants.max_ap

        # play all of hand once your ap reaches maximum. if ap runs out, putUnit doesn't do anything
        pth = 0
        if myself.ap >= max_ap/2:
            min_base_unit = myself.hand[0]
            for base_unit in myself.hand:
                if(min_base_unit.ap < base_unit.ap):
                    min_base_unit = base_unit
            world.put_unit(base_unit=min_base_unit, path=self.path_for_my_units[pth])
########################        AI no.1      ####################################################

        # this code tries to cast the received spell
        received_spell = world.get_received_spell()
        if received_spell is not None:
  #          my_units = myself.units
##            unit = my_units[0]
   #         my_paths = myself.paths_from_player
    #        path = my_paths[random.randint(0, len(my_paths) - 1)]
     #       size = len(path.cells)
      #      cell = path.cells[int((size + 1) / 2)]
            #if len(my_units) > 0:
       #         world.cast_unit_spell(unit=unit, path=path, cell=unit.cell, spell=received_spell)
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
########################        AI no.1      ####################################################

        # this code tries to upgrade damage of first unit. in case there's no damage token, it tries to upgrade range
        if len(myself.units) > 0:
            unit = myself.units[0]
            world.upgrade_unit_damage(unit=unit)
            world.upgrade_unit_range(unit=unit)

    # it is called after the game ended and it does not affect the game.
    # using this function you can access the result of the game.
    # scores is a map from int to int which the key is player_id and value is player_score
    def end(self, world, scores):
        print("end started!")
        print("My score:" ,scores[world.get_me().player_id])
