import pygame

class Projectile(pygame.sprite.Sprite):
    """
    Class representing a projectile in the game.
    """
    def __init__(self, screen, image, rect, velocity, damage):
        """
        Initializes a new instance of the Projectile class.

        Args:
            screen (pygame.Surface): The game screen.
            image (pygame.Surface): The image representing the projectile.
            rect (pygame.Rect): The rectangular area of the projectile.
            velocity (list): The velocity of the projectile in the (x, y) direction.
            damage (int): The damage inflicted by the projectile.
        """ 
        super().__init__()
        self.screen = screen
        self.image = image
        self.rect = rect
        self.velocity = velocity
        self.damage = damage

    def update(self):
        """
        Updates the position of the projectile based on its velocity.
        """
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def draw(self):
        """
        Draws the projectile on the game screen.
        """
        self.screen.blit(self.image, self.rect)

    def handle_collision(self, target):
        """
        Handles collision between the projectile and a target.

        Args:
            target (Target): The target object to check for collision.
        """
        if self.rect.colliderect(target.rect):
            self.kill()

    def get_damage(self):
        """
        Gets the damage inflicted by the projectile.

        Returns:
            int: The damage value.
        """
        return self.damage
