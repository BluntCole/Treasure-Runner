import pygame
import pytmx
import os
from Box2D import *
from Player import Player
from tiles import Tile

pygame.init()
screen = pygame.display.set_mode((1280, 620))

script_dir = os.path.dirname(os.path.abspath(__file__))
map_path = os.path.join(script_dir, "GameMap", "GameMap.tmx")
tiled_map = pytmx.util_pygame.load_pygame(map_path)

tile_group = pygame.sprite.Group()
non_pys_group = pygame.sprite.Group()

b2w = 100
gravity = b2Vec2(0, 100.0)
world = Box2D.b2World(gravity, doSleep=True)

for layer in tiled_map.layers:
    # if layer.name in ('player'):
    if layer.name in ('Physical for player and ball', 'physical for ball', 'physical for player'):
        for x, y, surf in layer.tiles():
            pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
            Tile(pos=pos, surf=surf, groups=tile_group)

for layer in tiled_map.layers:
    # if layer.name in ('player'):
    if layer.name in ('stairs'):
        for x, y, surf in layer.tiles():
            pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
            Tile(pos=pos, surf=surf, groups=non_pys_group)


class GameEngine:
    def __init__(self, screen_size=(600, 600), fps=60
                 ):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = False
        self.game_objects = []
        self.sprite_group = pygame.sprite.Group()
        self.world = world
        self.done = False

        self.player = Player(x=20000, y=12000, world = self.world, sheet_filename='GameMap/maleBase/maleBase/full/advnt_full.png',
                        frame_width=32, frame_height=64)

        self.add_game_object(self.player)

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)
        self.sprite_group.add(game_object)

    def remove_game_object(self, game_object):
        self.game_objects.remove(game_object)
        self.sprite_group.remove(game_object)

    def start(self):
        self.running = True
        while self.running:
            # # Handle events
            # self.rect.center = self.body.position[0] * b2w, 770 - self.body.position[1] * b2w
            # collided = pygame.sprite.spritecollide(self, tile_group, False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.move_up()
                    elif event.key == pygame.K_a:
                        self.player.move_left()
                    elif event.key == pygame.K_d:
                        self.player.move_right()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_a or event.key == pygame.K_d:
                        self.player.stop_moving()


            self.screen.fill((0, 0, 0))
            self.player.update(self.world, tile_group)
            world.Step(1 / 60, 6, 2)

            tile_group.draw(screen)
            non_pys_group.draw(screen)
            self.sprite_group.draw(screen)

            # Update display
            pygame.display.flip()

            # Control FPS
            self.clock.tick(self.fps)

        pygame.quit()
