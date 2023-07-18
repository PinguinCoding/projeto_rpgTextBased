# ==GAME IMPORTATION BLOCK== #
from sys import exit, stdout  # Will be used to exit prompt and to control text speed
from time import sleep  # Will be used to control text speed
from os import system  # Will be used to interact with prompt
from random import randint  # Will be used to add random elements to the game


# ==GAME SETUPS== #
# Recurrent Functions
def clear_screen():
    system('cls')
    # This function will always be used when the screen needed to be clean


def timed_speech(text: str, velocity: float):
    for character in text:
        stdout.write(character)
        stdout.flush()
        sleep(velocity)
        # This function will be used to create texts in prompt with control speed


# Player Setup
class Player(object):
    def __init__(self):
        self.name = ''
        self.role = ''
        self.hp = 0
        self.inventory = {'key_items': list(), 'useful_items': list()}
        self.amount_dices = 0
        self.dices = []
        self.status_effect = []
        self.position = 'b2'
        self.game_over = False

    def movement_handler(self, destination: str):
        if destination is None:
            print('You cannot go there.')
        else:
            print('\n' + 'You have moved to the ' + destination + '.')
            self.position = destination
            print_position()
        # This function will be in charged to move the player around the map

    def player_move(self, direction):
        # One word input
        if direction == '':
            ask = 'Where would you like to move to?\n> '
            destination = (input(ask)).lower().strip()
            while destination not in ['up', 'north', 'down', 'south', 'left', 'west', 'right', 'east']:
                print('Please type.\n(Up, down, left, right or north, sout, west, east\n')
                destination = (input(ask)).lower().strip()

            if destination in ['up', 'north']:
                destination = zone_map_keys[self.position].UP
                self.movement_handler(destination)

            elif destination in ['down', 'south']:
                destination = zone_map_keys[self.position].DOWN
                self.movement_handler(destination)

            elif destination in ['left', 'west']:
                destination = zone_map_keys[self.position].LEFT
                self.movement_handler(destination)

            elif destination in ['right', 'east']:
                destination = zone_map_keys[self.position].RIGHT
                self.movement_handler(destination)

        # Two word input
        elif direction in ['up', 'north', 'down', 'south', 'left', 'west', 'right', 'east']:
            destination = direction

            if destination in ['up', 'north']:
                destination = zone_map_keys[self.position].UP
                self.movement_handler(destination)

            elif destination in ['down', 'south']:
                destination = zone_map_keys[self.position].DOWN
                self.movement_handler(destination)

            elif destination in ['left', 'west']:
                destination = zone_map_keys[self.position].LEFT
                self.movement_handler(destination)

            elif destination in ['right', 'east']:
                destination = zone_map_keys[self.position].RIGHT
                self.movement_handler(destination)
        else:
            print('Invalid direction.\n')

        # This function will take the input to move from the player to move the character

    def player_examine(self, referredItem: str):
        if zone_map_keys[self.position].SOLVED is False:
            if referredItem == '':
                print(zone_map_keys[self.position].EXAMINATION)
                # Examination of the room

            elif referredItem in zone_map_keys[self.position].ELEMENTS:
                print(zone_map_keys[self.position].ELEMENTS[referredItem]['description'])
                # Examination of some element in the room

            elif referredItem in zone_map_keys[self.position].ITEMS:
                print(zone_map_keys[self.position].ITEMS[referredItem]['description'])
                # Examination of some item in the room

            else:
                print('The referred item "' + referredItem + '" does not exist in this room.')
        else:
            print('You have already exhausted this zone.')

        # This function will allow the player to interact with the map

    def player_use_item(self, referredItem):
        # Decides if he will use the item from inventory or from the zone
        if referredItem == '':
            ask1 = 'What would you like to use?\n> '
            item = (input(ask1)).lower().strip()
            ask2 = 'You would like to use the ' + item + ' from where?\n> '
            print('[Zone] or [Inventory]')
            local = (input(ask2)).lower().strip()
            while local not in ['zone', 'inventory']:
                print('Write a valid location to use the item from.')
                local = (input(ask2)).lower().strip()
            if local == 'zone':
                self.player_use_item_from_zone(item)
            elif local == 'inventory':
                self.player_use_item_from_inventory(item)
        else:
            ask = 'You would like to use the ' + referredItem + ' from where?\n> '
            print('[Zone] or [Inventory]')
            local = (input(ask)).lower().strip()
            while local not in ['zone', 'inventory']:
                print('Write a valid location to use the item from.')
                print('=' * 24)
                local = (input(ask)).lower().strip()
            if local == 'zone':
                self.player_use_item_from_zone(referredItem)
            elif local == 'inventory':
                self.player_use_item_from_inventory(referredItem)

    def player_use_item_from_inventory(self, referredItem):
        # Search item in inventory
        verify_item = dict()
        for index in self.inventory['key_items']:
            if index['nameDisplay'] == referredItem:
                verify_item = index
        if verify_item == dict():
            for index in self.inventory['useful_items']:
                if index['nameDisplay'] == referredItem:
                    verify_item = index
        # Using the item
        if verify_item == dict():
            print('There is no such an item in your possession to be used here.')
        else:
            # The item will be used to solve a puzzle
            if verify_item['classification'] == 'key_item':
                if verify_item['conditionUse']():
                    print(verify_item['whenUsed'])
                    print('After used, the ' + referredItem + ' was swallow by darkness.')
                    self.inventory['key_items'].remove(verify_item)
                    zone_map_keys[self.position].zone_change(referredItem)
                    zone_map_keys[self.position].SOLVED = True
                else:
                    print('You cannot use this item here.')
            # The item will be used to change player status
            else:
                # Can be 'healing', 'remove side effect A', 'remove side effect B', 'stronger body', etc
                if verify_item['effects'] == 'healing':
                    if self.hp in [60, 70, 90]:  # HP of priest, rogue and warrior
                        print('You feel fine by now, better saved for later.')
                    else:
                        amount = randint(1, 10)
                        self.hp += amount
                        print('You use the ' + referredItem + ' to heal your body.')
                        sleep(0.3)
                        print('You feel better now.')
                        self.inventory['useful_items'].remove(verify_item)
                        zone_map_keys[self.position].zone_change(referredItem)

    def player_use_item_from_zone(self, referredItem):
        if zone_map_keys[self.position].SOLVED is False:
            if referredItem not in zone_map_keys[self.position].ELEMENTS:
                print('There is nothing like that to use here.')
            elif zone_map_keys[self.position].ELEMENTS[referredItem]['wasUsed'] is False:
                print(zone_map_keys[self.position].ELEMENTS[referredItem]['narration'])
                zone_map_keys[self.position].ELEMENTS[referredItem]['wasUsed'] = True
                zone_map_keys[self.position].zone_change(referredItem)
            else:
                print('You already use the ' + referredItem + '.')
        else:
            print('You have already done everything possible here.')

    def collect_item(self, referredItem):
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
                zone_map_keys[self.position].zone_change(item)
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
                zone_map_keys[self.position].zone_change(referredItem)

    def drop_item(self, referredItem):
        if referredItem == '':
            ask = 'What item would you like to leave behind?\n(Remember that only not important items can' \
                  'be left behind and once you dispose of one, it can never take back.\n> '
            print('=' * 24)
            self.view_inventory()
            print('=' * 24)
            item = (input(ask)).lower().strip()
            verify_item = dict()
            for index in self.inventory['key_items']:
                if index['nameDisplay'] == item:
                    verify_item = index
            if verify_item != dict():
                print('You cannot let go of such an important item.')
            else:
                item_dict = dict()
                for index in self.inventory['useful_items']:
                    if index['nameDisplay'] == item:
                        item_dict = index
                if item_dict not in self.inventory['useful_items']:
                    print('There is no such an item in your possession.')
                else:
                    self.inventory['useful_items'].remove(item_dict)
                    print('The ' + item + ' was left behind, swallowed by darkness.')
        else:
            verify_item = dict()
            for index in self.inventory['key_items']:
                if index['nameDisplay'] == referredItem:
                    verify_item = index
            if verify_item != dict():
                print('You cannot let go of such an important item.')
            else:
                item_dict = dict()
                for index in self.inventory['useful_items']:
                    if index['nameDisplay'] == referredItem:
                        item_dict = index
                if item_dict not in self.inventory['useful_items']:
                    print('There is no such an item in your possession.')
                else:
                    self.inventory['useful_items'].remove(item_dict)
                    print('The ' + referredItem + ' was left behind, swallowed by darkness.')

    def view_inventory(self):
        if self.inventory == {'key_items': list(), 'useful_items': list()}:
            print('You carried nothing.')
        else:
            for item_class in self.inventory.keys():
                print('-=' + item_class + '=-')
                for i, item in enumerate(self.inventory[item_class]):
                    print(str(i + 1) + '.' + item['nameDisplay'])
            print()


