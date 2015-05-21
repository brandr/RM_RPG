import pygame
from pygame import *
from gamemanager import GameManager

def main():
	pygame.init()
	pygame.font.init()
	manager = GameManager()
	manager.run_game()

if __name__ == "__main__": main()