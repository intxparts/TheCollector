import pygame
import pytmx
import os

pygame.init()

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

    SPRITE_DEATH = pygame.image.load(get_asset_file('death.png'))

    SOUND_GRUNT = pygame.mixer.Sound(get_asset_file('grunt.ogg'))
    SOUND_SCREAM = pygame.mixer.Sound(get_asset_file('scream.ogg'))
    SOUND_DROWNING = pygame.mixer.Sound(get_asset_file('drowning.ogg'))
    SOUND_HAPPY_GRUMBLING = pygame.mixer.Sound(get_asset_file('item_collection.ogg'))

    HOLE_COLLISION = pygame.sprite.collide_rect_ratio(0.70)
    GATE_COLLISION_Y = pygame.sprite.collide_rect_ratio(0.5)
    GATE_COLLISION_X = pygame.sprite.collide_rect_ratio(1)
    BOULDER_COLLISION = pygame.sprite.collide_circle_ratio(0.75)

    def __init__(self, position, id):
        self.__aabb_sprite = CharBoundingBox()
        self.__aabb = self.__aabb_sprite.rect
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
        self.__is_alive = True
        self.__death_frames = 0
        self.artifacts_collected = []
        self.__sprites = [
            [Player.SPRITE_UP_STAND, Player.SPRITE_UP_WALK1, Player.SPRITE_UP_STAND, Player.SPRITE_UP_WALK2],
            [Player.SPRITE_DOWN_STAND, Player.SPRITE_DOWN_WALK1, Player.SPRITE_DOWN_STAND, Player.SPRITE_DOWN_WALK2],
            [Player.SPRITE_LEFT_STAND, Player.SPRITE_LEFT_WALK1, Player.SPRITE_LEFT_STAND, Player.SPRITE_LEFT_WALK2],
            [Player.SPRITE_RIGHT_STAND, Player.SPRITE_RIGHT_WALK1, Player.SPRITE_RIGHT_STAND, Player.SPRITE_RIGHT_WALK2],
            [Player.SPRITE_DEATH]
            ]

    def reset(self, position):
        self.__aabb_sprite = CharBoundingBox()
        self.__aabb = self.__aabb_sprite.rect
        self.__aabb.x = position[0]
        self.__aabb.y = position[1]
        self.__sprite_shift_counter = 0
        self.__is_running = False
        self.__moving_left = False
        self.__moving_right = False
        self.__moving_up = False
        self.__moving_down = False
        self.__speed = [1, 1]
        self.__sprite_index = 0
        self.__sprite_group_index = 0
        self.__is_alive = True
        self.__death_frames = 0

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
    def is_alive(self):
        return self.__is_alive

    @is_alive.setter
    def is_alive(self, value):
        if not value:
            self.__sprite_index = 0
            self.__sprite_group_index = 4
        self.__is_alive = value

    def has_artifact(self, artifact):
        for artifact in self.artifacts_collected:
            if artifact.name == artifact.name:
                return True
        return False

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
        self.__aabb_sprite.update(self.__aabb)
        if not self.is_alive:
            if self.__death_frames > 160:
                self.__death_frames = 0
                return 'reset_level'
            else:
                self.__death_frames += 1
                return None

        moving_vector = [0, 0]
        if self.moving_left:
            moving_vector[0] -= 1
        if self.moving_right:
            moving_vector[0] += 1
        if self.moving_up:
            moving_vector[1] -= 1
        if self.moving_down:
            moving_vector[1] += 1

        for boulder in level.boulders:
            if boulder.is_activated:
                if Player.BOULDER_COLLISION(self.__aabb_sprite, boulder):
                    if boulder.is_moving:
                        self.is_alive = False
                        Player.SOUND_GRUNT.play(0)

        for spikes in level.spikes:
            if self.__aabb.colliderect(spikes.AABB):
                spikes.is_triggered = True
                if spikes.is_extended:
                    self.is_alive = False
                    Player.SOUND_GRUNT.play(0)

        is_moving = moving_vector[0] != 0 or moving_vector[1] != 0

        if is_moving:
            if self.__sprite_shift_counter > 10:
                self.__sprite_index = (self.__sprite_index + 1) % len(self.__sprites[self.__sprite_group_index])
                self.__sprite_shift_counter = 0
            self.__sprite_shift_counter += 1
            dx = moving_vector[0]*self.__speed[0]
            dy = moving_vector[1]*self.__speed[1]
            self.__aabb.x += dx
            for blocker in level.blockers:
                if self.__aabb.colliderect(blocker):
                    self.__aabb.x -= dx

            for boulder in level.boulders:
                if boulder.is_activated:
                    if Player.BOULDER_COLLISION(self.__aabb_sprite, boulder):
                        if boulder.is_moving:
                            self.is_alive = False
                            Player.SOUND_GRUNT.play(0)
                        else:
                            self.__aabb.x -= dx

            for artifact in level.artifacts:
                if not artifact.is_collected and not self.has_artifact(artifact) and \
                        self.__aabb.colliderect(artifact.AABB):
                    Player.SOUND_HAPPY_GRUMBLING.play(0)
                    artifact.is_collected = True
                    self.artifacts_collected.append(artifact)

            for spikes in level.spikes:
                if self.__aabb.colliderect(spikes.AABB):
                    spikes.is_triggered = True
                    if spikes.is_extended:
                        self.is_alive = False
                        Player.SOUND_GRUNT.play(0)

            for gate in level.gates:
                if Player.GATE_COLLISION_X(self.__aabb_sprite, gate):
                    self.__aabb.x -= dx

            for hole in level.holes:
                if self.__aabb.colliderect(hole.AABB):
                    self.is_alive = False
                    Player.SOUND_SCREAM.play(0)

            for water in level.water:
                if self.__aabb.colliderect(water.AABB):
                    self.is_alive = False
                    Player.SOUND_DROWNING.play(0)

            for button in level.buttons:
                if self.__aabb.colliderect(button.AABB):
                    button.activate()

            self.__aabb.y += dy
            for blocker in level.blockers:
                if self.__aabb.colliderect(blocker):
                    self.__aabb.y -= dy

            for gate in level.gates:
                if Player.GATE_COLLISION_Y(self.__aabb_sprite, gate):
                    self.__aabb.y -= dy

            for boulder in level.boulders:
                if boulder.is_activated:
                    if Player.BOULDER_COLLISION(self.__aabb_sprite, boulder):
                        if boulder.is_moving:
                            self.is_alive = False
                        else:
                            self.__aabb.y -= dy

            for artifact in level.artifacts:
                if not artifact.is_collected and not self.has_artifact(artifact) and \
                        self.__aabb.colliderect(artifact.AABB):
                    Player.SOUND_HAPPY_GRUMBLING.play(0)
                    artifact.is_collected = True
                    self.artifacts_collected.append(artifact)

            for spikes in level.spikes:
                if self.__aabb.colliderect(spikes.AABB):
                    spikes.is_triggered = True
                    if spikes.is_extended:
                        self.is_alive = False
                        Player.SOUND_GRUNT.play(0)

            for hole in level.holes:
                if self.__aabb.colliderect(hole.AABB):
                    self.is_alive = False
                    Player.SOUND_SCREAM.play(0)

            for water in level.water:
                if self.__aabb.colliderect(water.AABB):
                    self.is_alive = False
                    Player.SOUND_DROWNING.play(0)

            for button in level.buttons:
                if self.__aabb.colliderect(button.AABB):
                    button.activate()

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
    end_game = False
    end_game_state = 'something_wrong'
    done = False
    while not done:
        clock.tick(60)
        display.fill(Color.BLACK)
        display.blit(map_surface, map_rect)

        for button in current_level.buttons:
            button.render(display)

        for gate in current_level.gates:
            gate.render(display)

        # debug purposes
        # display.blit(player.aabb_sprite.image, player.position)

        for artifact in current_level.artifacts:
            if not player.has_artifact(artifact):
                artifact.render(display)

        display.blit(player.current_sprite, player.position)

        for boulder in current_level.boulders:
            boulder.render(display)

        for spikes in current_level.spikes:
            spikes.render(display)

        pygame.display.flip()

        if player.is_alive:
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
        for spikes in current_level.spikes:
            spikes.update()
        for button in current_level.buttons:
            button.update()
        for gate in current_level.gates:
            gate.update(current_level.buttons)
        for boulder in current_level.boulders:
            boulder.update(current_level.buttons)
        if transition:
            if transition == 'reset_level':
                current_level = Level(levels[level_index], prev_level=True)
                map_surface = current_level.make_map()
                map_rect = map_surface.get_rect()
                player.reset((current_level.spawn_location.x, current_level.spawn_location.y))
            elif transition == 'prev_level' or transition == 'next_level':
                prev_level = True
                if transition == 'prev_level':
                    level_index -= 1
                    prev_level = False
                elif transition == 'next_level':
                    level_index += 1

                if level_index < 0:
                    end_game = True
                    end_game_state = 'going_home_early'
                    done = True
                elif level_index == len(levels):
                    end_game = True
                    end_game_state = 'victory'
                    done = True
                else:
                    current_level = Level(levels[level_index], prev_level=prev_level)
                    map_surface = current_level.make_map()
                    map_rect = map_surface.get_rect()
                    player.reset((current_level.spawn_location.x, current_level.spawn_location.y))

    EARLY_ENDING = pygame.image.load(get_asset_file('early_ending.png'))
    VICTORY = pygame.image.load(get_asset_file('victory.png'))
    while end_game:
        clock.tick(60)
        display.fill(Color.BLACK)
        events = pygame.event.get()
        if end_game_state == 'going_home_early':
            display.blit(EARLY_ENDING, (0, 0))
        elif end_game_state == 'victory':
            display.blit(VICTORY, (0, 0))
            show_case_x = 0
            show_case_y = 400
            for artifact in player.artifacts_collected:
                display.blit(artifact.image, (show_case_x, show_case_y))
                show_case_x += 40

        pygame.display.flip()
        # handle input
        for event in events:
            # handle clicking the X on the game window
            if event.type == pygame.QUIT:
                print('received a quit request')
                end_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    end_game = False


    # shuts down all pygame modules - IDLE friendly
    pygame.quit()


