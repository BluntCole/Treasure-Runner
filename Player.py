import pygame
from Box2D import *
from tiles import Tile
from time import time

PPM = .1


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, world, sheet_filename, frame_width, frame_height):
        super().__init__()
        # load the tiled sheet image
        self.sheet = pygame.image.load(sheet_filename).convert_alpha()

        self.move_force = 10000
        self.jump_force = 20000
        self.on_ground = True

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
        self.animation_speed = 10
        self.current_frame = 0

        self.direction = ""
        self.is_moving = True

        self.previous_position = (self.rect.x, self.rect.y)

        self.body = self.create_body(world)

        self.last_jump_time = 0
        self.jumped = False

    def create_body(self, world):
        body_def = b2BodyDef()
        body_def.type = b2_dynamicBody
        body_def.position = b2Vec2(self.rect.x * PPM, self.rect.y * PPM)

        body = world.CreateBody(body_def)

        shape = b2PolygonShape()
        shape.SetAsBox(self.rect.width / 2 * PPM, self.rect.height / 2 * PPM)

        fixDef = b2FixtureDef(shape=shape, friction=.3, restitution=0)

        body.CreateFixture(fixDef)

        return body

    def update(self, world, tiles):

        current_time = time()
        jump_time_since_last = current_time - self.last_jump_time
        jump_delay = 0.5

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
            self.body.ApplyLinearImpulse(b2Vec2(0, -self.jump_force), self.body.position, True)
            self.last_jump_time = current_time
            self.jumped = True
            self.on_ground = False
            print(self.on_ground, "here 2")
            print(self.jumped, "here 2")

        elif self.direction == "left":
            self.body.ApplyLinearImpulse(b2Vec2(-self.move_force, 0), self.body.position, True)

        elif self.direction == "right":
            self.body.ApplyLinearImpulse(b2Vec2(self.move_force, 0), self.body.position, True)

        # update player position based on Box2D physics
        self.rect.center = self.body.position * PPM

        print(self.body.linearVelocity.y, "here 1")
        # if self.body.linearVelocity.y > 0 and time.time() > .5:
        #         #     self.on_ground = True
        #         #     # apply a downward impulse to make the player fall
        #         #     self.body.ApplyLinearImpulse(b2Vec2(0, self.jump_force), self.body.position, True)

        self.previous_position = (self.rect.centerx, self.rect.centery)

        # self.previous_position = (self.rect.centerx, self.rect.centery)  # add this line

        if jump_time_since_last + 5 < current_time:
            print(self.on_ground)
            print(self.jumped)
            if self.body.linearVelocity.y < 0.1 and self.on_ground == False:
                self.body.ApplyLinearImpulse(b2Vec2(0, self.jump_force), self.body.position, True)
                self.on_ground = True
                self.jumped = False
                print(self.on_ground, "here 1")
                print(self.jumped, "here 1")

        # if time.time() - self.last_jump_time > 0.01:
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.direction == "left" or self.direction == "right":
                    self.body.linearVelocity = b2Vec2(self.body.linearVelocity.x, 0)
                if self.body.linearVelocity.y > 0.1:
                    self.body.linearVelocity = b2Vec2(self.body.linearVelocity.x, 0)

                # else:
                #     self.body.linearVelocity = b2Vec2(self.body.linearVelocity.x, 0)
                # if time.time() - last_jump_time > delay:
                #     self.on_ground = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

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
