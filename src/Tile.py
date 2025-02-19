import pygame

class Tile(pygame.sprite.Sprite):
        def __init__(self,x,y):
                super().__init__()
                self.x = x
                self.y = y
                self.image = pygame.image.load("./assets/platform.png").convert_alpha()
                self.rect = self.image.get_rect(center=(self.x,self.y))
                self.fall = 0
        def draw(self, display):
                display.blit(self.image,self.rect)