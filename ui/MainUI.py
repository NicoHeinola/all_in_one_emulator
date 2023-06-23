# Load and initialize Modules here
from ui.pre_made_scenes.MainMenu import MainMenu
from ui.scenes.SceneLoader import SceneLoader
from typing import List
import pygame
pygame.joystick.init()
pygame.init()
pygame.font.init()  # you have to call this at the start,


class MainUI(SceneLoader):
    def __init__(self, displayw, displayh):
        super().__init__()

        # Window Information
        self._window: pygame.Surface = pygame.display.set_mode((displayw, displayh), pygame.RESIZABLE)

        # Set title of screen
        pygame.display.set_caption("My Game")

        # Clock
        self._window_clock = pygame.time.Clock()

        self._display_width = displayw
        self._didplay_height = displayh

        # Scenes
        main_menu = MainMenu(self._window)
        self.add_scene('main_menu', main_menu)

        self.set_active_scene('main_menu')

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
                    quit()
                elif event.type == pygame.KEYDOWN:
                    print("KEYDOWN:", event.key, pygame.key.name(event.key))
                    scene.keyboard_key_down(event.key)
                elif event.type == pygame.JOYBUTTONDOWN:
                    button = event.button
                    print("JOYSTICK BUTTON DOWN:", button)
                    scene.joystick_key_down(button)
                elif event.type == pygame.WINDOWRESIZED:
                    self.build_scenes()

            scene.update()
            scene.draw()

            pygame.display.update()
            self._window_clock.tick(60)


if __name__ == '__main__':
    main_ui = MainUI(1280, 720)
    main_ui.run()
