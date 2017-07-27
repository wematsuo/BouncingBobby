import pygame

class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.passed = False
        self.image = pygame.image.load("Bob.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.speed = speed
        self.rect = pygame.Rect(x, y, width, height)
