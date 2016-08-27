import pygame
import pytmx
import os


ASSETS_FOLDER = os.path.join(os.getcwd(), 'Assets')


def get_asset_file(filename):
    return os.path.join(ASSETS_FOLDER, filename)


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
        self.__aabb_sprite = pygame.Surface((28, 36))
        self.__aabb_sprite.fill(Color.STEEL_BLUE)
        self.__aabb = self.__aabb_sprite.get_rect()
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
    def aabb_sprite(self):
        return self.__aabb_sprite

    @property
    def current_sprite(self):
        return self.__sprites[self.__sprite_group_index][self.__sprite_index]

    @property
    def position(self):
        return (self.__aabb.x, self.__aabb.y)

    @property
    def AABB(self):
        return self.__aabbb

    def interact(self, object):
        pass

    def update(self, level):

        moving_vector = [0, 0]
        if self.moving_left:
            moving_vector[0] -= 1
        if self.moving_right:
            moving_vector[0] += 1
        if self.moving_up:
            moving_vector[1] -= 1
        if self.moving_down:
            moving_vector[1] += 1

        is_moving = moving_vector[0] != 0 or moving_vector[1] != 0

        if is_moving:
            if self.__sprite_shift_counter > 10:
                self.__sprite_index = (self.__sprite_index + 1) % 4
                self.__sprite_shift_counter = 0
            self.__sprite_shift_counter += 1
            dx = moving_vector[0]*self.__speed[0]
            dy = moving_vector[1]*self.__speed[1]
            self.__aabb.x += dx
            for blocker in level.blockers:
                if self.__aabb.colliderect(blocker):
                    self.__aabb.x -= dx

            self.__aabb.y += dy
            for blocker in level.blockers:
                if self.__aabb.colliderect(blocker):
                    self.__aabb.y -= dy

            if self.__aabb.colliderect(level.entrance):
                return 'prev_level'
            elif self.__aabb.colliderect(level.exit):
                return 'next_level'

            return None
        else:
            self.__sprite_index = 0


def run_game():
    # initialize the display for drawing to the screen
    pygame.display.init()
    display = pygame.display.set_mode([800, 600], pygame.DOUBLEBUF, 32)

    # initialize the mixer for sound to work
    pygame.mixer.init()

    # clock for keeping track of time, ticks, and frames per second
    clock = pygame.time.Clock()

    levels = [get_asset_file('level1.tmx'), get_asset_file('level2.tmx')]
    level_index = 0

    current_level = Level(levels[level_index], prev_level=True)
    map_surface = current_level.make_map()
    map_rect = map_surface.get_rect()

    player = Player((current_level.spawn_location.x, current_level.spawn_location.y), 'player_main')

    done = False
    while not done:
        clock.tick(60)
        display.fill(Color.BLACK)
        display.blit(map_surface, map_rect)

        # debug purposes
        display.blit(player.aabb_sprite, player.position)

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

        transition = player.update(current_level)
        if transition:
            level_index = (level_index - 1) if transition == 'prev_level' else (level_index + 1)
            if level_index < 0:
                print('beginning')
                done = True
            elif level_index == len(levels):
                print('end')
                done = True
            else:
                current_level = Level(levels[level_index], prev_level=True)
                map_surface = current_level.make_map()
                map_rect = map_surface.get_rect()

                player = Player((current_level.spawn_location.x, current_level.spawn_location.y), 'player_main')

    # shuts down all pygame modules - IDLE friendly
    pygame.quit()


class Level:
    def __init__(self, filename, prev_level):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.blockers = []
        self.spawn_location = None
        self._prev_level = prev_level
        self.entrance = None
        self.exit = None
        self._load_game_objects()

    def _load_game_objects(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if tile_props and 'passable' in tile_props and tile_props['passable'] == 'false':
                        self.blockers.append(
                            pygame.Rect(
                                x * self.tmx_data.tilewidth,
                                y * self.tmx_data.tileheight,
                                int(tile_props['height']),
                                int(tile_props['width'])
                            )
                        )
            if isinstance(layer, pytmx.TiledObjectGroup):
                for tile_object in layer:
                    if 'spawn' in tile_object.properties:
                        if self._prev_level:
                            if tile_object.properties['spawn'] == 'prev_room':
                                self.spawn_location = self.__create_rect_from_tile_object(tile_object)
                        else:
                            if tile_object.properties['spawn'] == 'next_room':
                                self.spawn_location = self.__create_rect_from_tWWile_object(tile_object)
                    if 'exit' in tile_object.properties:
                        # colliding with the entrance will take you to the previous room
                        if tile_object.properties['exit'] == 'prev_room':
                            self.entrance = self.__create_rect_from_tile_object(tile_object)
                        # colliding with the exit will take you to the next room
                        elif tile_object.properties['exit'] == 'next_room':
                            self.exit = self.__create_rect_from_tile_object(tile_object)


    def __create_rect_from_tile_object(self, tile_object):
        return pygame.Rect(tile_object.x, tile_object.y, tile_object.width, tile_object.height)

    def render(self, surface):

        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight

        if self.tmx_data.background_color:
            surface.fill(self.tmx_data.background_color)

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * tw, y * th))

            elif isinstance(layer, pytmx.TiledObjectGroup):
                pass

            elif isinstance(layer, pytmx.TiledImageLayer):
                image = self.tmx_data.get_tile_image_by_gid(layer.gid)
                if image:
                    surface.blit(image, (0, 0))

    def make_map(self):
        temp_surface = pygame.Surface(self.size)
        self.render(temp_surface)
        return temp_surface


if __name__ == '__main__':
    run_game()
