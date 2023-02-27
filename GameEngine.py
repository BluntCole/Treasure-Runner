import pygame
import pytmx
import os
import PlayerObject
import Box2D

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

# pygame.init()
# screen = pygame.display.set_mode((1280,620))
#
# script_dir = os.path.dirname(os.path.abspath(__file__))
# map_path = os.path.join(script_dir, "GameMap", "GameMap.tmx")
# tiled_map = pytmx.util_pygame.load_pygame(map_path)
# sprite_group = pygame.sprite.Group()
#
# for layer in tiled_map.layers:
#     if layer.name == "player":
#         # Render tiles from the player layer
#         for x, y, surf in layer.tiles():
#             pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
#             Tile(pos=pos, surf=surf, groups=sprite_group)
#     else:
#         # Render all other layers
#         for x, y, surf in layer.tiles():
#             pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
#             Tile(pos=pos, surf=surf, groups=sprite_group)

class GameEngine:
    def __init__(self, screen_size=(700, 700), fps=30):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = False
        self.game_objects = []
        self.sprite_group = pygame.sprite.Group()
        self.camera_pos = [0, 0]
        self.camera_speed = 5

        script_dir = os.path.dirname(os.path.abspath(__file__))
        map_path = os.path.join(script_dir, "GameMap", "GameMap.tmx")
        tiled_map = pytmx.util_pygame.load_pygame(map_path)

        for layer in tiled_map.layers:
            if layer.name == "player":
                # Render tiles from the player layer
                for x, y, surf in layer.tiles():
                    pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    Tile(pos=pos, surf=surf, groups= self.sprite_group)
            else:
                # Render all other layers
                for x, y, surf in layer.tiles():
                    pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    Tile(pos=pos, surf=surf, groups= self.sprite_group)

        # player_object = None
        # for obj in tiled_map.get_layer_by_name('player'):
        #     obj_position = (obj[0], obj[1])
        #     obj_size = (obj[0], obj[1])
        #     obj_image = pygame.image.load(obj.image).convert_alpha()
        #     player_object = PlayerObject(obj_position, obj_size, obj_image)
        #     self.sprite_group.add(player_object)
        #
        # if player_object is not None:
        #     self.player_object = player_object
        # else:
        #     raise Exception("Player object not found in player layer.")

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
            # for game_object in self.game_objects:
            #     game_object.update()

            # Draw game objects
            #self.screen.fill((255, 255, 255))
            self.sprite_group.draw(self.screen)
            # for game_object in self.game_objects:
            #     game_object.draw(self.screen)

            # Update display
            pygame.display.flip()

            # Control FPS
            self.clock.tick(self.fps)

        pygame.quit()