class Gate(pygame.sprite.Sprite):
    SPRITE_GATE = pygame.image.load(get_asset_file('gate.png'))
    SOUND_GRINDING = pygame.mixer.Sound(get_asset_file('door_open.ogg'))

    def __init__(self, rect, name, direction, move_rate, max_move_length):
        pygame.sprite.Sprite.__init__(self)
        self.image = Gate.SPRITE_GATE
        self.rect = rect.copy()
        self.__name = name
        self.__original_position = rect.copy()
        self.__aabb = rect.copy()
        self.__direction = direction
        self.__move_rate = move_rate
        self.__max_move_length = max_move_length
        self.__frames = 0

    @property
    def AABB(self):
        return self.__aabb

    def render(self, display):
        display.blit(Gate.SPRITE_GATE, (self.__aabb.x, self.__aabb.y))

    def update(self, buttons):
        is_powered = True
        for button in buttons:
            if button.trigger_object == self.__name:
                is_powered = is_powered and button.is_activated
                # print('gate is powered =', is_powered, 'button is activated =', button.is_activated)

        distance = abs(self.__aabb.x - self.__original_position.x)
        if is_powered:
            if distance < self.__max_move_length:
                Gate.SOUND_GRINDING.play(0)
                self.__aabb.x += self.__direction*self.__move_rate
        else:
            # print('distance = ', distance)
            if self.__aabb.x != self.__original_position.x:
                Gate.SOUND_GRINDING.play(0)
                self.__aabb.x += -1*self.__direction*self.__move_rate
        self.rect.x = self.__aabb.x
        self.rect.y = self.__aabb.y

