import pygame,time,sys,random
high_scores = []

with open("scores.txt","r") as file:
    saved_scores = file.readlines()
    for line in saved_scores:

        line = line.rstrip('\n')
        high_scores.append(line)
        
def save_score(mode,score):
    saved = open("scores.txt", "r",1)
    list_of_lines = saved.readlines()
    
    if score > int(list_of_lines[mode]):
        list_of_lines[mode] = str(score) + "\n"
    saved = open("scores.txt", "w")
    saved.writelines(list_of_lines)
    high_scores.clear()
    for line in list_of_lines:
        line = line.rstrip("\n")
        high_scores.append(line)
    
        
    saved.close()
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
dx, dy = 332,720
display = pygame.display.set_mode((dx,dy))
bg= pygame.image.load("bg.png")
bg2 = pygame.image.load("bg.png")
pygame.display.set_caption("Doodle Boodle")
clock = pygame.time.Clock()	
gravity = 0.2
running = True
bg_y = 0
bg2_y = -1180
buttons_x = 50
buttons_y = 300
font = pygame.font.SysFont(None,25)
end_font = pygame.font.SysFont(None,50)
cover = pygame.image.load("cover.png").convert_alpha()
score_im = pygame.transform.scale2x(pygame.image.load("score.png").convert_alpha())
button_start = pygame.transform.scale(pygame.image.load("play.png").convert_alpha(),(240,60))
button_start_rect = button_start.get_rect()
button_start_rect.topleft = (buttons_x,buttons_y)

button_exit = pygame.transform.scale(pygame.image.load("exit.png").convert_alpha(),(240,60))
button_exit_rect = button_exit.get_rect()
button_exit_rect.topleft = (buttons_x,buttons_y+150)

button_edge = pygame.transform.scale(pygame.image.load("bullets.png").convert_alpha(),(240,60))

shoot_sound = pygame.mixer.Sound("shoot.ogg")
jump_sound = pygame.mixer.Sound("jump.ogg")
walk_sound = pygame.mixer.Sound("walk.ogg")
win_sound = pygame.mixer.Sound("game_won.ogg")
collision_sound = pygame.mixer.Sound("collision.ogg")
lose_sound = pygame.mixer.Sound("lose.ogg")
pygame.mixer.Sound.set_volume(shoot_sound, 0.1)
pygame.mixer.Sound.set_volume(jump_sound, 0.2)
pygame.mixer.Sound.set_volume(win_sound, 0.3)
pygame.mixer.Sound.set_volume(collision_sound, 0.1)
pygame.mixer.Sound.set_volume(lose_sound, 0.4)


def text(msg,color,x,y):
    text = font.render(msg,True,color)
    display.blit(text,[x,y])
def end_text(msg,color,x,y):
    text = end_font.render(msg,True,color)
    display.blit(text,[x,y])
class Player(pygame.sprite.Sprite):
        image_stand = pygame.image.load("standing.png")
        image_left = [pygame.image.load("left1.png"),pygame.image.load("left2.png"),pygame.image.load("left3.png"),pygame.image.load("left4.png")]
        image_right = [pygame.image.load("right1.png"),pygame.image.load("right2.png"),pygame.image.load("right3.png"),pygame.image.load("right4.png")]
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
        def check_collision(self):
##                print(self.rect.bottom,tile1.rect.top)
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
##                        self.sound = True
                        self.rect.y -= self.jump
                        self.jump -= 0.5
##                        if self.sound:
##                            if self.
##                            pygame.mixer.Sound.play(jump_sound)
##                            self.sound = False
##        def play_sound(self):
##            pygame.mixer.Sound.play(jump_sound)
##            
        def draw(self):
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

class Bullet(pygame.sprite.Sprite):
        def __init__(self,x,y,center):
                super().__init__()
                self.x = x
                self.y = y
                self.image = pygame.image.load("bullet.png").convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.state = "ready"
        def shoot(self):
                self.state = "fired"
        def draw(self):
                if self.state == "fired":
                        display.blit(self.image,self.rect)

class Enemy(pygame.sprite.Sprite):
        def __init__(self,x,y):
                super().__init__()
                self.x = x
                self.y = y
                self.image = pygame.image.load("enemy.png").convert_alpha()
                self.rect = self.image.get_rect(center=(self.x,self.y))
                self.change_x = 2
        def draw(self):
                display.blit(self.image,self.rect)
                

