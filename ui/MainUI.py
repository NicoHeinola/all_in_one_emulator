# Load and initialize Modules here
import pygame

from scenes.TestScene import TestScene
pygame.init()


class MainUI(object):
    def __init__(self, displayw, displayh):
        # Window Information
        self._window = pygame.display.set_mode((displayw, displayh))

        # Clock
        self._window_clock = pygame.time.Clock()

        self._display_width = displayw
        self._didplay_height = displayh

    def run(self):
        # Put all variables up here
        stopped = False

        test_scene = TestScene(self._window)

        while stopped == False:
            # Event Tasking
            # Add all your event tasking things here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    stopped = True

            # Remember to update your clock and display at the end
            pygame.display.update()
            self._window_clock.tick(60)

            test_scene.draw()
            test_scene.update()


if __name__ == '__main__':
    main_ui = MainUI(800, 600)
    main_ui.run()