class Button:
    SPRITE_PRESSED = pygame.image.load(get_asset_file('button_pressed.png'))
    SPRITE_UNPRESSED = pygame.image.load(get_asset_file('button_unpressed.png'))

    SOUND_ACTIVATE = pygame.mixer.Sound(get_asset_file('pressure_plate.ogg'))
    SOUND_RESET = pygame.mixer.Sound(get_asset_file('plate_reset.ogg'))

    def __init__(self, rect, reset_time, trigger_object):
        self.__activated = False
        self.__timer_frames = 0
        self.__reset_time = reset_time
        self.__sprite_position = rect.copy()
        self.__aabb = rect.copy()
        self.__aabb.x += 10
        self.__aabb.y += 14
        self.__aabb.width = 18
        self.__aabb.height = 12
        self.trigger_object = trigger_object

    @property
    def is_activated(self):
        return self.__activated

    @property
    def AABB(self):
        return self.__aabb

    def render(self, display):
        if self.__activated:
            display.blit(Button.SPRITE_PRESSED, (self.__sprite_position.x, self.__sprite_position.y))
        else:
            display.blit(Button.SPRITE_UNPRESSED, (self.__sprite_position.x, self.__sprite_position.y))

    def activate(self):
        if not self.__activated:
            Button.SOUND_ACTIVATE.play(0)

        self.__activated = True

    def update(self):
        if self.__activated and self.__reset_time > -1:
            if self.__timer_frames > self.__reset_time:
                Button.SOUND_RESET.play(0)
                self.__activated = False
                self.__timer_frames = 0
            else:
                self.__timer_frames += 1


