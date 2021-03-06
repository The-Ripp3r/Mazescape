# Import libraries
import os
from random import randrange
import pygame
import pygameMenu
from settings import *

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
CREATORS = ['Carrie Laber-Smith: {0}'.format('Narrative Designer'), 
            'Kevin Jiang: {0}'.format('Chief Designer'), 
            'Edward Rivera (aka Jack The-Ripp3r): {0}'.format('Chief Engineer'), 
            'Michelle Tan: {0}'.format('Project Manager')]
COLOR_BACKGROUND = (0, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MODE = ['1']
MENU_BACKGROUND_COLOR = LIGHTGREY
WINDOW_SIZE = (WIDTH, HEIGHT)

clock = None

# noinspection PyTypeChecker
main_menu = None  # type: pygameMenu.Menu

# noinspection PyTypeChecker
surface = None  # type: pygame.SurfaceType

paused = False
game_function = None


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def change_mode(value, color):
    """
    Change the mode of the game.
    :param value: Tuple containing the data of the selected object
    :type value: tuple
    :return: None
    """
    MODE[0] = value[0]


def play_function(game_function, mode):
    """
    Main game function.
    :param mode: mode of the game
    :type mode: list
    :param font: Pygame font
    :type font: pygame.font.FontType
    :param test: Test method, if true only one loop is allowed
    :type test: bool
    :return: None
    """
    # Define globals
    global main_menu

    # Reset main menu and disable
    # You also can set another menu, like a 'pause menu', or just use the same
    # main_menu as the menu that will check all your input.
    main_menu.disable()
    print(MODE[0])
    mode=MODE[0]
    MODE[0]='1'
    game_function(mode)

def main_background():
    """
    Function used by menus, draw on background while menu is active.
    :return: None
    """
    global surface
    surface.fill(COLOR_BACKGROUND)


def no():
    pass


def unpause(pause_menu):
    global paused
    paused = not paused
    pause_menu.disable()


def pause_menu():
    pause_menu = pygameMenu.Menu(surface,
                                bgfun=no,
                                back_box=False,
                                color_selected=DARKRED,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color_title=MENU_BACKGROUND_COLOR,
                                menu_color = COLOR_WHITE,
                                menu_height=int(WINDOW_SIZE[1] * 0.5),
                                menu_width=int(WINDOW_SIZE[0] * 0.5),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Paused',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    pause_menu.add_button('Resume',  # When pressing return -> play(mode[0], font)
                         unpause,
                         pause_menu)
    pause_menu.add_button('Quit', run_menu)

    global paused
    while paused:
        # Tick
        clock.tick(FPS)

        # Main menu
        pause_menu.mainloop()

        # Flip surface
        pygame.display.flip()


def win_menu():
    win_menu = pygameMenu.TextMenu(surface,
                                bgfun=no,
                                back_box=False,
                                color_selected=DARKRED,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=24,
                                menu_alpha=100,
                                font_size_title=30,
                                font_title=pygameMenu.font.FONT_BEBAS,
                                menu_color_title=MENU_BACKGROUND_COLOR,
                                menu_color=COLOR_WHITE,
                                menu_height=int(WINDOW_SIZE[1] * 0.5),
                                menu_width=int(WINDOW_SIZE[0] * 0.5),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                text_color=COLOR_BLACK,
                                text_fontsize=20,
                                text_align=pygameMenu.locals.ALIGN_CENTER,
                                title='You Won!',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
                                
    win_menu.add_line("Congratulations!")
    win_menu.add_line("You beat the game :)")
    win_menu.add_button('Quit', run_menu)

    while True:
        # Tick
        clock.tick(FPS)

        # Main menu
        win_menu.mainloop()

        # Flip surface
        pygame.display.flip()


def run_menu():
    """
    Main program.
    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus
    # -------------------------------------------------------------------------

    # Play menu
    global game_function
    play_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                back_box=False,
                                color_selected=DARKRED,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color_title=MENU_BACKGROUND_COLOR,
                                menu_color = COLOR_WHITE,
                                menu_height=int(WINDOW_SIZE[1] * 0.7),
                                menu_width=int(WINDOW_SIZE[0] * 0.7),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Play menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    play_menu.add_button('Start',  # When pressing return -> play(mode[0], font)
                         play_function,
                         game_function,
                         MODE[0])
    play_menu.add_selector('Select Mode',
                           [('1', GREEN),
                            ('2', YELLOW)],
                           onchange=change_mode,
                           selector_id='select_mode')
    play_menu.add_button('Back', pygameMenu.events.BACK)

    # About menu
    about_menu = pygameMenu.TextMenu(surface,
                                     bgfun=main_background,
                                     back_box=False,
                                     color_selected=DARKRED,
                                     font=pygameMenu.font.FONT_BEBAS,
                                     font_color=COLOR_BLACK,
                                     menu_alpha=100,
                                     font_size_title=30,
                                     font_title=pygameMenu.font.FONT_BEBAS,
                                     menu_color_title=MENU_BACKGROUND_COLOR,
                                     menu_color=COLOR_WHITE,
                                     menu_height=int(WINDOW_SIZE[1] * 0.6),
                                     menu_width=int(WINDOW_SIZE[0] * 0.6),
                                     onclose=pygameMenu.events.DISABLE_CLOSE,
                                     option_shadow=False,
                                     text_color=COLOR_BLACK,
                                     text_fontsize=20,
                                     title='Creators',
                                     window_height=WINDOW_SIZE[1],
                                     window_width=WINDOW_SIZE[0]
                                     )
    for m in CREATORS:
        about_menu.add_line(m)
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_button('Return to menu', pygameMenu.events.BACK)

    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                back_box=False,
                                color_selected=DARKRED,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color_title=MENU_BACKGROUND_COLOR,
                                menu_color=WHITE,
                                menu_height=int(WINDOW_SIZE[1] * 0.6),
                                menu_width=int(WINDOW_SIZE[0] * 0.6),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Welcome...',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )

    main_menu.add_button('Play', play_menu)
    main_menu.add_button('About', about_menu)
    main_menu.add_button('Quit', pygameMenu.events.EXIT)

    # Configure main menu
    main_menu.set_fps(FPS)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        main_menu.mainloop(events)

        # Flip surface
        pygame.display.flip()