myPlayer = Player()


# Title Screen Setup
def title_screen_select():
    option = (input('> ')).lower()

    while option not in ['play', 'help', 'quit']:
        print('Enter a valid option please\n')
        option = (input('> ')).lower()

    if option == 'play':
        start_game()
    elif option == 'help':
        help_menu()

    exit()


def title_screen_display():
    clear_screen()
    print('#' * 24)
    print('Welcome to the Text RPG!')
    print('#' * 24)
    print('' * 9, '-Play-', '' * 9)
    print('' * 9, '-Help-', '' * 9)
    print('' * 9, '-Quit-', '' * 9)
    title_screen_select()


def help_menu():
    print('#' * 24)
    print('Welcome to the Text RPG!')
    print('#' * 24)
    print('-Use up, down, left, right to move-')
    print('-Type your commands to do them-')
    print("-Use 'look' to inspect something-")
    title_screen_select()


# Class Setup
class Zone(object):
    def __init__(self):
        self.ZONE_NAME = ''  # Nome da zona --> string
        self.DESCRIPTION = ''  # Descrição da zona --> string
        self.EXAMINATION = ''  # Observação detalhada da zona para evidenciar objetos presentes --> string
        self.SOLVED = False  # Condição do puzzle da zona --> bool
        self.ELEMENTS = {}  # Objetos presentes na zona --> dicionário
        self.CHANGES = {}  # Mudanças que a sala passa conforme puzzles são resolvidos --> dicionário
        self.ITEMS = {}  # Item que podem ser coletados na zona --> dicionário
        self.UP = ''  # Zona acima --> string
        self.DOWN = ''  # Zona abaixo --> string
        self.LEFT = ''  # Zona a esquerda --> string
        self.RIGHT = ''  # Zona a direita --> string

    def zone_change(self, referredItem):
        self.EXAMINATION = self.CHANGES[referredItem]


