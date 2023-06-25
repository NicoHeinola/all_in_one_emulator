from enum import Enum
from helpers.ConfigManager import ConfigManager
from ui.InputActions import InputAction
from ui.pre_made_scenes.GameListScene import GameListScene
from ui.pre_made_scenes.MainMenuScene import MainMenuScene
from typing import List
import pygame
from ui.scenes.Scene import SceneLoader

pygame.joystick.init()
pygame.init()
pygame.font.init()  # you have to call this at the start,


class MainUI(SceneLoader):
    def __init__(self, displayw, displayh):
        super().__init__()

        # Window Information
        self._window: pygame.Surface = pygame.display.set_mode((displayw, displayh), pygame.RESIZABLE | pygame.SRCALPHA)

        # Set title of screen
        pygame.display.set_caption("All In One Emulator")

        # Clock
        self._window_clock = pygame.time.Clock()

        self._display_width = displayw
        self._didplay_height = displayh

        # Scenes
        main_menu = MainMenuScene(self._window, self)
        self.add_scene('main-menu', main_menu)

        game_picker_scene = GameListScene(self._window, self)
        self.add_scene('game-list', game_picker_scene)

        self.set_active_scene('main-menu')

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    stopped = True
                elif event.type == pygame.KEYDOWN:
                    print("KEYDOWN:", event.key, pygame.key.name(event.key))
                    key_code = event.key
                    if key_code in ConfigManager.get_actions_per_keycodes()['keyboard']:
                        action: str = ConfigManager.get_actions_per_keycodes()['keyboard'][key_code]
                        scene.action_performed(InputAction[action.upper()])
                elif event.type == pygame.JOYBUTTONDOWN:
                    key_code = event.button
                    if key_code in ConfigManager.get_actions_per_keycodes()['controller']:
                        action: str = ConfigManager.get_actions_per_keycodes()['controller'][key_code]
                        scene.action_performed(InputAction[action.upper()])
                    print("JOYSTICK BUTTON DOWN:", key_code)
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
