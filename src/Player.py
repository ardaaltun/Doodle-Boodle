import pygame

class Player(pygame.sprite.Sprite):
        image_stand = pygame.image.load("./assets/standing.png")
        image_left = [pygame.image.load("./assets/left1.png"),pygame.image.load("./assets/left2.png"),pygame.image.load("./assets/left3.png"),pygame.image.load("./assets/left4.png")]
        image_right = [pygame.image.load("./assets/right1.png"),pygame.image.load("./assets/right2.png"),pygame.image.load("./assets/right3.png"),pygame.image.load("./assets/right4.png")]
        frame = 0
        def __init__(self,x,y):
                super().__init__()
                self.x = x
                self.y = y
                self.image = self.image_stand.convert_alpha()
                self.rect = self.image.get_rect(center=(self.x,self.y))
                self.jump = 0
                self.gravity = 0
                self.is_on_floor = False
                self.standing = True
                self.left = False
                self.right = False
                self.face = "down"
                self.anim_speed = 0.5
                self.sound = False
        def check_collision(self, tile_group):
                self.is_on_floor = False
                for tile in tile_group:
                        if self.rect.colliderect(tile.rect):
                                if self.rect.bottom <= tile.rect.bottom:
                                        if self.jump <= 0:
                                                self.rect.bottom = tile.rect.top +1
                                                self.is_on_floor = True
                                                self.gravity = 0
        def update(self):
                if not self.jump:
                        if not self.is_on_floor:
                                self.rect.y += self.gravity
                                self.gravity += 0.5
                else:
                        self.rect.y -= self.jump
                        self.jump -= 0.5
         
        def draw(self, display):
                if self.left:
                    self.face = "left"
                    self.right = False
                    self.standing = False
                    self.image = self.image_left[int(self.frame)].convert_alpha()
                    self.frame += self.anim_speed
                    if int(self.frame) >= len(self.image_left):
                        self.frame = 0
                elif self.right:
                    self.face = "right"
                    self.left = False
                    self.standing = False
                    self.image = self.image_right[int(self.frame)].convert_alpha()
                    self.frame += self.anim_speed
                    if int(self.frame) >= len(self.image_right):
                        self.frame = 0
                elif self.standing:
                    self.left = False
                    self.right = False
                    if self.face == "down":
                        self.image = self.image_stand.convert_alpha()
                    elif self.face == "left":
                        self.image = self.image_left[0].convert_alpha()
                    elif self.face == "right":
                        self.image = self.image_right[0].convert_alpha()
                    self.frame = 0
                display.blit(self.image,self.rect)
