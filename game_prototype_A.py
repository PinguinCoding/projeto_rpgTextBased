# This file contains the first prototype of the game, the functions here will be adapted to other
# files and this file will serve only as reference for development purpose

# ==GAME IMPORTATION BLOCK== #
from sys import exit, stdout  # Will be used to exit prompt and to control text speed
from time import sleep  # Will be used to control text speed
from os import system  # Will be used to interact with prompt
from random import randint  # Will be used to add random elements to the game


# ==GAME SETUPS== #
# Recurrent Functions
def void_clear_screen_gmf():
    system('cls')


# This function will be used when the screen needed to be clean


def void_speech_gmf(text: str, velocity: float):
    for character in text:
        stdout.write(character)
        stdout.flush()
        sleep(velocity)


# This function will be used to create texts in prompt with control speed


# Player Setup
class Player(object):
    def __init__(self):
        """
        Explaining the attributes from this class:
        NAME --> It's a constant that holds the player's chosen name: str
        ROLE --> It's a constant that holds tha player's chosen role: str
        hp --> It's a variable that holds the player's health points: int
        inventory --> It's a dictionary that holds the player's items from two classifications; 'key_item' and 'useful_item': dict
        status_effect --> It's a list that displays the player's status effects: list
        position --> It's a variable tha keeps track of the player's position: str
        game_over --> It's a variable that tells when the game ends as the player's hp hits 0: bool
        """
        self.NAME = ''
        self.ROLE = ''
        self.hp = 0
        self.inventory = {'key_items': list(), 'useful_items': list()}
        self.status_effect = []
        self.position = 'b2'
        self.game_over = False

    # This function initiate the class 'Player'

    def player_move_character_gmf(self, destination: str):
        if destination is None:
            print('You cannot go there.')
        else:
            print('\n' + 'You have moved to the ' + destination + '.')
            self.position = destination
            void_print_position_gmd()

    # This function will be in charged to move the player around the map

    def player_input_to_move_gmi(self, direction: str):
        # Deals with a one word input
        if direction == '':
            ask = 'Where would you like to move to?\n> '
            destination = (input(ask)).lower().strip()
            while destination not in ['up', 'north', 'down', 'south', 'left', 'west', 'right', 'east']:
                print('Please type.\n(Up, down, left, right or north, sout, west, east\n')
                destination = (input(ask)).lower().strip()

            if destination in ['up', 'north']:
                destination = zone_map_keys[self.position].UP
                self.player_move_character_gmf(destination)

            elif destination in ['down', 'south']:
                destination = zone_map_keys[self.position].DOWN
                self.player_move_character_gmf(destination)

            elif destination in ['left', 'west']:
                destination = zone_map_keys[self.position].LEFT
                self.player_move_character_gmf(destination)

            elif destination in ['right', 'east']:
                destination = zone_map_keys[self.position].RIGHT
                self.player_move_character_gmf(destination)

        # Deals with a two word input
        elif direction in ['up', 'north', 'down', 'south', 'left', 'west', 'right', 'east']:
            destination = direction

            if destination in ['up', 'north']:
                destination = zone_map_keys[self.position].UP
                self.player_move_character_gmf(destination)

            elif destination in ['down', 'south']:
                destination = zone_map_keys[self.position].DOWN
                self.player_move_character_gmf(destination)

            elif destination in ['left', 'west']:
                destination = zone_map_keys[self.position].LEFT
                self.player_move_character_gmf(destination)

            elif destination in ['right', 'east']:
                destination = zone_map_keys[self.position].RIGHT
                self.player_move_character_gmf(destination)
        else:
            print('Invalid direction.\n')

    # This function will take the input to move from the player to move the character

    def player_examine_zone_gmf(self, referredItem: str):
        if zone_map_keys[self.position].solved is False:
            if referredItem == '':
                print(zone_map_keys[self.position].EXAMINATION)
                # Examination of the room

            elif referredItem in zone_map_keys[self.position].ELEMENTS:
                print(zone_map_keys[self.position].ELEMENTS[referredItem]['description'])
                # Examination of some element in the room (OBS: Elements can't be pick up by the player)

            elif referredItem in zone_map_keys[self.position].ITEMS:
                print(zone_map_keys[self.position].ITEMS[referredItem]['description'])
                # Examination of some item in the room (OBS: Item can be pick up by the player)

            else:
                print('The referred item "' + referredItem + '" does not exist in this room.')
        else:
            print('You have already exhausted this zone.')

    # This function will allow the player to interact with the map

    def player_search_inventory_gmf(self, searchedItem: str):
        for item in self.inventory['key_items']:
            if item['nameDisplay'] == searchedItem:
                return item

        # Item was not found in 'key_items'
        for item in self.inventory['useful_items']:
            if item['nameDisplay'] == searchedItem:
                return item

        # Item was not found in neither
        return None

    # This function will search an item from the player inventory in both the 'key_items' and 'useful_items'

    def player_input_to_use_gmi(self, referredItem: str):
        # Decides if player will use the item from inventory or from the zone he's in
        if referredItem == '':
            ask1 = 'What would you like to use?\n> '
            item = (input(ask1)).lower().strip()
            # Input item

            ask2 = 'You would like to use the ' + item + ' from where?\n> '
            print('[Zone] or [Inventory]')
            local = (input(ask2)).lower().strip()
            # Input location

            while local not in ['zone', 'inventory']:
                print('Write a valid location to use the item from.')
                print('=' * 24)
                local = (input(ask2)).lower().strip()

            if local == 'zone':
                self.player_use_element_gmf(item)
            else:
                self.player_use_item_gmf(item)
        else:
            ask = 'You would like to use the ' + referredItem + ' from where?\n> '
            print('[Zone] or [Inventory]')
            local = (input(ask)).lower().strip()
            # Input location

            while local not in ['zone', 'inventory']:
                print('Write a valid location to use the item from.')
                print('=' * 24)
                local = (input(ask)).lower().strip()

            if local == 'zone':
                self.player_use_element_gmf(referredItem)
            else:
                self.player_use_item_gmf(referredItem)

    # This function will filtrate the place from where the player is trying to use the item from

    def player_use_item_gmf(self, referredItem: str):
        item = self.player_search_inventory_gmf(referredItem)

        if item is None:
            print('There is no such an item in your possession to be used here.')
        else:
            if item['classification'] == 'key_item':  # The item will be used to solve a puzzle
                if item['conditionUse']():
                    print(item['whenUsed'])
                    print('After used, the ' + referredItem + ' was swallow by darkness.')
                    self.inventory['key_items'].remove(item)
                    zone_map_keys[self.position].zone_state_change_gmf(referredItem)
                    zone_map_keys[self.position].solved = True
                else:
                    print('You cannot use this item here.')

            else:  # The item will be used to change player status
                # Effects can be 'healing', 'remove side effect A', 'remove side effect B', 'stronger body', etc
                if item['effects'] == 'healing':
                    if self.hp in [60, 70, 90]:  # HP of priest, rogue and warrior
                        print('You feel fine by now, better saved for later.')
                    else:
                        amount = randint(1, 10)
                        self.hp += amount
                        print('You use the ' + referredItem + ' to heal your body.')
                        sleep(0.3)
                        print('You feel better now.')
                        self.inventory['useful_items'].remove(item)
                        zone_map_keys[self.position].zone_state_change_gmf(referredItem)

    # This function will allow the player to use an item from his inventory

    def player_use_element_gmf(self, referredItem: str):
        if zone_map_keys[self.position].solved is False:
            if referredItem not in zone_map_keys[self.position].ELEMENTS:
                print('There is nothing like that to use here.')

            elif zone_map_keys[self.position].ELEMENTS[referredItem]['wasUsed'] is False:
                print(zone_map_keys[self.position].ELEMENTS[referredItem]['narration'])
                zone_map_keys[self.position].ELEMENTS[referredItem]['wasUsed'] = True
                zone_map_keys[self.position].zone_state_change_gmf(referredItem)

            else:
                print('You already use the ' + referredItem + '.')
        else:
            print('You have already done everything possible here.')

    # This function will allow the player to use an element from the zone he's in

    def player_collect_item_gmi(self, referredItem: str):
        if referredItem == '':
            ask = 'What would you like to take from this room?\n> '
            item = (input(ask)).lower().strip()

            if item not in zone_map_keys[self.position].ITEMS:
                print('There is nothing like that laying in the room.')
            else:
                item_dict = zone_map_keys[self.position].ITEMS[item]
                print(item_dict['whenGrabbed'])

                if item_dict['classification'] == 'key_item':
                    self.inventory['key_items'].append(item_dict)
                else:
                    self.inventory['useful_items'].append(item_dict)

                zone_map_keys[self.position].zone_state_change_gmf(item)  # This line updates the map
        else:
            if referredItem not in zone_map_keys[self.position].ITEMS:
                print('There is nothing like that laying in the room.')
            else:
                item_dict = zone_map_keys[self.position].ITEMS[referredItem]
                print(item_dict['whenGrabbed'])

                if item_dict['classification'] == 'key_item':
                    self.inventory['key_items'].append(item_dict)
                else:
                    self.inventory['useful_items'].append(item_dict)

                zone_map_keys[self.position].zone_state_change_gmf(referredItem)  # This line updates the map

    # This function will allow the player to collect items from the zone he's in

    def player_drop_item_gmi(self, referredItem: str):
        if referredItem == '':
            ask = 'What item would you like to leave behind?\n(Remember that only not important items can' \
                  'be left behind and once you dispose of one, it can never take back.\n> '

            # Show inventory before item can be dropped
            print('=' * 24)
            self.player_visualize_inventory_gmf()
            print('=' * 24)

            # Take input
            item = (input(ask)).lower().strip()

            # Search the item
            verify_item = self.player_search_inventory_gmf(item)

            if verify_item is None:
                print('There is no such an item in your possession.')
            elif verify_item['classification'] == 'key_item':
                print('You cannot let go of such an important item.')
            else:
                self.inventory['useful_items'].remove(verify_item)
                print('The ' + item + ' was left behind, swallowed by darkness.')
        else:
            # Search the item
            verify_item = self.player_search_inventory_gmf(referredItem)

            if verify_item is None:
                print('There is no such an item in your possession.')
            elif verify_item['classification'] == 'key_item':
                print('You cannot let go of such an important item.')
            else:
                self.inventory['useful_items'].remove(verify_item)
                print('The ' + referredItem + ' was left behind, swallowed by darkness.')

    # This function will allow the player to drop an item from his inventory

    def player_visualize_inventory_gmf(self):
        if self.inventory == {'key_items': list(), 'useful_items': list()}:
            print('You carried nothing.')
        else:
            for item_class in self.inventory.keys():
                print('-=' + item_class + '=-')
                for i, item in enumerate(self.inventory[item_class]):
                    print(str(i + 1) + '.' + item['nameDisplay'])
            print()

    # This function will allow the player to view his inventory


