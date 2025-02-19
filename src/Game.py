import pygame,time,sys,random
from Player import Player
from Enemy import Enemy
from Tile import Tile
from Portal import Portal
from Bullet import Bullet

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption("Doodle Boodle")

class Game():
    _instance = None
    high_scores = []
    dx, dy = 332,720
    display = pygame.display.set_mode((dx,dy))
    bg= pygame.image.load("./assets/bg.png")
    bg2 = pygame.image.load("./assets/bg.png")
    clock = pygame.time.Clock()	
    gravity = 0.2
    running = True
    bg_y = 0
    bg2_y = -1180
    buttons_x = 50
    buttons_y = 300
    font = pygame.font.SysFont(None,25)
    end_font = pygame.font.SysFont(None,50)
    cover = pygame.image.load("./assets/cover.png").convert_alpha()
    score_im = pygame.transform.scale2x(pygame.image.load("./assets/score.png").convert_alpha())
    button_start = pygame.transform.scale(pygame.image.load("./assets/play.png").convert_alpha(),(240,60))
    button_start_rect = button_start.get_rect()
    button_start_rect.topleft = (buttons_x,buttons_y)

    button_exit = pygame.transform.scale(pygame.image.load("./assets/exit.png").convert_alpha(),(240,60))
    button_exit_rect = button_exit.get_rect()
    button_exit_rect.topleft = (buttons_x,buttons_y+150)

    button_edge = pygame.transform.scale(pygame.image.load("./assets/bullets.png").convert_alpha(),(240,60))

    shoot_sound = pygame.mixer.Sound("./assets/shoot.ogg")
    jump_sound = pygame.mixer.Sound("./assets/jump.ogg")
    walk_sound = pygame.mixer.Sound("./assets/walk.ogg")
    win_sound = pygame.mixer.Sound("./assets/game_won.ogg")
    collision_sound = pygame.mixer.Sound("./assets/collision.ogg")
    lose_sound = pygame.mixer.Sound("./assets/lose.ogg")

    tile_collision_group = pygame.sprite.Group()
    tile_group = [Tile(150,550)]
    tile_collision_group.add(tile_group[0])
    enemy_collision_group = pygame.sprite.Group()
    enemy_group = []
    platform = 550
    enemy_y = 300
    score = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

    with open("scores.txt","r") as file:
        saved_scores = file.readlines()
        for line in saved_scores:

            line = line.rstrip('\n')
            high_scores.append(line)

    def save_score(self, mode, score):
        with open("scores.txt", "r") as saved:
            list_of_lines = saved.readlines()
        
        if self.score > int(list_of_lines[mode]):
            list_of_lines[mode] = str(score) + "\n"
        
        with open("scores.txt", "w") as saved:
            saved.writelines(list_of_lines)
        
        self.high_scores.clear()
        self.high_scores.extend(line.strip() for line in list_of_lines)
        saved.close()
    
    def gameloop(self):
        player = Player(150,450)
        bullet1 = Bullet(player.rect.centerx,player.rect.centery,player.rect.center)
        
        platform = 550
        enemy_y = 300

        self.score = 0
        pygame.mixer.Sound.set_volume(self.shoot_sound, 0.1)
        pygame.mixer.Sound.set_volume(self.jump_sound, 0.2)
        pygame.mixer.Sound.set_volume(self.win_sound, 0.3)
        pygame.mixer.Sound.set_volume(self.collision_sound, 0.1)
        pygame.mixer.Sound.set_volume(self.lose_sound, 0.4)
        
        for i in range(0,500):
            platform -= 100
            self.tile_group.append(Tile(random.randint(20,232),platform))
        final = platform
        final_platform = Portal(self.dx/2,final)
        final_platform_sprite = pygame.sprite.GroupSingle([final_platform])
        for i in range(0,165):
                self.enemy_group.append(Enemy(random.randint(20,232),enemy_y))
                enemy_y -= 300
        for tile in self.tile_group:
                self.tile_collision_group.add(tile)
        for enemy in self.enemy_group:
                self.enemy_collision_group.add(enemy)
        
        i = 0
        while self.running:
                self.display.blit(self.bg,(0,self.bg_y))
                self.display.blit(self.bg2,(0,self.bg2_y))
                if player.rect.centery <= self.dy/2:
                        self.bg_y += 5
                        self.bg2_y += 5
                        for tile in self.tile_group:
                                tile.rect.top += 5
                        for enemy in self.enemy_group:
                                enemy.rect.top += 5
                        final_platform.rect.centery += 5
                final_shot = pygame.sprite.spritecollide(bullet1,final_platform_sprite,False,pygame.sprite.collide_rect)
                if final_shot:
                    pygame.mixer.Sound.play(self.win_sound)
                    self.end_screen()
                if self.bg_y >= 1180:
                        self.bg_y = 0
                if self.bg2_y >= 0:
                        self.bg2_y = -1180
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                self.running = False
                                pygame.quit()
                                sys.exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                        player.left = True
                        player.right= False
                        player.standing = False
                        player.rect.centerx -= 5
                        i += 1
                        if i % 10 == 0:
                            pygame.mixer.Sound.play(self.walk_sound)
                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                        player.left = False
                        player.right= True
                        player.standing = False
                        player.rect.centerx += 5
                        i += 1
                        if i % 10 == 0:
                            pygame.mixer.Sound.play(self.walk_sound)
                else:
                        i = 0
                        player.standing = True
                        player.left = False
                        player.right = False
                if keys[pygame.K_SPACE]:
                        if player.is_on_floor: # check if player is allowd to jump (is on floor)
                            player.jump = 10 # set any value for jumping
                            player.is_on_floor = False # disable floor check
                            pygame.mixer.Sound.play(self.jump_sound)
                if keys[pygame.K_c] and bullet1.state == "ready":
                        bullet1.rect.center = player.rect.center
                        pygame.mixer.Sound.play(self.shoot_sound)
                        bullet1.state = "fired"
                if player.sound:
                            pygame.mixer.Sound.play(self.jump_sound)
                            player.sound = False        
                
                player.check_collision(self.tile_group)
                player.update()
                
                final_platform.draw(self.display)
                player.draw(self.display)
                if bullet1.state == "fired":
                        bullet1.draw(self.display)
                enemy.draw(self.display)
                
                #PLAYER
                if player.rect.left > self.dx:
                        player.rect.right = 0
                elif player.rect.right < 0:
                        player.rect.left = self.dx
                if player.rect.bottom >= self.dy:
                        self.save_score(0,self.score)
                        self.end_screen()
                
                #TILES
                for tile in self.tile_group:
                        tile.draw(self.display)
                        if tile.rect.top >= self.dy:
                                self.tile_group.remove(tile)
                                self.score += 10
                self.text("Score: ",(255,255,255),210,self.dy - 30)
                self.text(str(self.score),(255,255,255),270,self.dy - 30)
                if final_platform.rect.centery >= 50:
                    final_platform.rect.centery = 50
                    self.end_text("YOU WON!",(0,0,0),75,140)
                
                #ENEMY
                for enemy in self.enemy_collision_group:
                        enemy.draw(self.display)
                        if len(self.enemy_collision_group) <= 0:
                            self.enemy_collision_group.empty()
                        enemy.rect.centerx += enemy.change_x
                        if enemy.rect.left <= 0:
                                enemy.change_x = 2
                        if enemy.rect.right >= self.dx:
                                enemy.change_x = -2
                
                if bullet1.state == "fired":
                        hit = pygame.sprite.spritecollide(bullet1,self.enemy_collision_group,True,pygame.sprite.collide_rect)
                        if hit:
                                bullet1.rect.center = player.rect.center
                                bullet1.state = "ready"
                                self.score += 100
                                pygame.mixer.Sound.play(self.collision_sound)
                collided = pygame.sprite.spritecollide(player,self.enemy_collision_group,False)
                if collided:
                        self.save_score(0,self.score)
                        pygame.mixer.Sound.play(self.lose_sound)
                        self.end_screen()
                #BULLET
                if bullet1.state == "fired":
                        bullet1.shoot()
                        bullet1.rect.centery -= 5
                if bullet1.rect.centery <= 0:
                        bullet1.rect.center = player.rect.center
                        bullet1.state = "ready"
                
                self.clock.tick(60)
                pygame.display.update()

    def main_menu(self):
        pygame.mouse.set_visible(True)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
                    pygame.quit()
                    sys.exit(0)
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                clicked = False
                self.display.fill((107,188,255))
                self.display.blit(self.cover,(0,0))
                self.text("High Score: ",(0,0,0),70,220)
                self.text(str(self.high_scores[0]),(0,0,0),180,220)
                self.display.blit(self.button_start,(self.buttons_x,self.buttons_y))
                self.display.blit(self.button_exit,(self.buttons_x,self.buttons_y+150))
                self.text("Move with A-D/RIGHT-LEFT arrow keys",(0,0,0),10,550)
                self.text("Jump with SPACE, shoot with C",(0,0,0),30,580)
                
                buttons = [self.button_start_rect,self.button_exit_rect]
        
                for button in buttons:
                    if button[0] < mouse[0] < button[0] + button[2]:
                        if button[1] < mouse[1] < button[1] +button[3]:
                            self.display.blit(self.button_edge,(button[0],button[1]))
                            if click[0] == 1:
                                clicked = True
                                if button[1] == self.button_start_rect[1]: self.gameloop()
                                if button[1] == self.button_exit_rect[1]: pygame.quit(); sys.exit(0);
                            
                self.clock.tick(60)
                pygame.display.update()

    def end_screen(self):
        self.tile_collision_group.empty()
        self.enemy_collision_group.empty()
        self.tile_group.clear()
        self.tile_group = [Tile(150,550)]
        self.enemy_group.clear()
        while True:
            self.display.fill((107,188,255))
            self.display.blit(self.cover,(0,0))
            self.display.blit(self.score_im,(10,200))
            self.display.blit(self.button_start,(self.buttons_x,self.buttons_y))
            self.display.blit(self.button_exit,(self.buttons_x,self.buttons_y+150))
            self.end_text(str(self.score),(0,0,0),230,234)
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
                    pygame.quit()
                    sys.exit(0)
                
        
    ##            end_text(str(score),(0,0,0),400,100)
            buttons = [self.button_start_rect,self.button_exit_rect]
            for button in buttons:
                if button[0] < mouse[0] < button[0] + button[2]:
                    if button[1] < mouse[1] < button[1] +button[3]:
                        self.display.blit(self.button_edge,(button[0],button[1]))
                        if click[0] == 1:
                            if button[1] == self.button_start_rect[1]: self.gameloop()
                            if button[1] == self.button_exit_rect[1]: pygame.quit(); sys.exit(0);
            
            self.clock.tick(60)
            pygame.display.update()
    
    def text(self, msg,color,x,y):
        text = self.font.render(msg,True,color)
        self.display.blit(text,[x,y])

    def end_text(self, msg,color,x,y):
        text = self.end_font.render(msg,True,color)
        self.display.blit(text,[x,y])