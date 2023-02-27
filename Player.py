import pygame
import Box2D
from tiles import Tile


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet_filename, frame_width, frame_height):
        super().__init__()
        # load the tiled sheet image
        self.sheet = pygame.image.load(sheet_filename).convert_alpha()

        # define the dimensions of each frame in the tiled sheet
        self.frame_width = frame_width
        self.frame_height = frame_height

        # define the coordinates of the first frame in the tiled sheet
        self.frame_x = 0
        self.frame_y = 0

        # extract the first frame from the tiled sheet
        self.image = self.sheet.subsurface(pygame.Rect(self.frame_x, self.frame_y, self.frame_width, self.frame_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # set up variables for animation
        self.frame_count = 0
        self.animation_speed = 5
        self.current_frame = 0

        self.speed = 5
        self.direction = ""
        self.is_moving = False

    def update(self):
        # increment frame_count and check if it's time to update animation
        if self.is_moving:
            self.frame_count += 1
            if self.frame_count >= self.animation_speed:
                self.frame_count = 0

                # update the current frame of the animation
                self.current_frame = (self.current_frame + 1) % 4
                self.frame_x = self.current_frame * self.frame_width

                # extract the current frame from the tiled sheet
                self.image = self.sheet.subsurface(
                    pygame.Rect(self.frame_x, self.frame_y, self.frame_width, self.frame_height))

        # move the player
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

    def move_up(self):
        self.is_moving = True
        self.direction = "up"

    def move_down(self):
        self.is_moving = True
        self.direction = "down"

    def move_left(self):
        self.is_moving = True
        self.direction = "left"

    def move_right(self):
        self.is_moving = True
        self.direction = "right"

    def stop_moving(self):
        self.is_moving = False

    def handle_collision(self, other_sprite):
        if isinstance(other_sprite,Tile):
            if other_sprite.tile_type in ["Physical for player and ball", "Physical for player"]:
                if self.direction == "up":
                    self.rect.top = other_sprite.rect.bottom
                elif self.direction == "down":
                    self.rect.bottom = other_sprite.rect.top
                elif self.direction == "left":
                    self.rect.left = other_sprite.rect.right
                elif self.direction == "right":
                    self.rect.right = other_sprite.rect.left
                # stop the player's movement
                self.stop_moving()
