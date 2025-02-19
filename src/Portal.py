import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self,x,y):
                super().__init__()
                self.x = x
                self.y = y
                self.image = pygame.transform.scale(pygame.image.load("./assets/exit.png").convert_alpha(),(240,60))
                self.rect = self.image.get_rect(center=(self.x,self.y))
    def draw(self, display):
        display.blit(self.image,self.rect)