import pygame
import random
import sys

# window size
WIDTH = 636
HEIGHT = 764

# display
pygame.init()
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# frames per second
clock = pygame.time.Clock()
fps = 60

# constants
ground_scroll = 0
scroll_speed = 4
pipe_gap = 150
pipe_frequency = 1500 # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency

# variables
flying = False
gameover = False

# load images
bg = pygame.image.load("graphics/bg.png").convert()
ground_img = pygame.image.load("graphics/ground.png").convert()
button_img = pygame.image.load("graphics/restart.png")

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            imm = (f"graphics/bird{num}.png")
            img = pygame.image.load(imm).convert_alpha()
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False

    def update(self):
        # gravity
        if flying == True:
            self.vel += 0.4
            if self.vel > 8:
                self.vel = 8 

        if self.rect.bottom < 600:
            self.rect.y += int(self.vel)
        
        # trigger
        if gameover == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel -=10
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False

            # animation 
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        
        else:
            # rotate 90 degrees
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):

    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/pipe.png")
        self.rect = self.image.get_rect()

        # position
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap / 2)]

    def update(self):
        # scroll pipes
        if flying == True:
            self.rect.x -= scroll_speed
            if self.rect.right < 0:
                self.kill()

class Button():

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check if mouse is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        # draw button
        wn.blit(self.image, (self.rect.x, self.rect.y))
        return action

# group
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

# bird
flappy = Bird(100, int(HEIGHT / 2))

# button instance
button = Button(WIDTH // 2 - 50, HEIGHT // 2 - 100, button_img)

# add to group
bird_group.add(flappy)
  
while True:
    # set fps
    clock.tick(fps)

    # draw background
    wn.blit(bg, (0,-150))

    # check for pipe collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        gameover = True

    # check for ground collison
    if flappy.rect.bottom > 600:
        gameover = True
        flying = False

    if gameover == False and flying == True:
        # generate pipe
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(WIDTH, int(HEIGHT /2)+ pipe_height, -1)
            top_pipe = Pipe(WIDTH, int(HEIGHT /2)+ pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # scroll ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()

    # draw bird
    bird_group.draw(wn)
    bird_group.update()

    # draw pipe
    pipe_group.draw(wn)

    # draw the ground
    wn.blit(ground_img, (ground_scroll, 600))

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameover == False:
            flying = True

    # check for game over
    if gameover == True:
        if button.draw() == True:
            flying = True
            gameover = False
            pipe_group.empty()
            flappy.rect.x = 100
            flappy.rect.y = int(HEIGHT / 2)
            flappy.vel = 0
    
    # update screen
    pygame.display.update()
