import pygame
import pytmx
import os


def get_asset_file(filename):
    return os.path.join('Assets', filename)


level_data = pytmx.TiledMap(get_asset_file('demo.tmx'))


class Grid:
    BLOCK_SIZE = 32


class Color:
    STEEL_BLUE = (95, 158, 160)
    BLACK = (0, 0, 0)


class Player:

    def __init__(self, position, id):
        self.__sprite = pygame.Surface((32, 32))
        self.__sprite.fill(Color.STEEL_BLUE)
        self.__aabb = self.__sprite.get_rect()
        self.__aabb.x = position[0]
        self.__aabb.y = position[1]
        self.__id = id
        self.is_running = False
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.__speed = [1, 1]

    @property
    def sprite(self):
        return self.__sprite

    @property
    def position(self):
        return (self.__aabb.x, self.__aabb.y)

    @property
    def AABB(self):
        return self.__aabbb

    def move(self, direction, speed):
        self.__aabb.x += direction[0]*speed[0]
        self.__aabb.y += direction[1]*speed[1]

    def update(self):

        moving_vector = [0, 0]
        if self.moving_left:
            moving_vector[0] -= 1
        if self.moving_right:
            moving_vector[0] += 1
        if self.moving_up:
            moving_vector[1] -= 1
        if self.moving_down:
            moving_vector[1] += 1

        self.__speed = [2, 2] if self.is_running else [1, 1]

        self.move(moving_vector, self.__speed)

# initialize the display for drawing to the screen
pygame.display.init()
display = pygame.display.set_mode([800, 600], pygame.DOUBLEBUF, 32)

# initialize the mixer for sound to work
pygame.mixer.init()

# clock for keeping track of time, ticks, and frames per second
clock = pygame.time.Clock()

player = Player((400, 300), 'player_main')

done = False
while not done:
    clock.tick(120)
    display.fill(Color.BLACK)
    display.blit(player.sprite, player.position)
    pygame.display.flip()

    events = pygame.event.get()

    # handle input
    for event in events:
        # handle clicking the X on the game window
        if event.type == pygame.QUIT:
            print('received a quit request')
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_w:
                print('moving up')
                player.moving_up = True
            if event.key == pygame.K_s:
                print('moving down')
                player.moving_down = True
            if event.key == pygame.K_a:
                print('moving left')
                player.moving_left = True
            if event.key == pygame.K_d:
                print('moving right')
                player.moving_right = True
            if event.key == pygame.K_LSHIFT:
                player.is_running = True

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_w:
                print('no longer moving up')
                player.moving_up = False
            if event.key == pygame.K_s:
                print('no longer moving down')
                player.moving_down = False
            if event.key == pygame.K_a:
                print('no longer moving left')
                player.moving_left = False
            if event.key == pygame.K_d:
                print('no longer moving right')
                player.moving_right = False
            if event.key == pygame.K_LSHIFT:
                player.is_running = False

    player.update()

# shuts down all pygame modules - IDLE friendly
pygame.quit()