# Map Setup
# Player starts at b2 location
# Map representation (matriz):
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

# Creating the zones
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

# Setting the attributes from each zone
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
b1.ITEMS = {'bandage': {'nameDisplay': 'bandage',
                        'description': 'A dirty bandage, it can be used to stop the bleeding.',
                        'whenGrabbed': 'You bend down and grab it.',
                        'whenUsed': 'You use the bandage to recover from your wounds.',
                        'wasUsed': False,
                        'conditionUse': None,
                        'classification': 'useful_item',
                        'effects': 'healing'}
            }
b1.CHANGES = {'bandage': 'The room where you toke the bandage, it seems more empty now.'}

b2.ZONE_NAME = 'Dark room'
b2.DESCRIPTION = 'A room filled with nothing but darkness.'
b2.EXAMINATION = 'There is a small glowing key laying in the floor.'
b2.UP = 'a2'
b2.DOWN = 'c2'
b2.LEFT = 'b1'
b2.RIGHT = 'b3'
b2.ITEMS = {'small key': {'nameDisplay': 'small key',
                          'description': 'A small glowing key, it probably can be use to open a door.',
                          'whenGrabbed': 'You bend down and grab it.',
                          'whenUsed': 'You use the key to open the door, it works!',
                          'wasUsed': False,
                          'conditionUse': lambda: myPlayer.position == 'b3',
                          'classification': 'key_item',
                          'effects': None}
            }
b2.CHANGES = {'small key': 'The room where you toke the key, it seems more empty now.'}

b3.ZONE_NAME = 'Dark room'
b3.DESCRIPTION = 'A room filled with nothing but darkness.'
b3.EXAMINATION = 'There is a door here to open.'
b3.UP = 'a3'
b3.DOWN = 'c3'
b3.LEFT = 'b2'
b3.RIGHT = 'b4'
b3.CHANGES = {'small key': 'The door is laying wide open.'}
# zona.CHANGES = {'<object that caused the change>': '<new examination of the room>'}

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