myPlayer = Player()


# Title Screen Setup
def void_tittle_screen_select_gmi():
    option = (input('> ')).lower().strip()

    while option not in ['play', 'help', 'quit']:
        print('Enter a valid option please\n')
        option = (input('> ')).lower().strip()

    if option == 'play':
        void_start_game_gmf()
    elif option == 'help':
        void_help_menu_display_gmd()

    exit()


# This function will allow the player to navigate through the title screen


def void_tittle_screen_display_gmd():
    void_clear_screen_gmf()
    print('#' * 24)
    print('Welcome to the Text RPG!')
    print('#' * 24)
    print('' * 9, '-Play-', '' * 9)
    print('' * 9, '-Help-', '' * 9)
    print('' * 9, '-Quit-', '' * 9)
    void_tittle_screen_select_gmi()


# This function will display the tittle screen to the player


def void_help_menu_display_gmd():
    print('#' * 24)
    print('Welcome to the Text RPG!')
    print('#' * 24)
    print('-Type your commands to do them-')
    print("-Type 'move' to walk around the map-")
    print('-Type a direction like up, down, left, right or north, south, east, west to move-')
    print("-Type 'look' to inspect the room you are in-")
    print("-Type some word after 'look' to inspect something specific that catches your attention-")
    print("-Type 'view' to see the items in your inventory-")
    print("-Type 'use' to use any item you want-")
    print("-Type 'quit' at any time to exit the game-")
    void_tittle_screen_select_gmi()


