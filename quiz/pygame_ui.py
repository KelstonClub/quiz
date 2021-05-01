import pygame
import fake_db
import Maker

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
running = True
counter = 0

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((40, 40, 40))
pygame.display.set_caption("Quiz")

def game_screen(mouse_pos, counter):
    item_colour = (20, 20, 20)
    gap = 20
    num_across = 2
    num_down = 2
    question_gap = 200

    box_width = (SCREEN_WIDTH / num_across) - gap
    box_height = ((SCREEN_HEIGHT - question_gap) / num_down) - gap

    if counter == 1:
        create_buttons(box_width, box_height, mouse_pos, item_colour)

def create_buttons(box_width, box_height, mouse_pos, item_colour):
    test_button = Maker.item(0, 200, box_width, box_height, item_colour, fake_db.get_answer())
    test_button.mouse_over(mouse_pos)
    test_button.draw(screen)

while running:
    counter += 1
    pygame.display.flip()
    game_screen(pygame.mouse.get_pos(), counter)

    for event in pygame.event.get():
        pass