class Spikes:
    EXTENDED_SPIKES_OFFSET = 20
    EXTENDED_SPIKES = pygame.image.load(get_asset_file('floor_spike_extended.png'))
    SPIKES_EXTENDING_SOUND = pygame.mixer.Sound(get_asset_file('spears_extended.ogg'))
    def __init__(self, rect):
        self.__aabb = rect
        self.__is_triggered = False
        self.__frames = 0
        self.__is_extended = False

    @property
    def AABB(self):
        return self.__aabb

    @property
    def is_triggered(self):
        return self.__is_triggered

    @is_triggered.setter
    def is_triggered(self, value):
        self.__is_triggered = value

    @property
    def is_extended(self):
        return self.__is_extended

    def render(self, display):
        if self.__is_extended:
            display.blit(Spikes.EXTENDED_SPIKES, (self.__aabb.x, self.__aabb.y - Spikes.EXTENDED_SPIKES_OFFSET))

    def update(self):

        if self.__is_triggered:
            if self.__frames > 37:
                Spikes.SPIKES_EXTENDING_SOUND.play(0)
                self.__is_triggered = False
                self.__is_extended = True
                self.__frames = 0
            else:
                self.__frames += 1

        if self.__is_extended:
            if self.__frames > 30:
                self.__is_extended = False
                self.__is_triggered = False
                self.__frames = 0
            else:
                self.__frames += 1