# This functon will display a quick guide to the player


# Map and Zones Setups
class Zone(object):
    def __init__(self):
        """
        Explaining the attributes from this class:
        ZONE_NAME --> It's the name of the zone: str
        DESCRIPTION --> It's the zone description the shows when entered: str
        EXAMINATION --> It's the zone description when inspect by the player: str
        ELEMENTS --> It's a dictionary containing all the elements of the zone: dict
        CHANGES --> It's the zone description after it's been change by some item/element use: str
        ITEMS --> It's a dictionary containing all the items of the zone: dict
        NPCS --> It's a dictionary ---
        UP --> It's the room pointer to the zone directly above: str
        DOWN --> It's the room pointer to  the zone directly bellow: str
        LEFT --> It's the room pointer to the zone directly at left: str
        RIGHT --> It's the room pointer to the zone directly at right: str
        solved --> It's a variable that shows if the puzzle of the room has be solved or not: bool
        """
        self.ZONE_NAME = ''
        self.DESCRIPTION = ''
        self.EXAMINATION = ''
        self.ELEMENTS = {}
        self.CHANGES = {}
        self.ITEMS = {}
        self.NPCS = {}
        self.UP = ''
        self.DOWN = ''
        self.LEFT = ''
        self.RIGHT = ''
        self.solved = False

    # This function initiate the class 'Zone'

    def zone_state_change_gmf(self, referredItem):
        self.EXAMINATION = self.CHANGES[referredItem]
    # This function changes a zone 'EXAMINATION'


