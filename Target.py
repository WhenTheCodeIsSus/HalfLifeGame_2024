import pygame

class Target:
    """
    Class representing a target in the game.
    """
    def __init__(self, x, y, health, image, hit_image, destroy_image):
        """
        Initializes a new instance of the Target class.

        Args:
            x (int): The initial x-coordinate of the target.
            y (int): The initial y-coordinate of the target.
            health (int): The health points of the target.
            image (str): The image file path for the target.
            hit_image (str): The image file path for the hit effect.
            destroy_image (str): The image file path for the destroy effect.
        """
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=(x, y))
        self.hit_effect_duration = 30
        self.hit_effect_timer = 0
        self.hit_effect_image = pygame.image.load(hit_image)
        self.destroy_effect_image = pygame.image.load(destroy_image)
        self.health = health
        self.is_destroyed = False
        self.is_hit = False

    def hit(self):
        """
        Initiates the hit effect on the target.
        """
        self.hit_effect_timer = self.hit_effect_duration    
        self.is_hit = True

    def update(self):
        """
        Updates the target's state.
        """
        if self.hit_effect_timer > 0 and self.is_hit:
            self.hit_effect_timer -= 1
        else:
            self.is_hit = False

    def draw(self, screen):
        """
        Draws the target on the screen.

        Args:
            screen (pygame.Surface): The game screen.
        """
        screen.blit(self.image, self.rect)

        if self.hit_effect_timer > 0 and not self.is_destroyed:
            screen.blit(self.hit_effect_image, self.rect)

        elif self.is_destroyed:
            screen.blit(self.destroy_effect_image, self.rect)
            
    def is_target_hit(self):
        """
        Checks if the target is currently hit.

        Returns:
            bool: True if the target is hit, False otherwise.
        """
        return self.is_hit

    def is_target_destroyed(self):
        """
        Checks if the target is destroyed.

        Returns:
            bool: True if the target is destroyed, False otherwise.
        """
        return self.is_destroyed

    def receive_damage(self, damage):
        """
        Receives damage and updates the target's state.

        Args:
            damage (int): The amount of damage to be received.
        """
        self.health -= damage
        if self.health <= 0:
            self.is_destroyed = True

    def get_coords(self):
        """
        Gets the coordinates of the target.

        Returns:
            tuple: The (x, y) coordinates of the target.
        """
        return self.rect.center
            

        
