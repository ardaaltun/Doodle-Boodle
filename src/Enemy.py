import pygame

class Enemy(pygame.sprite.Sprite):
        def __init__(self,x,y):
                super().__init__()
                self.x = x
                self.y = y
                self.image = pygame.image.load("./assets/enemy.png").convert_alpha()
                self.rect = self.image.get_rect(center=(self.x,self.y))
                self.change_x = 2
        def draw(self, display):
                display.blit(self.image,self.rect)
                