# OBS: The player initiate at the 'b2' position
# Map representation:
'''
-------------
|a1|a2|a3|a4| 
-------------
|b1|**|b3|b4| 
-------------
|c1|c2|c3|c4| 
-------------
|d1|d2|d3|d4| 
-------------

Orientation:
      UP
LEFT      RIGHT
     DOWN
'''

# Creating the zones as objects
a1 = Zone()
a2 = Zone()
a3 = Zone()
a4 = Zone()

b1 = Zone()
b2 = Zone()
b3 = Zone()
b4 = Zone()

c1 = Zone()
c2 = Zone()
c3 = Zone()
c4 = Zone()

d1 = Zone()
d2 = Zone()
d3 = Zone()
d4 = Zone()

# Items dictionary
items = {'bandage': {'nameDisplay': 'bandage',
                     'description': 'A dirty bandage, it can be used to stop the bleeding.',
                     'whenGrabbed': 'You bend down and grab it.',
                     'whenUsed': 'You use the bandage to recover from your wounds.',
                     'wasUsed': False,
                     'conditionUse': None,
                     'classification': 'useful_item',
                     'effects': 'healing'},
         'small key': {'nameDisplay': 'small key',
                       'description': 'A small glowing key, it probably can be use to open a door.',
                       'whenGrabbed': 'You bend down and grab it.',
                       'whenUsed': 'You use the key to open the door, it works!',
                       'wasUsed': False,
                       'conditionUse': lambda: myPlayer.position == 'b3',
                       'classification': 'key_item',
                       'effects': None},
         'health potion': {'nameDisplay': 'health potion',
                           'description': 'A small red potion, it stinks.',
                           'whenGrabbed': 'You bend down and grab it.',
                           'whenUsed': 'You drink the potion, it taste awful, but you feel better in a second.',
                           'wasUsed': False,
                           'conditionUse': None,
                           'classification': 'useful_item',
                           'effects': 'healing'}
         }

