import pygame

class Flash(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()
        self.passed = False
        self.image = pygame.image.load("Flash.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
