import pygame
from Projectile import Projectile
from Enemy import Enemy
import math

class Player(pygame.sprite.Sprite):
    """
    Class representing the player in the game.
    """
    def __init__(self, screen):
        """
        Initializes a new instance of the Player class.

        Args:
            screen (pygame.Surface): The game screen.
        """
        # Call the constructor of the parent class (pygame.sprite.Sprite)
        super().__init__()
        self.screen = screen
        self.player_normal_left = pygame.image.load("Images/PlayerKunKunLeft.png")
        self.player_normal_right = pygame.image.load("Images/PlayerKunKunRight.png")
        self.player_image = self.player_normal_left
        self.rect = self.player_image.get_rect()
        self.rect.center = (screen.get_width() // 2, screen.get_height() // 2)

        self.projectiles = pygame.sprite.Group()   
        self.projectile_damage = 50

        self.is_hit = False
        self.is_killed = False

        self.player_speed = 2
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        self.health = 30000

        self.splat_timer = 0
        self.splat_duration = 360
        self.hit_position = None

    def update(self, cursor_position):
        """
        Update the player's state.

        Args:
            cursor_position (tuple): The position of the cursor.
        """
        direction_vector = pygame.math.Vector2(cursor_position[0] - self.rect.centerx, cursor_position[1] - self.rect.centery)
        angle = math.degrees(math.atan2(direction_vector.y, direction_vector.x))

        if -90 <= angle <= 90: # If cursor is facing right half of screen, Player image is player_right
            self.player_image = self.player_normal_right
        else:
            self.player_image = self.player_normal_left # If cursor is facing left half of screen, Player image is player_left

        self.update_projectiles()

        if self.splat_timer > 0:
            self.splat_timer -= 1
            if self.splat_timer == 0:
                self.hit_position = None

    def move_left(self):
        """Move the player left."""
        self.rect.x -= self.player_speed

    def move_right(self):
        """Move the player right."""
        self.rect.x += self.player_speed

    def move_up(self):
        """Move the player up."""
        self.rect.y -= self.player_speed

    def move_down(self):
        """Move the player down."""
        self.rect.y += self.player_speed

    def draw(self):
        """Draw the player on the screen."""
        self.screen.blit(self.player_image, self.rect)
        if self.hit_position is not None:
            splat_image = pygame.image.load("Images/Splat.png")
            splat_rect = splat_image.get_rect(center=self.hit_position)
            self.screen.blit(splat_image, splat_rect)  # Draw the splat image above the enemy
            self.hit_position = None

    def move_player(self):
        """Move the player based on keyboard input."""
        if self.moving_left:
            self.move_left()
        if self.moving_right:
            self.move_right()
        if self.moving_up:
            self.move_up()
        if self.moving_down:
            self.move_down()

    def handle_movement(self, event):
        """
        Handle keyboard input for player movement.

        Args:
            event (pygame.event.Event): The pygame event.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.moving_left = True
            elif event.key == pygame.K_d:
                self.moving_right = True
            elif event.key == pygame.K_w:
                self.moving_up = True
            elif event.key == pygame.K_s:
                self.moving_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.moving_left = False
            elif event.key == pygame.K_d:
                self.moving_right = False
            elif event.key == pygame.K_w:
                self.moving_up = False
            elif event.key == pygame.K_s:
                self.moving_down = False

    def shoot(self, target_position):
        """
        Shoot a projectile towards the specified target position.

        Args:
            target_position (tuple): The position of the target.
        """
        # Handle projectile speed and direction
        projectile_image = pygame.image.load("Images/KunKunAttack.png")
        projectile_rect = projectile_image.get_rect()
        projectile_rect.center = self.rect.center
        projectile_damage = self.projectile_damage

        direction = math.atan2(target_position[1] - self.rect.centery, target_position[0] - self.rect.centerx)
        speed = 15 # Projectile speed
        projectile_velocity = [speed * math.cos(direction), speed * math.sin(direction)]

        self.projectiles.add(Projectile(self.screen, projectile_image, projectile_rect, projectile_velocity, projectile_damage))

    def draw_projectiles(self):
        """Draw the player's projectiles on the screen."""
        self.projectiles.draw(self.screen)

    def handle_shooting(self, event):
        """
        Handle mouse input for shooting projectiles.

        Args:
            event (pygame.event.Event): The pygame event.
        """
        # Shoot at mouse position
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self.shoot(mouse_pos)

    def check_collision(self, enemies):
        """
        Check collision between player projectiles and enemies.

        Args:
            enemies (list): List of enemy instances.
        """
        for projectile in self.projectiles:
            for enemy in enemies:
                if enemy.rect.colliderect(projectile.rect):
                    enemy.receive_damage(projectile.damage)
                    self.projectiles.remove(projectile)
                    break  # Exit loop after handling one collision

    def handle_damage(self, damage):
        """
        Handle damage to the player.

        Args:
            damage (int): The amount of damage received.
        """
        self.health -= damage
        self.hit_position = self.rect.center
        self.splat_timer = self.splat_duration
        if self.health <= 0:
            self.is_killed = True

    def get_coords(self):
        """
        Get the player's current coordinates.

        Returns:
            tuple: The player's (x, y) coordinates.
        """
        return self.rect.center

    def is_destroyed(self):
        """
        Check if the player is destroyed.

        Returns:
            bool: True if the player is destroyed, False otherwise.
        """
        return self.is_killed

    def update_projectiles(self):
        """Update the player's projectiles."""
        self.projectiles.update()

    def get_health(self):
        """
        Get the player's current health.

        Returns:
            int: The player's health.
        """
        return self.health

    def render_health(self, screen):
        """
        Render the player's health on the screen.

        Args:
            screen (pygame.Surface): The game screen.
        """
        font = pygame.font.Font(None, 36) 
        health_text = font.render(f"Health: {self.health}", True, (255, 255, 255))
        screen.blit(health_text, (10, screen.get_height() - 50))

    def set_health(self, health):
        """Set Player health"""
        self.health = health
