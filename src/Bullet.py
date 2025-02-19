import pygame

class Bullet(pygame.sprite.Sprite):
        def __init__(self,x,y,center):
                super().__init__()
                self.x = x
                self.y = y
                self.image = pygame.image.load("./assets/bullet.png").convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.state = "ready"
        def shoot(self):
                self.state = "fired"
        def draw(self, display):
                if self.state == "fired":
                        display.blit(self.image,self.rect)
