from enum import Enum
from helpers.ConfigManager import ConfigManager
from ui.InputActions import InputAction
from ui.pre_made_scenes.GameDownloadScene import GameDownloadScene
from ui.pre_made_scenes.GameListScene import GameListScene
from ui.pre_made_scenes.MainMenuScene import MainMenuScene
from typing import List
import pygame
from ui.scenes.Scene import ActionFrom, SceneLoader
pygame.joystick.init()
pygame.init()
pygame.font.init()  # you have to call this at the start,


class MainUI(SceneLoader):
    def __init__(self, displayw, displayh):
        super().__init__()

        # Window Information
        self._window: pygame.Surface = pygame.display.set_mode((displayw, displayh), pygame.RESIZABLE | pygame.SRCALPHA | pygame.HWSURFACE | pygame.DOUBLEBUF)

        # Set title of screen
        pygame.display.set_caption("All In One Emulator")

        # Clock
        self._window_clock = pygame.time.Clock()

        self._display_width = displayw
        self._didplay_height = displayh

        # Inputs
        self._delay_until_hold: int = 20  # How long (in frames) to press 1 key until it starts to register it as holding
        self._delay_until_hold_count: int = 0
        self._hold_delay: int = 1  # How many frames are between hold inputs
        self._hold_delay_count: int = 0
        self._hold_action: InputAction = None

        # Scenes
        main_menu = MainMenuScene(self._window, self)
        self.add_scene('main-menu', main_menu)

        game_picker_scene = GameListScene(self._window, self)
        self.add_scene('game-list', game_picker_scene)

        game_download_scene = GameDownloadScene(self._window, self)
        self.add_scene('game-download', game_download_scene)

        self.set_active_scene('game-download')

    def _reset_hold(self) -> None:
        self._hold_delay_count: int = 0
        self._delay_until_hold_count: int = 0
        self._hold_action: InputAction = None
        self._hold_action_from: ActionFrom = None

    def run(self):
        # Put all variables up here
        stopped = False

        self.build_scenes()

        for joystick_index in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(joystick_index)  # Get the first joystick
            joystick.init()
            print("Joystick detected:", joystick.get_name())

        while stopped == False:
            scene = self.get_active_scene()

            if self._hold_action is not None:
                if self._delay_until_hold_count < self._delay_until_hold:
                    self._delay_until_hold_count += 1
                elif self._hold_delay_count < self._hold_delay:
                    self._hold_delay_count += 1
                else:
                    self._hold_delay_count = 0
                    print("Performing!", self._hold_action)
                    scene.action_performed(self._hold_action, self._hold_action_from)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    stopped = True
                elif event.type == pygame.MOUSEMOTION:
                    mouse_position = pygame.mouse.get_pos()
                    scene.mouse_moved(mouse_position[0], mouse_position[1])
                    # print(f"Mouse {mouse_position[0]} {mouse_position[1]}")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"MOUSE BUTTON DOWN: {event.pos}, {event.button}")
                    key_code = event.button
                    if key_code in ConfigManager.get_actions_per_keycodes()['mouse']:
                        action: str = ConfigManager.get_actions_per_keycodes()['mouse'][key_code]
                        input_action: InputAction = InputAction[action.upper()]
                        scene.mouse_action_performed(input_action)
                elif event.type == pygame.KEYDOWN:
                    print("KEYDOWN:", event.key, pygame.key.name(event.key), event.unicode)
                    key_code = event.key
                    scene.keyboard_key_down(key_code, event.unicode)
                    if key_code in ConfigManager.get_actions_per_keycodes()['keyboard']:
                        action: str = ConfigManager.get_actions_per_keycodes()['keyboard'][key_code]
                        input_action: InputAction = InputAction[action.upper()]
                        self._hold_action = input_action
                        self._hold_action_from = ActionFrom.KEYBOARD
                        scene.action_performed(input_action, ActionFrom.KEYBOARD)
                elif event.type == pygame.KEYUP:
                    self._reset_hold()
                elif event.type == pygame.JOYBUTTONDOWN:
                    print("JOYSTICK BUTTON DOWN:", key_code)
                    key_code = event.button
                    scene.joystick_key_down(key_code)
                    if key_code in ConfigManager.get_actions_per_keycodes()['controller']:
                        action: str = ConfigManager.get_actions_per_keycodes()['controller'][key_code]
                        input_action: InputAction = InputAction[action.upper()]
                        self._hold_action = input_action
                        self._hold_action_from = ActionFrom.CONTROLLER
                        scene.action_performed(input_action, ActionFrom.CONTROLLER)
                elif event.type == pygame.JOYBUTTONUP:
                    self._reset_hold()
                elif event.type == pygame.WINDOWRESIZED:
                    self.build_scenes()

            if not stopped:
                scene.update()
                scene.draw()
                pygame.display.update()
                self._window_clock.tick(60)


if __name__ == '__main__':
    main_ui = MainUI(1280, 720)
    main_ui.run()
