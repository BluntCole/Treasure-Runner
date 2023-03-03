import pygame
from Box2D import *
from tiles import Tile

PPM = 0.1

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, world, sheet_filename, frame_width, frame_height):
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

        self.body = self.create_body(world)

    def create_body(self, world):
        body_def = b2BodyDef()
        body_def.type = b2_dynamicBody
        body_def.position = b2Vec2(self.rect.x * PPM, self.rect.y * PPM)

        body = world.CreateBody(body_def)

        shape = b2PolygonShape()
        shape.SetAsBox(self.rect.width / 2 * PPM, self.rect.height / 2 * PPM)

        fixture_def = b2FixtureDef()
        fixture_def.shape = shape
        fixture_def.density = 1
        fixture_def.restitution = 0.1

        body.CreateFixture(fixture_def)

        return body

    def update(self, world):
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

        # move the player using Box2D physics
        if self.direction == "up":
            self.body.ApplyLinearImpulse = (0, -5)
            print(self.body.ApplyLinearImpulse)
        elif self.direction == "down":
            self.body.ApplyLinearImpulse = (0, 5)
            print(self.body.ApplyLinearImpulse)
        elif self.direction == "left":
            self.body.ApplyLinearImpulse = (-5, 0)
            print(self.body.ApplyLinearImpulse)
        elif self.direction == "right":
            self.body.ApplyLinearImpulse = (5, 0)
            print(self.body.ApplyLinearImpulse)

        # update player position based on Box2D physics
        pos = self.body.position
        self.rect.x = pos.x - self.rect.width / 2
        self.rect.y = pos.y - self.rect.height / 2

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        print(self.rect)

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
        self.body.ApplyLinearImpulse = (0, 0)


