import pygame
import Box2D

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

    def collides_with_sprite(self, sprite):
        return self.rect.colliderect(sprite.rect)

# class Tile(pygame.sprite.Sprite):
#     def __init__(self, pos, surf, groups, world):
#         super().__init__(groups)
#         self.image = surf
#         self.rect = self.image.get_rect(topleft=pos)
#         self.world = world
#
#     def create_body(self):
#         # Create a Box2D body for the tile
#         bodyDef = Box2D.b2BodyDef()
#         bodyDef.position = (self.rect.centerx, self.rect.centery)
#         self.body = self.world.CreateBody(bodyDef)
#
#         # Create a Box2D shape for the tile
#         shape = Box2D.b2PolygonShape()
#         shape.SetAsBox(self.rect.width/2, self.rect.height/2)
#         fixtureDef = Box2D.b2FixtureDef(shape=shape)
#         self.body.CreateFixture(fixtureDef)
#
#         # Set the user data for the body to the tile instance
#         self.body.userData = self
#         # Return the Box2D body
#         return self.body