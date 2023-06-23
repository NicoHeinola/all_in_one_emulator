# Load and initialize Modules here
from typing import List
import pygame

from scenes.SceneLoader import SceneLoader
from pre_made_scenes.MainMenu import MainMenu
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

        while stopped == False:
            scene = self.get_active_scene()
            # Event Tasking
            # Add all your event tasking things here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    stopped = True
                elif event.type == pygame.WINDOWRESIZED:
                    self.build_scenes()

            scene.update()
            scene.draw()

            pygame.display.update()
            self._window_clock.tick(60)


if __name__ == '__main__':
    main_ui = MainUI(1280, 720)
    main_ui.run()
