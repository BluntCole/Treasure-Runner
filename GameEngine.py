import pygame
import pytmx
import os
import Box2D

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

pygame.init()
screen = pygame.display.set_mode((1280,620))

script_dir = os.path.dirname(os.path.abspath(__file__))
map_path = os.path.join(script_dir, "GameMap", "GameMap.tmx")
tiled_map = pytmx.util_pygame.load_pygame(map_path)
sprite_group = pygame.sprite.Group()

for layer in tiled_map.layers:
    if layer.name in ('Physical for player and ball', 'physical for ball', 'physical for player'):
        for x, y, surf in layer.tiles():
            pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
            Tile(pos = pos, surf = surf, groups = sprite_group)

# for layer in tiled_map.visible_layers:
#     if isinstance(layer, pytmx.TiledTileLayer):
#         for x, y, gid in layer:
#             tile = tiled_map.get_tile_image_by_gid(gid)
#             screen.blit(tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))

class GameEngine:
    def __init__(self, screen_size=(600, 600), fps=30):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = False
        self.game_objects = []



    def add_game_object(self, game_object):
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object):
        self.game_objects.remove(game_object)

    def start(self):
        self.running = True

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update game objects
            #for game_object in self.game_objects:
                #game_object.update()

            sprite_group.draw(screen)
                # Draw Tiled map
            # for layer in self.tiled_map.visible_layers:
            #     if isinstance(layer, pytmx.TiledTileLayer):
            #         for x, y, gid in layer:
            #             tile = self.tiled_map.get_tile_image_by_gid(gid)
            #             self.screen.blit(tile, (x * self.tiled_map.tilewidth, y * self.tiled_map.tileheight))

            # Draw game objects
            #for game_object in self.game_objects:
                #game_object.draw(self.screen)

            # Update display
            pygame.display.flip()

            # Control FPS
            self.clock.tick(self.fps)

        pygame.quit()