class Tiles(pygame.sprite.Sprite):
        def __init__(self,x,y):
                super().__init__()
                self.x = x
                self.y = y
##                self.image = pygame.Surface((50,50))
                self.image = pygame.image.load("platform.png").convert_alpha()
                self.rect = self.image.get_rect(center=(self.x,self.y))
                self.fall = 0
        def draw(self):
##                pygame.draw.rect(display,(0,0,0),self.rect)
                display.blit(self.image,self.rect)
##        def add(self):
class Portal(pygame.sprite.Sprite):
    def __init__(self,x,y):
                super().__init__()
                self.x = x
                self.y = y
                self.image = pygame.transform.scale(pygame.image.load("exit.png").convert_alpha(),(240,60))
                self.rect = self.image.get_rect(center=(self.x,self.y))
    def draw(self):
        display.blit(self.image,self.rect)
tile_collision_group = pygame.sprite.Group()
tile_group = [Tiles(150,550)]
tile_collision_group.add(tile_group[0])
enemy_collision_group = pygame.sprite.Group()
enemy_group = []
platform = 550
enemy_y = 300
score = 0


def main_menu():
    
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
            display.fill((107,188,255))
            display.blit(cover,(0,0))
            text("High Score: ",(0,0,0),70,220)
            text(str(high_scores[0]),(0,0,0),180,220)
            display.blit(button_start,(buttons_x,buttons_y))
            display.blit(button_exit,(buttons_x,buttons_y+150))
            text("Move with A-D/RIGHT-LEFT arrow keys",(0,0,0),10,550)
            text("Jump with SPACE, shoot with C",(0,0,0),30,580)
            
            buttons = [button_start_rect,button_exit_rect]
      
            for button in buttons:
                if button[0] < mouse[0] < button[0] + button[2]:
                    if button[1] < mouse[1] < button[1] +button[3]:
                        display.blit(button_edge,(button[0],button[1]))
                        if click[0] == 1:
                            clicked = True
                            if button[1] == button_start_rect[1]: main()
                            if button[1] == button_exit_rect[1]: pygame.quit(); sys.exit(0);
                        
            clock.tick(60)
            pygame.display.update()


def end_screen():
    global tile_group,enemy_group
    tile_collision_group.empty()
    enemy_collision_group.empty()
    tile_group.clear()
    tile_group = [Tiles(150,550)]
    enemy_group.clear()
    while True:
        display.fill((107,188,255))
        display.blit(cover,(0,0))
        display.blit(score_im,(10,200))
        display.blit(button_start,(buttons_x,buttons_y))
        display.blit(button_exit,(buttons_x,buttons_y+150))
        end_text(str(score),(0,0,0),230,234)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                pygame.quit()
                sys.exit(0)
            
    
##            end_text(str(score),(0,0,0),400,100)
        buttons = [button_start_rect,button_exit_rect]
        for button in buttons:
            if button[0] < mouse[0] < button[0] + button[2]:
                if button[1] < mouse[1] < button[1] +button[3]:
                    display.blit(button_edge,(button[0],button[1]))
                    if click[0] == 1:
                        if button[1] == button_start_rect[1]: main()
                        if button[1] == button_exit_rect[1]: pygame.quit(); sys.exit(0);
        
        clock.tick(60)
        pygame.display.update()
def main():
        global score
        
##        
        player = Player(150,450)
        bullet1 = Bullet(player.rect.centerx,player.rect.centery,player.rect.center)
        
        platform = 550
        enemy_y = 300
        score = 0
        
        
        for i in range(0,500):
            platform -= 100
            tile_group.append(Tiles(random.randint(20,232),platform))
        final = platform
        final_platform = Portal(dx/2,final)
        final_platform_sprite = pygame.sprite.GroupSingle([final_platform])
##        print(-49450)
        for i in range(0,165):
                enemy_group.append(Enemy(random.randint(20,232),enemy_y))
                enemy_y -= 300
        ##print(len(enemy_group))
        for tile in tile_group:
                tile_collision_group.add(tile)
        for enemy in enemy_group:
                enemy_collision_group.add(enemy)
        
        global running,bg_y,bg2_y
        i = 0
        while running:
##                print(final_platform.rect.center)
##                print(final,platform)
                display.blit(bg,(0,bg_y))
                display.blit(bg2,(0,bg2_y))
                if player.rect.centery <= dy/2:
                        bg_y += 5
                        bg2_y += 5
                        for tile in tile_group:
                                tile.rect.top += 5
                        for enemy in enemy_group:
                                enemy.rect.top += 5
                        final_platform.rect.centery += 5
                final_shot = pygame.sprite.spritecollide(bullet1,final_platform_sprite,False,pygame.sprite.collide_rect)
                if final_shot:
##                    print("YOU WON!")
                    pygame.mixer.Sound.play(win_sound)
                    end_screen()
                if bg_y >= 1180:
                        bg_y = 0
                if bg2_y >= 0:
                        bg2_y = -1180
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                running = False
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
##                            print("a")
##                        print(i)
                            pygame.mixer.Sound.play(walk_sound)
##                        pygame.mixer.Sound.play(walk_sound)
        ##                display.blit(player.turn_right[0],(player.rect.centerx,player.rect.centery))
                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                        player.left = False
                        player.right= True
                        player.standing = False
                        player.rect.centerx += 5
                        i += 1
                        if i % 10 == 0:
##                            print("a")
##                        print(i)
                            pygame.mixer.Sound.play(walk_sound)
                else:
                        i = 0
                        player.standing = True
                        player.left = False
                        player.right = False
                if keys[pygame.K_SPACE]:
                        if player.is_on_floor: # check if player is allowd to jump (is on floor)
                            player.jump = 10 # set any value for jumping
                            player.is_on_floor = False # disable floor check
                            pygame.mixer.Sound.play(jump_sound)
                if keys[pygame.K_c] and bullet1.state == "ready":
                        bullet1.rect.center = player.rect.center
                        pygame.mixer.Sound.play(shoot_sound)
                        bullet1.state = "fired"
                if player.sound:
                            pygame.mixer.Sound.play(jump_sound)
                            player.sound = False        
                
                player.check_collision()
                player.update()
                
                final_platform.draw()
                player.draw()
                if bullet1.state == "fired":
                        bullet1.draw()
                enemy.draw()
        ##        print(bullet1.state)
        ##        player.jump()

                #PLAYER
                if player.rect.left > dx:
                        player.rect.right = 0
                elif player.rect.right < 0:
                        player.rect.left = dx
                if player.rect.bottom >= dy:
                        save_score(0,score)
                        end_screen()
                
                #TILES
                for tile in tile_group:
                        tile.draw()
                        if tile.rect.top >= dy:
                                tile_group.remove(tile)
                                score += 10
                text("Score: ",(255,255,255),210,dy - 30)
                text(str(score),(255,255,255),270,dy - 30)
##                display.blit(button_exit,(45,final-250))
                if final_platform.rect.centery >= 50:
                    final_platform.rect.centery = 50
                    end_text("YOU WON!",(0,0,0),75,140)
                 #ENEMY
                for enemy in enemy_collision_group:
                        enemy.draw()
                        if len(enemy_collision_group) <= 0:
                            enemy_collision_group.empty()
                        enemy.rect.centerx += enemy.change_x
                        if enemy.rect.left <= 0:
                                enemy.change_x = 2
                        if enemy.rect.right >= dx:
                                enemy.change_x = -2
##                print()
                if bullet1.state == "fired":
                        hit = pygame.sprite.spritecollide(bullet1,enemy_collision_group,True,pygame.sprite.collide_rect)
                        if hit:
                                bullet1.rect.center = player.rect.center
                                bullet1.state = "ready"
                                score += 100
                                pygame.mixer.Sound.play(collision_sound)
                collided = pygame.sprite.spritecollide(player,enemy_collision_group,False)
                if collided:
                        save_score(0,score)
                        pygame.mixer.Sound.play(lose_sound)
                        end_screen()
                #BULLET
                if bullet1.state == "fired":
                        bullet1.shoot()
                        bullet1.rect.centery -= 5
                if bullet1.rect.centery <= 0:
                        bullet1.rect.center = player.rect.center
                        bullet1.state = "ready"
                
        ##        print(bullet1.rect.centery)
                clock.tick(60)
                pygame.display.update()
main_menu()
