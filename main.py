"""AwasDitabrak - Watch Out for the Crash!

A fun arcade game built with Python and Pygame.
Run with: python main.py
"""

import pygame
from src.core.game import Game


def main():
    pygame.init()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