# Hold of zones
zone_map_keys = {
    'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4,
    'b1': b1, 'b2': b2, 'b3': b3, 'b4': b4,
    'c1': c1, 'c2': c2, 'c3': c3, 'c4': c4,
    'd1': d1, 'd2': d2, 'd3': d3, 'd4': d4,
}


def setup_game():
    # Collect name from the player
    question = 'Enter the name of the prisoner. \n'
    timed_speech(question, 0.05)
    player_name = (input('> ')).capitalize()
    myPlayer.name = player_name

    # Collect role from the player
    question = 'Enter the role of the prisoner. \n(You can play as a warrior, rogue or priest)\n'
    timed_speech(question, 0.05)
    player_role = (input('> ')).lower()
    valid_roles = ['warrior', 'rogue', 'priest']

    while player_role not in valid_roles:
        print('Enter a valid role.\n')
        player_role = (input('> ')).lower()

    myPlayer.role = player_role
    print('The prisoner used to be a ' + player_role + '.\n')

    # Defining player stats
    if myPlayer.role == 'warrior':
        myPlayer.hp = 90
        myPlayer.amount_dices = 8

    elif myPlayer.role == 'rogue':
        myPlayer.hp = 70
        myPlayer.amount_dices = 5

    elif myPlayer.role == 'priest':
        myPlayer.hp = 60
        myPlayer.amount_dices = 3


# GAME INTERACTIVITY
def print_position():
    print('\n' + ('#' * (4 + len(myPlayer.position))))
    print('# ' + myPlayer.position.upper() + ' #')
    print('# ' + zone_map_keys[myPlayer.position].DESCRIPTION + ' #')
    print('\n' + ('#' * (4 + len(myPlayer.position))))


def prompt():
    acceptable_actions = ['go', 'move', 'travel', 'walk', 'look', 'examine', 'inspect', 'interact',
                          'quit', 'use', 'grab', 'collect', 'take', 'trow', 'drop', 'view']
    print('\n' + '=' * 24)
    print('What would you like to do?')
    action = (input('> ')).lower().strip()
    if ' ' in action:
        actionVerb = action[:action.index(' ')].strip()
        actionObj = action[action.index(' '):].strip()
    else:
        actionVerb = action
        actionObj = ''

    while actionVerb not in acceptable_actions:
        print('Unknown action, try again.\n')
        action = (input('> ')).lower().strip()
        if ' ' in action:
            actionVerb = action[:action.index(' ')].strip()
            actionObj = action[action.index(' '):].strip()
        else:
            actionVerb = action
            actionObj = ''

    if actionVerb == 'quit':
        exit()
    elif actionVerb in ['go', 'move', 'travel', 'walk']:
        myPlayer.player_move(actionObj)
    elif actionVerb in ['look', 'examine', 'inspect', 'interact']:
        myPlayer.player_examine(actionObj)
    elif actionVerb == 'use':
        myPlayer.player_use_item(actionObj)
    elif actionVerb in ['grab', 'collect', 'take']:
        myPlayer.collect_item(actionObj)
    elif actionVerb in ['trow', 'drop']:
        myPlayer.drop_item(actionObj)
    elif actionVerb == 'view':
        myPlayer.view_inventory()


# GAME FUNCTIONALITY
def main_game_loop():
    while not myPlayer.game_over:
        prompt()


def start_game():
    clear_screen()
    setup_game()

    # Play introduction
    quote = 'Welcome, ' + myPlayer.name + ' the prisoner and ex-' + myPlayer.role + '.\n'
    timed_speech(quote, 0.05)

    speech1 = 'Welcome to this fantasy world!\n'
    speech2 = 'I hope it greets you well\n'
    speech3 = 'Just make sure you do not get to lost...\n'
    speech4 = 'Heheheh...\n'

    timed_speech(speech1, 0.03)
    timed_speech(speech2, 0.03)
    timed_speech(speech3, 0.1)
    timed_speech(speech4, 0.2)

    clear_screen()
    print('#' * 20)
    print('# Let the journey begin... #')
    print('#' * 20)
    main_game_loop()


title_screen_display()
