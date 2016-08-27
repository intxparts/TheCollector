import pygame
import pytmx
import os


ASSETS_FOLDER = os.path.join(os.getcwd(), 'Assets')


def get_asset_file(filename):
    return os.path.join(ASSETS_FOLDER, filename)


level_data = pytmx.TiledMap(get_asset_file('demo.tmx'))


class Grid:
    BLOCK_SIZE = 32


class Color:
    STEEL_BLUE = (95, 158, 160)
    BLACK = (0, 0, 0)


class Player:

    SPRITE_UP_STAND = pygame.image.load(get_asset_file('char_up_standing.png'))
    SPRITE_UP_WALK1 = pygame.image.load(get_asset_file('char_up_walk1.png'))
    SPRITE_UP_WALK2 = pygame.image.load(get_asset_file('char_up_walk2.png'))

    SPRITE_DOWN_STAND = pygame.image.load(get_asset_file('char_down_standing.png'))
    SPRITE_DOWN_WALK1 = pygame.image.load(get_asset_file('char_down_walk1.png'))
    SPRITE_DOWN_WALK2 = pygame.image.load(get_asset_file('char_down_walk2.png'))

    SPRITE_LEFT_STAND = pygame.image.load(get_asset_file('char_left_standing.png'))
    SPRITE_LEFT_WALK1 = pygame.image.load(get_asset_file('char_left_walk1.png'))
    SPRITE_LEFT_WALK2 = pygame.image.load(get_asset_file('char_left_walk2.png'))

    SPRITE_RIGHT_STAND = pygame.image.load(get_asset_file('char_right_standing.png'))
    SPRITE_RIGHT_WALK1 = pygame.image.load(get_asset_file('char_right_walk1.png'))
    SPRITE_RIGHT_WALK2 = pygame.image.load(get_asset_file('char_right_walk2.png'))

    def __init__(self, position, id):
        self.__sprite = pygame.Surface((32, 36))
        self.__sprite.fill(Color.STEEL_BLUE)
        self.__aabb = self.__sprite.get_rect()
        self.__aabb.x = position[0]
        self.__aabb.y = position[1]
        self.__id = id
        self.__sprite_shift_counter = 0
        self.__is_running = False
        self.__moving_left = False
        self.__moving_right = False
        self.__moving_up = False
        self.__moving_down = False
        self.__speed = [1, 1]
        self.__sprite_index = 0
        self.__sprite_group_index = 0
        self.__sprites = [
            [Player.SPRITE_UP_STAND, Player.SPRITE_UP_WALK1, Player.SPRITE_UP_STAND, Player.SPRITE_UP_WALK2],
            [Player.SPRITE_DOWN_STAND, Player.SPRITE_DOWN_WALK1, Player.SPRITE_DOWN_STAND, Player.SPRITE_DOWN_WALK2],
            [Player.SPRITE_LEFT_STAND, Player.SPRITE_LEFT_WALK1, Player.SPRITE_LEFT_STAND, Player.SPRITE_LEFT_WALK2],
            [Player.SPRITE_RIGHT_STAND, Player.SPRITE_RIGHT_WALK1, Player.SPRITE_RIGHT_STAND, Player.SPRITE_RIGHT_WALK2]
            ]

    @property
    def is_running(self):
        return self.__is_running

    @is_running.setter
    def is_running(self, value):
        self.__is_running = value
        self.__speed = [2, 2] if self.__is_running else [1, 1]

    @property
    def moving_left(self):
        return self.__moving_left

    @moving_left.setter
    def moving_left(self, value):
        if value:
            self.__sprite_group_index = 2
        self.__moving_left = value

    @property
    def moving_right(self):
        return self.__moving_right

    @moving_right.setter
    def moving_right(self, value):
        if value:
            self.__sprite_group_index = 3
        self.__moving_right = value

    @property
    def moving_up(self):
        return self.__moving_up

    @moving_up.setter
    def moving_up(self, value):
        if value:
            self.__sprite_group_index = 0
        self.__moving_up = value

    @property
    def moving_down(self):
        return self.__moving_down

    @moving_down.setter
    def moving_down(self, value):
        if value:
            self.__sprite_group_index = 1
        self.__moving_down = value

    @property
    def sprite(self):
        return self.__sprite

    @property
    def current_sprite(self):
        return self.__sprites[self.__sprite_group_index][self.__sprite_index]

    @property
    def position(self):
        return (self.__aabb.x, self.__aabb.y)

    @property
    def AABB(self):
        return self.__aabbb

    def move(self, direction, speed):
        self.__aabb.x += direction[0]*speed[0]
        self.__aabb.y += direction[1]*speed[1]

    def interact(self, object):
        pass

    def update(self):

        if self.__sprite_shift_counter > 10:
            self.__sprite_index = (self.__sprite_index + 1) % 4

        moving_vector = [0, 0]
        if self.moving_left:
            moving_vector[0] -= 1
        if self.moving_right:
            moving_vector[0] += 1
        if self.moving_up:
            moving_vector[1] -= 1
        if self.moving_down:
            moving_vector[1] += 1

        self.move(moving_vector, self.__speed)
        self.__sprite_shift_counter += 1

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
    display.blit(player.current_sprite, player.position)
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
            if event.key == pygame.K_e:
                player.interact('nothing')

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
