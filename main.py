# Simple pygame program

# Import and initialize the pygame library
import pygame
import spit
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
pygame.init()

game = spit.Game()
# Set up the drawing window
screen = pygame.display.set_mode([500, 500])
players = pygame.sprite.Group()
cards = pygame.sprite.Group()
players.add(game.player1, game.player2)
cards.add(game.cards)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()