class Level:
    def __init__(self, filename, prev_level):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.blockers = []
        self.spikes = []
        self.buttons = []
        self.holes = []
        self.water = []
        self.gates = []
        self.boulders = []
        self.artifacts = []
        self.spawn_location = None
        self._prev_level = prev_level
        self.entrance = None
        self.exit = None
        self._load_game_objects()

    def __create_rect_from_tile_props(self, x, y, tile_props):
        return pygame.Rect(
            x * self.tmx_data.tilewidth,
            y * self.tmx_data.tileheight,
            int(tile_props['height']),
            int(tile_props['width'])
        )

    def _load_game_objects(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if tile_props and 'passable' in tile_props and tile_props['passable'] == 'false':
                        self.blockers.append(self.__create_rect_from_tile_props(x, y, tile_props))
                    if tile_props and 'trap' in tile_props:
                        if tile_props['trap'] == 'spikes':
                            self.spikes.append(Spikes(self.__create_rect_from_tile_props(x, y, tile_props)))
                        if tile_props['trap'] == 'hole':
                            self.holes.append(
                                Hole(
                                    self.tmx_data.get_tile_image_by_gid(gid),
                                    self.__create_rect_from_tile_props(x, y, tile_props)
                                )
                            )
                        if tile_props['trap'] == 'water':
                            self.water.append(
                                Hole(
                                    self.tmx_data.get_tile_image_by_gid(gid),
                                    self.__create_rect_from_tile_props(x, y, tile_props)
                                )
                            )
            if isinstance(layer, pytmx.TiledObjectGroup):
                for tile_object in layer:
                    if 'artifact' in tile_object.properties:
                        name = tile_object.properties['artifact']
                        worth = int(tile_object.properties['worth'])
                        self.artifacts.append(Artifact(name, self.__create_rect_from_tile_object(tile_object), tile_object.image, worth))
                    if 'boulder' in tile_object.properties:
                        direction = int(tile_object.properties['direction'])
                        move_rate = int(tile_object.properties['move_rate'])
                        max_move_length = int(tile_object.properties['max_move_length'])
                        name = tile_object.properties['boulder']
                        self.boulders.append(Boulder(self.__create_rect_from_tile_object(tile_object), name, direction, move_rate, max_move_length))
                    if 'gate' in tile_object.properties:
                        direction = int(tile_object.properties['direction'])
                        move_rate = int(tile_object.properties['move_rate'])
                        max_move_length = int(tile_object.properties['max_move_length'])
                        name = tile_object.properties['gate']
                        self.gates.append(Gate(self.__create_rect_from_tile_object(tile_object), name, direction, move_rate, max_move_length))
                    if 'button' in tile_object.properties:
                        timer = int(tile_object.properties['timer']) if 'timer' in tile_object.properties else -1
                        self.buttons.append(Button(self.__create_rect_from_tile_object(tile_object), timer, tile_object.properties['trigger']))
                    if 'spawn' in tile_object.properties:
                        if self._prev_level:
                            if tile_object.properties['spawn'] == 'prev_room':
                                self.spawn_location = self.__create_rect_from_tile_object(tile_object)
                        else:
                            if tile_object.properties['spawn'] == 'next_room':
                                self.spawn_location = self.__create_rect_from_tile_object(tile_object)
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


class Boulder(pygame.sprite.Sprite):

    SPRITE_BOULDER1 = pygame.image.load(get_asset_file('boulder1.png'))
    SPRITE_BOULDER2 = pygame.image.load(get_asset_file('boulder2.png'))
    SPRITE_BOULDER3 = pygame.image.load(get_asset_file('boulder3.png'))
    SPRITE_BOULDER4 = pygame.image.load(get_asset_file('boulder4.png'))

    SPRITES = [SPRITE_BOULDER1, SPRITE_BOULDER3, SPRITE_BOULDER2, SPRITE_BOULDER4]

    SOUND_ROLLING = pygame.mixer.Sound(get_asset_file('rolling.ogg'))

    def __init__(self, rect, name, direction, move_rate, max_move_length):
        pygame.sprite.Sprite.__init__(self)
        Boulder.SOUND_ROLLING.stop()
        self.rect = rect.copy()
        self.__original_position = rect.copy()
        self.__aabb = rect.copy()
        self.__name = name
        self.__direction = direction
        self.__move_rate = move_rate
        self.__max_move_length = max_move_length
        self.__sprite_index = 0
        self.__frames = 0
        self.__is_activated = False
        self.__is_moving = False

    @property
    def is_activated(self):
        return self.__is_activated

    @property
    def is_moving(self):
        return self.__is_moving

    def render(self, display):
        if self.__is_activated:
            display.blit(self.SPRITES[self.__sprite_index], (self.__aabb.x, self.__aabb.y))

    def update(self, buttons):
        is_powered = True
        for button in buttons:
            if button.trigger_object == self.__name:
                is_powered = is_powered and button.is_activated

        if is_powered:
            self.__is_activated = True

        distance = abs(self.__aabb.y - self.__original_position.y)
        if self.__is_activated:
            if distance < self.__max_move_length:
                Boulder.SOUND_ROLLING.play(-1)
                self.__is_moving = True
                self.__aabb.y += self.__direction*self.__move_rate
            else:
                self.__is_moving = False
                Boulder.SOUND_ROLLING.stop()

        if self.__is_moving:
            if self.__frames > 80/self.__move_rate:
                self.__frames = 0
                self.__sprite_index = (self.__sprite_index + 1) % len(Boulder.SPRITES)
            else:
                self.__frames += 1
        self.rect.x = self.__aabb.x
        self.rect.y = self.__aabb.y

class Artifact:
    def __init__(self, name, rect, image, worth):
        self.name = name
        self.image = image
        self.__aabb = rect
        self.__is_collected = False
        self.worth = worth

    @property
    def AABB(self):
        return self.__aabb

    @property
    def is_collected(self):
        return self.__is_collected

    @is_collected.setter
    def is_collected(self, value):
        self.__is_collected = value

    def render(self, display):
        if not self.is_collected:
            display.blit(self.image, (self.__aabb.x, self.__aabb.y))

class CharBoundingBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((28, 36))
        self.image.fill(Color.STEEL_BLUE)
        self.rect = self.image.get_rect()

    def update(self, rect):
        self.rect.x = rect.x
        self.rect.y = rect.y

class Hole(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = rect
        self.__aabb = rect.copy()
        self.__aabb.x += 10
        self.__aabb.y += 5
        self.__aabb.height = 10
        self.__aabb.width = 20

    @property
    def AABB(self):
        return self.__aabb


if __name__ == '__main__':
    run_game()
