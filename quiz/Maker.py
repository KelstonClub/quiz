import pygame

class item:
    def __init__(self, x, y, width, height, colour, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.name = name

    def draw(self, surface):
        # surface is the window on which the rectangle should be drawn
        pygame.draw.rect(surface, self.colour, [self.x, self.y, self.width, self.height])

        if self.name != "":
            font = pygame.font.SysFont("Rockwell", 25)
            b_text = font.render(self.name, True, (255, 255, 255))
            x_coord = self.x + 10
            y_coord = self.y + (self.height / 2 - b_text.get_height() / 2)
            surface.blit(b_text, (x_coord, y_coord))

        #test
        if False:
            font = pygame.font.SysFont("Rockwell", 25)
            b_text = font.render(self.name, True, (255, 255, 255))



    def mouse_over(self, pos):
        if self.x < pos[0] < (self.x + self.width):
            if self.y < pos[1] < (self.y + self.height):
                self.colour = (14, 77, 146)
                return True

    def mouse_click(self, pos):
        if self.mouse_over(pos):
            return True