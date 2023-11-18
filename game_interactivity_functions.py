# This file contains all the functions responsible to represent all the game interactivity from the class
# and void instances

# A game interactivity function is a code function that requires an input from the user to operate

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