# Configuration of each zone
# 'a' zones
a1.ZONE_NAME = 'Dark Cell'
a1.DESCRIPTION = 'A room filled with nothing but darkness.'
a1.EXAMINATION = 'There is a stone laying on the floor and a chain.'
a1.UP = None
a1.DOWN = 'b1'
a1.LEFT = None
a1.RIGHT = 'a2'
a1.ELEMENTS = {'stone': {'description': 'a small stone, can possible be used to destroy the chains.',
                         'narration': 'you use the stone to break the chains.',
                         'wasUsed': False}
               }
a1.CHANGES = {'stone': 'The chain is laying in the floor, broken by you.'}
# zona.CHANGES = {'<object that caused the change>': '<new examination of the room>'}

a2.ZONE_NAME = 'Dark room'
a2.DESCRIPTION = 'A room filled with nothing but darkness.'
a2.EXAMINATION = 'There is nothing here to find.'
a2.UP = None
a2.DOWN = 'b2'
a2.LEFT = 'a1'
a2.RIGHT = 'a3'
a2.NPCS = {'name': 'Helm',
           'description': 'You see and old man, sitting in the floor. He is skinny and look weak to you, '
                          'he is whispering something you cannot hear.',
           'repetitive': ['Broke...', '...', 'Chains...', 'Free me...'],
           'main-dialogue': 'Thank you so much, you broke those chains, have you not? I am free now, you see, here.'
                            'Take this, it may be useful to you. Now, see you later prisoner.',
           'after-dialogue': 'He is not going to talk to you again.',
           'item-given': items['health potion'],
           'condition': lambda: a1.solved is True}
# name == the NPC's name
# description == the NPC's description when the player use 'inspect' or similar
# repetitive == the NPC's random lines when the conditions to unlock his main dialogue still is unmatched
# main-dialogue == the NPC's main dialogue
# after-dialogue == the NPC's dialogue once he talked to the player
# item-given == the NPC's item he gives the player
# condition == the NPC's condition to unlock his main dialogue sequence

a3.ZONE_NAME = 'Dark room'
a3.DESCRIPTION = 'A room filled with nothing but darkness.'
a3.EXAMINATION = 'There is nothing here to find.'
a3.UP = None
a3.DOWN = 'b3'
a3.LEFT = 'a2'
a3.RIGHT = 'a4'

a4.ZONE_NAME = 'Dark room'
a4.DESCRIPTION = 'A room filled with nothing but darkness.'
a4.EXAMINATION = 'There is nothing here to find.'
a4.UP = None
a4.DOWN = 'b4'
a4.LEFT = 'a3'
a4.RIGHT = None

# 'b' zones
b1.ZONE_NAME = 'Dark room'
b1.DESCRIPTION = 'A room filled with nothing but darkness.'
b1.EXAMINATION = 'There is a dirty bandage laying in the dark floor.'
b1.UP = 'a1'
b1.DOWN = 'c1'
b1.LEFT = None
b1.RIGHT = 'b2'
b1.CHANGES = {'bandage': 'The room where you toke the bandage, it seems more empty now.'}

b2.ZONE_NAME = 'Dark room'
b2.DESCRIPTION = 'A room filled with nothing but darkness.'
b2.EXAMINATION = 'There is a small glowing key laying in the floor.'
b2.UP = 'a2'
b2.DOWN = 'c2'
b2.LEFT = 'b1'
b2.RIGHT = 'b3'

b2.CHANGES = {'small key': 'The room where you toke the key, it seems more empty now.'}

