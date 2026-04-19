"""
Main entry point for AwasDitabrak game.

Run this file to start the game:
    python main.py
"""

import pygame
from game import Game


def main():
    """Initialize pygame and run the game."""
    pygame.init()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
