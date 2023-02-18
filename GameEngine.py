import pygame

class GameEngine:
    def __init__(self, screen_size=(640, 480), fps=30):
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
            for game_object in self.game_objects:
                game_object.update()

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Draw game objects
            for game_object in self.game_objects:
                game_object.draw(self.screen)

            # Update display
            pygame.display.flip()

            # Control FPS
            self.clock.tick(self.fps)

        pygame.quit()
