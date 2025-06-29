import pygame
import math
from Enemy import Enemy

class FluidEnemy(Enemy):
    """
    Class representing a fluid enemy in the game.
    Inherits from the Enemy class.
    """
    def __init__(self, x, y, health, speed, target, left_image, right_image, damage, attack_cooldown, left_flame_image, right_flame_image, flame_duration):
        """
        Initializes a new instance of the FluidEnemy class.

        Args:
            x (int): The initial x-coordinate of the enemy.
            y (int): The initial y-coordinate of the enemy.
            health (int): The health points of the enemy.
            speed (float): The speed of the enemy.
            target (Player): The player object that the enemy targets.
            left_image (pygame.Surface): The image of the enemy facing left.
            right_image (pygame.Surface): The image of the enemy facing right.
            damage (int): The damage dealt by the enemy.
            attack_cooldown (int): The cooldown period between enemy attacks.
            left_flame_image (pygame.Surface): The image of the flame when enemy is facing left.
            right_flame_image (pygame.Surface): The image of the flame when enemy is facing right.
            flame_duration (int): The duration for which the flame is displayed.
        """
        # Call the constructor of the parent class (Enemy)
        super().__init__(x, y, health, speed, target, left_image, right_image, damage, attack_cooldown)

        # Additional attributes for FluidEnemy
        self.left_flame_image = left_flame_image
        self.right_flame_image = right_flame_image
        self.flame_duration = flame_duration
        self.flame_timer = 0

    def draw_flame(self, screen):
        """
        Draws the flame image on the screen.

        Args:
            screen (pygame.Surface): The game screen.
        """
        # Depending on the state of the FluidEnemy's image, the flame image is either the left version or the right version
        if self.flame_timer > 0 and self.attack_timer == 0:
            flame_image = self.left_flame_image if self.get_orientation() == self.enemy_left_image else self.right_flame_image
            flame_rect = flame_image.get_rect(center=self.rect.center)
            screen.blit(flame_image, flame_rect)

    def update(self, projectiles, player, other_enemies, screen):
        """
        Updates the fluid enemy's state.

        Args:
            projectiles (pygame.sprite.Group): The group of projectiles in the game.
            player (Player): The player object.
            other_enemies (pygame.sprite.Group): The group of other enemies in the game.
            screen (pygame.Surface): The game screen.
        """
        # Call the update method of the parent class (Enemy)
        super().update(projectiles, player, other_enemies, screen)

        if self.attack_timer == 0:
            self.flame_timer = self.flame_duration

        self.draw_flame(screen)
