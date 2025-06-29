import math
import pygame
from Projectile import Projectile

class ProjectileEnemy:
    """
    Class representing projectile-firing enemies in the game.
    """
    projectile_enemies_killed = 0
    
    def __init__(self, x, y, health, speed, target, left_image, right_image, damage, attack_cooldown, projectile_image, bullet_speed):
        """
        Initializes a new instance of the ProjectileEnemy class.

        Args:
            x (int): The initial x-coordinate of the enemy.
            y (int): The initial y-coordinate of the enemy.
            health (int): The initial health of the enemy.
            speed (float): The movement speed of the enemy.
            target (Player): The target player object.
            left_image (pygame.Surface): The image of the enemy facing left.
            right_image (pygame.Surface): The image of the enemy facing right.
            damage (int): The damage dealt by the enemy.
            attack_cooldown (int): The cooldown between enemy attacks.
            projectile_image (pygame.Surface): The image of the projectile fired by the enemy.
            bullet_speed (float): The speed of the projectile.
        """
        self.x = x
        self.y = y
        self.health = health
        self.speed = speed
        self.target = target
        self.radius = 1000000  # Distance for tracking Player
        self.damage = damage
        self.attack_cooldown = attack_cooldown
        self.attack_timer = 0
        self.hit_position = None  # Initialize hit position
        self.is_destroyed = False
        self.splat_duration = 120
        self.splat_timer = 0

        self.enemy_left_image = left_image
        self.enemy_right_image = right_image
        self.enemy_image = self.enemy_left_image
        self.rect = self.enemy_image.get_rect(topleft=(x, y))

        self.projectiles = pygame.sprite.Group()
        self.projectile_image = projectile_image
        self.speed = bullet_speed

    def move_towards(self, target_x, target_y):
        """
        Move the projectile-firing enemy towards the specified target coordinates.

        Args:
            target_x (int): X-coordinate of the target.
            target_y (int): Y-coordinate of the target.
        """
        delta_x = target_x - self.x
        delta_y = target_y - self.y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

        # Calculate speed and direction if distance to player is greater than 0
        if distance > 0:
            direction_x = delta_x / distance
            direction_y = delta_y / distance
            
            self.x += direction_x * self.speed
            self.y += direction_y * self.speed
            self.rect.topleft = (self.x, self.y)

            if direction_x > 0: # If moving right, blit right image
                self.enemy_image = self.enemy_right_image
            elif direction_x < 0: # If moving left, blit left image
                self.enemy_image = self.enemy_left_image

    def draw(self, screen):
        """
        Draw the projectile-firing enemy on the screen.

        Args:
            screen (pygame.Surface): The game screen.
        """
        if self.hit_position is not None: # If hit, blit splat image
            splat_image = pygame.image.load("Images/Splat.png")
            splat_rect = splat_image.get_rect(center=self.hit_position)
            screen.blit(splat_image, splat_rect)
            self.hit_position = None

        screen.blit(self.enemy_image, self.rect)

    def is_enemy_destroyed(self):
        """
        Check if the projectile-firing enemy is destroyed.

        Returns:
            bool: True if the enemy is destroyed, False otherwise.
        """
        return self.is_destroyed

    def receive_damage(self, damage, hit_position, screen):
        """
        Receive damage and update the projectile-firing enemy's state.

        Args:
            damage (int): The amount of damage received.
            hit_position (tuple): The position where the enemy was hit.
            screen (pygame.Surface): The game screen.
        """
        self.health -= damage 
        if self.health <= 0: # If hit and health lower or equal to zero, blit Splat and set is_destroyed to True
            self.hit_position = hit_position
            splat_image = pygame.image.load("Images/Splat.png")
            splat_rect = splat_image.get_rect(center=self.hit_position)
            screen.blit(splat_image, splat_rect)
            
            self.is_destroyed = True
            ProjectileEnemy.projectile_enemies_killed += 1
        else: # If not dead, record hit_position (Splat will be blitted in another function)
            self.hit_position = hit_position

    def update(self, projectiles, player, screen):
        """
        Update the projectile-firing enemy's state.

        Args:
            projectiles (list): List of projectile instances.
            player (Player): The player object.
            screen (pygame.Surface): The game screen.
        """
        player_coords = player.get_coords()
        distance_to_player = math.sqrt((self.rect.x - player_coords[0]) ** 2 + (self.rect.y - player_coords[1]) ** 2)
        distance_threshold = 100  # Distance threshold that ProjectileEnemies stop at

        if distance_to_player <= self.radius: # Makes sure Player is in range but not over the threshold 
            if distance_to_player > distance_threshold:
                self.move_towards(player_coords[0], player_coords[1])
                
            if self.attack_timer >= self.attack_cooldown:
                self.fire_projectile(player, screen)
                self.attack_timer = 0

        self.attack_timer += 1 # Update projectiles and check for projectile collisions
        self.projectiles.update()
        self.projectiles.draw(screen)
        self.check_collision(projectiles, screen)

    def fire_projectile(self, player, screen):
        """
        Fire a projectile towards the player.

        Args:
            player (Player): The player object.
            screen (pygame.Surface): The game screen.
        """
        # Calculate direction and speed
        delta_x = player.rect.centerx - self.rect.centerx
        delta_y = player.rect.centery - self.rect.centery
        angle = math.atan2(delta_y, delta_x)
        velocity = [self.speed * math.cos(angle), self.speed * math.sin(angle)]
        projectile_image = self.projectile_image
        projectile_rect = projectile_image.get_rect(center=self.rect.center)
        projectile = Projectile(screen, projectile_image, projectile_rect, velocity, self.damage) # Create Projectile
        self.projectiles.add(projectile) # Add to list of projectiles fired by said ProjectileEnemy

    def check_collision(self, projectiles, screen):
        """
        Check collision with Player projectiles.

        Args:
            projectiles (list): List of projectile instances.
            screen (pygame.Surface): The game screen.
        """
        for projectile in projectiles: # Check for collisions between Player projectiles and self
            if self.rect.colliderect(projectile.rect):
                self.receive_damage(projectile.damage, projectile.rect.center, screen)
                projectiles.remove(projectile) # Remove the projectiles if hit
                break

    def deal_damage_to_player(self, player):
        """
        Deal damage to the player with projectiles.

        Args:
            player (Player): The player object.
        """
        for projectile in self.projectiles:
            if projectile.rect.colliderect(player.rect):
                player.handle_damage(self.damage)
                projectile.kill() # Remove projectiles after collision