b3.ZONE_NAME = 'Dark room'
b3.DESCRIPTION = 'A room filled with nothing but darkness.'
b3.EXAMINATION = 'There is a door here to open.'
b3.UP = 'a3'
b3.DOWN = 'c3'
b3.LEFT = 'b2'
b3.RIGHT = 'b4'
b3.CHANGES = {'small key': 'The door is laying wide open.'}

b4.ZONE_NAME = 'Dark room'
b4.DESCRIPTION = 'A room filled with nothing but darkness.'
b4.EXAMINATION = 'There is nothing here to find.'
b4.UP = 'a4'
b4.DOWN = 'c4'
b4.LEFT = 'b3'
b4.RIGHT = None

# 'c' zones
c1.ZONE_NAME = 'Dark room'
c1.DESCRIPTION = 'A room filled with nothing but darkness.'
c1.EXAMINATION = 'There is nothing here to find.'
c1.UP = 'b1'
c1.DOWN = 'd1'
c1.LEFT = None
c1.RIGHT = 'c2'

c2.ZONE_NAME = 'Dark room'
c2.DESCRIPTION = 'A room filled with nothing but darkness.'
c2.EXAMINATION = 'There is nothing here to find.'
c2.UP = 'b2'
c2.DOWN = 'd2'
c2.LEFT = 'c1'
c2.RIGHT = 'c3'

c3.ZONE_NAME = 'Dark room'
c3.DESCRIPTION = 'A room filled with nothing but darkness.'
c3.EXAMINATION = 'There is nothing here to find.'
c3.UP = 'b3'
c3.DOWN = 'd3'
c3.LEFT = 'c2'
c3.RIGHT = 'c4'

c4.ZONE_NAME = 'Dark room'
c4.DESCRIPTION = 'A room filled with nothing but darkness.'
c4.EXAMINATION = 'There is nothing here to find.'
c4.UP = 'b4'
c4.DOWN = 'd4'
c4.LEFT = 'c3'
c4.RIGHT = None

# 'd' zones
d1.ZONE_NAME = 'Dark room'
d1.DESCRIPTION = 'A room filled with nothing but darkness.'
d1.EXAMINATION = 'There is nothing here to find.'
d1.UP = 'c1'
d1.DOWN = None
d1.LEFT = None
d1.RIGHT = 'd2'

d2.ZONE_NAME = 'Dark room'
d2.DESCRIPTION = 'A room filled with nothing but darkness.'
d2.EXAMINATION = 'There is nothing here to find.'
d2.UP = 'c2'
d2.DOWN = None
d2.LEFT = 'd1'
d2.RIGHT = 'd3'

d3.ZONE_NAME = 'Dark room'
d3.DESCRIPTION = 'A room filled with nothing but darkness.'
d3.EXAMINATION = 'There is nothing here to find.'
d3.UP = 'c3'
d3.DOWN = None
d3.LEFT = 'd2'
d3.RIGHT = 'd4'

d4.ZONE_NAME = 'Dark room'
d4.DESCRIPTION = 'A room filled with nothing but darkness.'
d4.EXAMINATION = 'There is nothing here to find.'
d4.UP = 'c4'
d4.DOWN = None
d4.LEFT = 'd3'
d4.RIGHT = None

# Creating a dictionary to easily access the zones attributes
zone_map_keys = {
    'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4,
    'b1': b1, 'b2': b2, 'b3': b3, 'b4': b4,
    'c1': c1, 'c2': c2, 'c3': c3, 'c4': c4,
    'd1': d1, 'd2': d2, 'd3': d3, 'd4': d4,
}


def void_setup_game_gmi():
    # Collect name from the player
    question = 'Enter the name of the prisoner. \n'
    void_speech_gmf(question, 0.05)
    player_name = (input('> ')).capitalize()
    myPlayer.NAME = player_name

    # Collect role from the player
    question = 'Enter the role of the prisoner. \n(You can play as a warrior, rogue or priest)\n'
    void_speech_gmf(question, 0.05)
    player_role = (input('> ')).lower()
    valid_roles = ['warrior', 'rogue', 'priest']

    while player_role not in valid_roles:
        print('Enter a valid role.\n')
        player_role = (input('> ')).lower()

    myPlayer.ROLE = player_role
    print('The prisoner used to be a ' + player_role + '.\n')

    # Defining player status
    if myPlayer.ROLE == 'warrior':
        myPlayer.hp = 90

    elif myPlayer.ROLE == 'rogue':
        myPlayer.hp = 70

    elif myPlayer.ROLE == 'priest':
        myPlayer.hp = 60


