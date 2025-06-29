import math
import pygame

class Enemy:
    """
    Class representing melee enemies in the game.
    """
    enemies_killed = 0

    def __init__(self, x, y, health, speed, target, left_image, right_image, damage, attack_cooldown):
        """
        Initializes a new instance of the Enemy class.

        Args:
            x (int): The initial x-coordinate of the enemy.
            y (int): The initial y-coordinate of the enemy.
            health (int): The initial health of the enemy.
            speed (float): The movement speed of the enemy.
            target (Player): The player object targeted by the enemy.
            left_image (pygame.Surface): The image of the enemy facing left.
            right_image (pygame.Surface): The image of the enemy facing right.
            damage (int): The damage dealt by the enemy.
            attack_cooldown (int): The cooldown period between enemy attacks.
        """
        self.x = x
        self.y = y
        self.health = health
        self.speed = speed
        self.target = target
        self.radius = 100000  # Distance for tracking Player
        self.damage = damage
        self.attack_cooldown = attack_cooldown
        self.attack_timer = 0
        self.hit_position = None  # Initialize hit position
        self.is_destroyed = False
        self.splat_duration = 120
        self.splat_timer = 0

        # Load enemy images
        self.enemy_left_image = left_image
        self.enemy_right_image = right_image
        self.enemy_image = self.enemy_left_image
        self.rect = self.enemy_image.get_rect(topleft=(x, y))

    def move_towards(self, target_x, target_y, other_enemies):
        """
        Move the enemy towards the specified coordinates while avoiding collisions with other enemies.

        Args:
            target_x (int): X-coordinate of the target position.
            target_y (int): Y-coordinate of the target position.
            other_enemies (list): List of other Enemy objects in the game.
        """
        delta_x = target_x - self.x
        delta_y = target_y - self.y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

        # Calculate movement direction and speed
        if distance > 0:
            direction_x = delta_x / distance 
            direction_y = delta_y / distance

            new_x = self.x + direction_x * self.speed
            new_y = self.y + direction_y * self.speed

            for enemy in other_enemies:
                if enemy != self and pygame.Rect(new_x, new_y, self.rect.width, self.rect.height).colliderect(enemy.rect):
                    new_x, new_y = self.avoid_overlap(new_x, new_y, enemy.rect)

            self.x = new_x
            self.y = new_y
            self.rect.topleft = (self.x, self.y)

            if direction_x > 0: # If moving right, change image to right_image
                self.enemy_image = self.enemy_right_image
            elif direction_x < 0: # If moving left, change image to left_image
                self.enemy_image = self.enemy_left_image

    def avoid_overlap(self, new_x, new_y, other_rect):
        """
        Adjust the new coordinates to avoid overlap with another rectangle.

        Args:
            new_x (int): The new x-coordinate to be adjusted.
            new_y (int): The new y-coordinate to be adjusted.
            other_rect (pygame.Rect): The rectangle to avoid overlap with.

        Returns:
            Tuple[int, int]: Adjusted x and y coordinates.
        """
        if new_x < other_rect.left:
            new_x = other_rect.left - self.rect.width
        elif new_x > other_rect.right - self.rect.width:
            new_x = other_rect.right
        if new_y < other_rect.top:
            new_y = other_rect.top - self.rect.height
        elif new_y > other_rect.bottom - self.rect.height:
            new_y = other_rect.bottom

        return new_x, new_y

    def draw(self, screen):
        """
        Draw the enemy on the specified screen.

        Args:
            screen (pygame.Surface): The screen to draw the enemy on.
        """
        if self.hit_position is not None:
            splat_image = pygame.image.load("Images/Splat.png")
            splat_rect = splat_image.get_rect(center=self.hit_position)
            screen.blit(splat_image, splat_rect)
            self.hit_position = None

        screen.blit(self.enemy_image, self.rect)

    def is_enemy_destroyed(self):
        """
        Check if the enemy is destroyed.

        Returns:
            bool: True if the enemy is destroyed, False otherwise.
        """
        return self.is_destroyed

    def receive_damage(self, damage, hit_position, screen):
        """
        Receive damage and update the enemy's state.

        Args:
            damage (int): Amount of damage received.
            hit_position (Tuple[int, int]): Position where the enemy was hit.
            screen (pygame.Surface): The screen to display the hit effect.
        """
        self.health -= damage
        if self.health <= 0: 
            self.hit_position = hit_position # If hit dead, get hit position and blit image and change is_destroyed to True
            splat_image = pygame.image.load("Images/Splat.png")
            splat_rect = splat_image.get_rect(center=self.hit_position)
            screen.blit(splat_image, splat_rect)
            
            self.is_destroyed = True 
            Enemy.enemies_killed += 1
        else: # Otherwise, just get hit position (Splat will be blitted in another function)
            self.hit_position = hit_position

    def update(self, projectiles, player, other_enemies, screen):
        """
        Update the state of the enemy in the game loop.

        Args:
            projectiles (list): List of projectiles in the game.
            player (Player): The player object.
            other_enemies (list): List of other Enemy objects in the game.
            screen (pygame.Surface): The screen to display the enemy and effects.
        """
        player_coords = self.target.get_coords()
        distance_to_player = math.sqrt((self.rect.x - player_coords[0]) ** 2 + (self.rect.y - player_coords[1]) ** 2)

        if distance_to_player <= self.radius:
            self.move_towards(player_coords[0], player_coords[1], other_enemies)

        self.attack_timer += 1 # Attack if not on cooldown
        if self.attack_timer >= self.attack_cooldown:
            self.attack_timer = 0
            self.deal_damage_to_player(player)

        if self.splat_timer > 0: # Splat timer countdown
            self.splat_timer -= 1
            if self.splat_timer == 0: # If splat timer ends, remove the effect
                self.hit_position = None

        self.check_collision(projectiles, screen)

    def check_collision(self, projectiles, screen):
        """
        Check for collisions with projectiles and update the enemy state.

        Args:
            projectiles (list): List of projectiles in the game.
            screen (pygame.Surface): The screen to display effects.
        """
        for projectile in projectiles: # Keep track of projectiles and if they collide with Enemy
            if self.rect.colliderect(projectile.rect):
                self.receive_damage(projectile.damage, projectile.rect.center, screen)
                projectiles.remove(projectile)
                break

    def deal_damage_to_player(self, player):
        """
        Deal damage to the player.

        Args:
            player (Player): The player object.
        """
        player_rect = player.rect
        if self.rect.colliderect(player_rect):
            player.handle_damage(self.damage)
            self.hit_position = player_rect.center
            self.splat_timer = self.splat_duration # Begin splat timer countdown for blitting the splat image.

    def get_orientation(self):
        """
        Get the orientation of the enemy.

        Returns:
            pygame.Surface: The image representing the enemy's orientation.
        """
        return self.enemy_image
