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

b2w = 100
gravity = b2Vec2(0.5, -10.0)
world = Box2D.b2World(gravity, doSleep=True)


for layer in tiled_map.layers:
    if layer.name in ('Physical for player and ball', 'physical for ball', 'physical for player'):
        for x, y, gid, in layer:
            if gid > 0:
                surf = tiled_map.get_tile_image_by_gid(gid)
                pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
                tile = Tile(pos=pos, surf=surf, groups=tile_group, world=world)
                tile.create_body()

class GameEngine:
    def __init__(self, screen_size=(600, 600), fps=30):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = False
        self.game_objects = []
        self.sprite_group = pygame.sprite.Group()
        self.world = world
        self.done = False

        self.player = Player(x=2000, y=1200, world = self.world, sheet_filename='GameMap/maleBase/maleBase/full/advnt_full.png',
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
                    if event.key == pygame.K_UP:
                        self.player.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.player.move_down()
                    elif event.key == pygame.K_LEFT:
                        self.player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.stop_moving()

            self.screen.fill((0, 0, 0))

            self.player.update(self.world)
            tile_group.draw(screen)
            self.player.draw(self.screen)

            print(world.contactListener)
            # Update display
            pygame.display.flip()

            # Control FPS
            self.clock.tick(self.fps)

        pygame.quit()