# This function will set up the game before starting it

# ==GAME SETUPS ENDS== #


# ==GAME INTERACTIVITY== #
def void_print_position_gmd():
    print('\n' + ('#' * (4 + len(myPlayer.position))))
    print('# ' + myPlayer.position.upper() + ' #')
    print('# ' + zone_map_keys[myPlayer.position].DESCRIPTION + ' #')
    print('\n' + ('#' * (4 + len(myPlayer.position))))


# This function will print the position of the player


def void_prompt_gmi():
    acceptable_actions = ['go', 'move', 'travel', 'walk', 'look', 'examine', 'inspect', 'interact',
                          'quit', 'use', 'grab', 'collect', 'take', 'trow', 'drop', 'view', 'speak',
                          'say', 'talk']
    print('\n' + '=' * 24)
    print('What would you like to do?')
    action = (input('> ')).lower().strip()

    # Dealing with a two words input
    if ' ' in action:
        actionVerb = action[:action.index(' ')].strip()
        actionObj = action[action.index(' '):].strip()

    # Dealing with a one word input
    else:
        actionVerb = action
        actionObj = ''

    while actionVerb not in acceptable_actions:
        print('Unknown action, try again.\n')
        action = (input('> ')).lower().strip()

        # Same from above
        if ' ' in action:
            actionVerb = action[:action.index(' ')].strip()
            actionObj = action[action.index(' '):].strip()
        else:
            actionVerb = action
            actionObj = ''

    if actionVerb == 'quit':
        exit()

    elif actionVerb in ['go', 'move', 'travel', 'walk']:
        myPlayer.player_input_to_move_gmi(actionObj)

    elif actionVerb in ['look', 'examine', 'inspect', 'interact']:
        myPlayer.player_examine_zone_gmf(actionObj)

    elif actionVerb == 'use':
        myPlayer.player_input_to_use_gmi(actionObj)

    elif actionVerb in ['grab', 'collect', 'take']:
        myPlayer.player_collect_item_gmi(actionObj)

    elif actionVerb in ['trow', 'drop']:
        myPlayer.player_drop_item_gmi(actionObj)

    elif actionVerb == 'view':
        myPlayer.player_visualize_inventory_gmf()


# This function will be the main interactivity with the game, the prompt asking him actions

# ==GAME INTERACTIVITY ENDS== #


# ==GAME FUNCTIONALITY== #
def void_main_game_loop_gmf():
    while not myPlayer.game_over:
        void_prompt_gmi()


# This function will keep the main game loop running


def void_start_game_gmf():
    void_clear_screen_gmf()
    void_setup_game_gmi()

    # Play the game introduction
    quote = 'Welcome, ' + myPlayer.NAME + ' the prisoner and ex-' + myPlayer.ROLE + '.\n'
    void_speech_gmf(quote, 0.05)

    speech1 = 'Welcome to this fantasy world!\n'
    speech2 = 'I hope it greets you well\n'
    speech3 = 'Just make sure you do not get to lost...\n'
    speech4 = 'Heheheh...\n'
    speech5 = '# Let the journey begin... #'

    void_speech_gmf(speech1, 0.03)
    void_speech_gmf(speech2, 0.03)
    void_speech_gmf(speech3, 0.1)
    void_speech_gmf(speech4, 0.2)
    void_speech_gmf(speech5, 0.1)
    void_clear_screen_gmf()
    void_main_game_loop_gmf()


# This function will start the game


void_tittle_screen_display_gmd()
