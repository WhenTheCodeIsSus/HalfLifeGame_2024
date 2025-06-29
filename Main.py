import pygame
import math
from Player import Player
from Target import Target
from Enemy import Enemy
from ProjectileEnemy import ProjectileEnemy
from FluidEnemy import FluidEnemy

# Constants
WIDTH, HEIGHT = 800, 600
TITLE_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 100, 100)
FPS = 60
WAVE_NUMBER = 0

pygame.init() # Init Pygame

game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game Menu')
clock = pygame.time.Clock()

def create_main_menu(screen):
    """
    Creates the main menu screen and handles button selection.

    Args:
        screen (pygame.Surface): The game screen.

    Returns:
        str: The selected button.
    """

    # Create the labels and rects
    font_title = pygame.font.Font("Fonts/Freedom-10eM.ttf", 80)
    font_buttons = pygame.font.Font("Fonts/Freedom-10eM.ttf", 40)
    title_text = font_title.render("Funny Game", True, TITLE_COLOR)
    start_text = font_buttons.render("Start", True, BUTTON_COLOR)
    tutorial_text = font_buttons.render("Tutorial", True, BUTTON_COLOR)
    exit_text = font_buttons.render("Exit Game", True, BUTTON_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    tutorial_rect = tutorial_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    def draw_buttons(selected_button):
        """
        Draws the buttons on the main menu screen.

        Args:
            selected_button (str): The currently selected button.

        Returns:
            None
        """

        # Blit the labels
        game_screen.blit(title_text, title_rect)
        game_screen.blit(start_text, start_rect)
        game_screen.blit(tutorial_text, tutorial_rect)
        game_screen.blit(exit_text, exit_rect)

    def handle_button_selection(mouse_pos):
        """
        Handles button selection on the main menu screen.

        Args:
            mouse_pos (tuple): The mouse coordinates (x, y).

        Returns:
            str: The selected button.
        """
        selected_button = None
        for event in pygame.event.get(): # If user tries to close window, return Exit Game
            if event.type == pygame.QUIT:
                return "Exit Game"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(mouse_pos): # If pressed Start, return Start
                    selected_button = "Start"
                elif tutorial_rect.collidepoint(mouse_pos): # If pressed Tutorial, return Tutorial
                    selected_button = "Tutorial"
                elif exit_rect.collidepoint(mouse_pos): #If pressed Exit Game, return Exit Game
                    return "Exit Game"
        return selected_button

    selected_button = None
    while True:
        game_screen.fill((0, 0, 0))
        draw_buttons(selected_button)
        mouse_pos = pygame.mouse.get_pos()
        selected_button = handle_button_selection(mouse_pos)
        pygame.display.flip()
        clock.tick(FPS)
        if selected_button:
            return selected_button

def run_start_screen():
    """
    Runs the main game screen where the player faces different waves of enemies.
    """
     
    global WAVE_NUMBER

    player = Player(game_screen)
    enemies = []
    projectile_enemies = []
    fluid_enemies = []

    clock = pygame.time.Clock()
    running = True
    paused = False
    # Get the maps
    stone_map = pygame.image.load("Images/StoneBrickFloor.jpg")
    desert_map = pygame.image.load("Images/DesertFloor.jpg")
    grass_map = pygame.image.load("Images/GrassFloor.png")
    
    
    screen_boundary = pygame.Rect(0, 0, WIDTH, HEIGHT)

    # Create font for Wave Label
    font = pygame.font.Font(None, 36)
    wave_label = font.render(f"Current Wave: {WAVE_NUMBER}", True, (255, 255, 255))
    wave_rect = wave_label.get_rect(bottomright=(WIDTH - 20, HEIGHT - 30))

    while running:
        if WAVE_NUMBER < 9:
            game_screen.blit(stone_map, (0, 0)) # If Wave is under 9, blit stone map

        elif WAVE_NUMBER < 14 and WAVE_NUMBER > 8:
            game_screen.blit(desert_map, (0, 0)) # If Wave is under 14, blit desert map

        elif WAVE_NUMBER < 18 and WAVE_NUMBER > 13:
            game_screen.blit(grass_map, (0, 0)) # If Wave is under 18, blit grass map

        game_screen.blit(wave_label, wave_rect) # Blit the current wave label


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If user tries to exit screen, clear the stats
                Enemy.enemies_killed = 0
                ProjectileEnemy.projectile_enemies_killed = 0
                WAVE_NUMBER = 0
                running = False # Close window
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # Toggle pause state

            player.handle_movement(event)
            player.handle_shooting(event)

        if paused: # When paused, if user resumes, continue. If user tries to return to menu, clear stats. If user tries to close window, clear stats and return to menu
            pause_option = pause_screen(game_screen)
            if pause_option == "Resume":
                paused = False
            elif pause_option == "Menu":
                Enemy.enemies_killed = 0
                ProjectileEnemy.projectile_enemies_killed = 0
                WAVE_NUMBER = 0
                running = False
            elif pause_option == "Exit":
                Enemy.enemies_killed = 0
                ProjectileEnemy.projectile_enemies_killed = 0
                WAVE_NUMBER = 0
                running = False

        # Update Player 
        player.move_player()
        player.update_projectiles()
        
        # Update Enemy
        for enemy in enemies:
            enemy.update(player.projectiles, player, enemies + projectile_enemies + fluid_enemies, game_screen)
            enemy.draw(game_screen)
            enemy.deal_damage_to_player(player)

            if enemy.is_enemy_destroyed():
                enemies.remove(enemy)
                
        # Update Projectile Enemy
        for projectile_enemy in projectile_enemies:
            projectile_enemy.update(player.projectiles, player, game_screen)  
            projectile_enemy.draw(game_screen)
            projectile_enemy.deal_damage_to_player(player)

            if projectile_enemy.is_enemy_destroyed():
                projectile_enemies.remove(projectile_enemy)
                
        # Update Fluid Enemy
        for fluid_enemy in fluid_enemies:
            fluid_enemy.update(player.projectiles, player, enemies + projectile_enemies + fluid_enemies, game_screen)
            fluid_enemy.draw(game_screen)
            fluid_enemy.deal_damage_to_player(player)

            if fluid_enemy.is_enemy_destroyed():
                fluid_enemies.remove(fluid_enemy)
                
        #Check if Player is destroyed, if so, display game over screen and clear stats.
        if player.is_destroyed():
            if WAVE_NUMBER < 18:
                display_game_over_screen(player, Enemy.enemies_killed, ProjectileEnemy.projectile_enemies_killed, WAVE_NUMBER, 30000)
                Enemy.enemies_killed = 0
                ProjectileEnemy.projectile_enemies_killed = 0
                WAVE_NUMBER = 0
                selected = create_main_menu(game_screen)  # Go back to the main menu
            running = False

        #Get Player speed
        new_x = player.rect.x
        new_y = player.rect.y

        if player.moving_left:
            new_x -= player.player_speed
        if player.moving_right:
            new_x += player.player_speed
        if player.moving_up:
            new_y -= player.player_speed
        if player.moving_down:
            new_y += player.player_speed

        # Boundary check
        player.rect.x = min(max(new_x, screen_boundary.left), screen_boundary.right - player.rect.width)
        player.rect.y = min(max(new_y, screen_boundary.top), screen_boundary.bottom - player.rect.height)

        #Update rest of Player
        player.draw()
        player.draw_projectiles()
        player.render_health(game_screen)  # Rendering player health screen
        cursor_position = pygame.mouse.get_pos()
        player.update(cursor_position)

        # Check if all enemies are destroyed, then spawn a new wave
        if not enemies and not projectile_enemies and not fluid_enemies:
            if WAVE_NUMBER == 17: # If Game is completed, display victory screen and then clear stats
                display_game_over_screen(player, Enemy.enemies_killed, ProjectileEnemy.projectile_enemies_killed, WAVE_NUMBER, 30000)
                Enemy.enemies_killed = 0
                ProjectileEnemy.projectile_enemies_killed = 0
                WAVE_NUMBER = -1
                selected = create_main_menu(game_screen)  # Go back to the main menu
                running = False

            else: #  If Wave is 0 (hasn't started yet) display the initial text alerting the Player that game is starting
                if  WAVE_NUMBER == 0:
                    initial_font = pygame.font.Font(None, 48)
                    initial_text = f"Game Starting in 3 Seconds!"
                    initial_label = initial_font.render(initial_text, True, (255, 255, 255))
                    initial_rect = initial_label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    
                    game_screen.fill((0,0,0))
                    game_screen.blit(stone_map, (0,0))
                    game_screen.blit(initial_label, initial_rect)
                    pygame.display.flip()

                    pygame.time.delay(3000)

                    pygame.display.flip()

                else: # Otherwise, display the wave completed and the upcoming wave.
                    completion_font = pygame.font.Font(None, 48)
                    completion_text = f"Wave {WAVE_NUMBER} completed! Wave {WAVE_NUMBER + 1} starting..."
                    completion_label = completion_font.render(completion_text, True, (255, 255, 255))
                    completion_rect = completion_label.get_rect(center=(WIDTH // 2, HEIGHT // 2))

                    game_screen.blit(completion_label, completion_rect)
                    pygame.display.flip()

                    pygame.time.delay(5000)

                    pygame.display.flip()

            
            if WAVE_NUMBER == 9: # At 9th wave, new enemies are introduced, so previous enemies are cleared from list
                projectile_enemies.clear()
                enemies.clear()

            if WAVE_NUMBER == 13: # At 13th wave, new enemies are introduced, so previous enemies are cleared from list
                projectile_enemies.clear()
                enemies.clear()

            if WAVE_NUMBER == 18: # At 18th wave, new enemies are introduced, so previous enemies are cleared from list
                projectile_enemies.clear()
                fluid_enemies.clear()
                enemies.clear()
                
            WAVE_NUMBER += 1 # Add 1 to Wave after each completed wave
            wave_label = font.render(f"Current Wave: {WAVE_NUMBER}", True, (255, 255, 255)) # Change the wave label
            spawn_wave(enemies, projectile_enemies, fluid_enemies, WAVE_NUMBER, player) # Spawn new wave

        
        pygame.display.flip() # Update display
        clock.tick(FPS) # Keep tick constant
    

def run_tutorial_screen():
    """
    Runs the tutorial screen to introduce the player to the game mechanics.
    """
    # Create screen parameters
    screen = pygame.display.set_mode((800, 600))
    screen_boundary = pygame.Rect(0, 0, WIDTH, 500)
    pygame.display.set_caption('Tutorial Screen One')
    
    # Get images
    player = Player(screen)
    background = pygame.image.load('Images/StoneBrickFloor.jpg')
    targets = [Target(50 + i * 200, 50, 1000, "Images/Target.png", "Images/TargetSmokeEffect.png", "Images/TargetDestroyEffect.png") for i in range(4)]
    portal_image = pygame.image.load("Images/BluePortal.png")
    portal_rect = portal_image.get_rect(center=(400, 250))
    portal_active = False

    running = True
    paused = False
    panel_text = "W A S D to move! Hit the Targets Once or More!"
    while running:
        screen.blit(background, (0, 0)) # Blit background

        # Update targets
        for target in targets:
            target.draw(screen)
            target.update()

        panel = pygame.Surface((WIDTH, 100))
        panel.fill((0, 0, 0))
        font = pygame.font.Font("Fonts/AdventPro.ttf", 36)

        targets = [target for target in targets if not target.is_target_destroyed()]
        # Check for collisions between targets and projectiles
        for projectile in player.projectiles:
            collided_targets = [target for target in targets if target.rect.colliderect(projectile.rect)]
            for target in collided_targets: # Draw hit effect if hit
                target.hit()
                target.draw(screen)
                portal_active = True
                target.receive_damage(projectile.get_damage())
                if target.is_target_destroyed(): # Draw destroyed effect if destroyed
                    target.draw(screen)
                    targets.remove(target)

        cursor_position = pygame.mouse.get_pos()
        player.update(cursor_position)  # Passing the targets list to the player's update method
        player.draw()
        player.update_projectiles()
        player.draw_projectiles()

        # Update target hit status and display appropriate panel text
        if portal_active:
            font = pygame.font.Font("Fonts/AdventPro.ttf", 20)
            panel_text = "Target Hit! Time to face live enemies! Go through the portal."
            screen.blit(portal_image, portal_rect)

        if portal_active and player.rect.colliderect(portal_rect):
            running = False # Close window if Player goes through portal

        text = font.render(panel_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, 50))

        panel = pygame.Surface((WIDTH, 100)) # Blit text panel underneath the game window
        panel.fill((0, 0, 0))
        panel.blit(text, text_rect)
        screen.blit(panel, (0, HEIGHT - 100))

        for event in pygame.event.get(): # If user tries to close window, running = False
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

            # Update Player
            player.handle_movement(event)
            player.handle_shooting(event)

        if paused: # Depending on user interaction, either pause game, or return to menu
            pause_option = pause_screen(screen)
            if pause_option == "Resume": 
                paused = False
            elif pause_option == "Menu":
                running = False
            elif pause_option == "Exit":
                running = False

        # Get Player speed information
        new_x = player.rect.x
        new_y = player.rect.y

        if player.moving_left:
            new_x -= player.player_speed
        if player.moving_right:
            new_x += player.player_speed
        if player.moving_up:
            new_y -= player.player_speed
        if player.moving_down:
            new_y += player.player_speed

        # Boundary check
        player.rect.x = min(max(new_x, screen_boundary.left), screen_boundary.right - player.rect.width)
        player.rect.y = min(max(new_y, screen_boundary.top), screen_boundary.bottom - player.rect.height)

        player.move_player()

        pygame.display.flip()
        clock.tick(FPS)


def pause_screen(screen):
    """
    Displays a pause screen with options to resume, return to the menu, or exit the game.

    Args:
        screen (pygame.Surface): The game screen.

    Returns:
        str: The selected option.
    """
    # Create texts
    font = pygame.font.Font("Fonts/Freedom-10eM.ttf", 40)
    resume_text = font.render("Resume", True, BUTTON_COLOR)
    menu_text = font.render("Return to Menu", True, BUTTON_COLOR)
    resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def draw_buttons(selected_button):
        """
        Draws the buttons on the pause screen.

        Args:
            selected_button (str): The currently selected button.

        Returns:
            None
        """
        screen.fill((0, 0, 0))
        screen.blit(resume_text, resume_rect)
        screen.blit(menu_text, menu_rect)
        
        if selected_button == "Resume":
            pygame.draw.rect(screen, resume_rect)
        elif selected_button == "Menu":
            pygame.draw.rect(screen, menu_rect)

    def handle_button_selection(mouse_pos):
        """
        Handles button selection on the pause screen.

        Args:
            mouse_pos (tuple): The mouse coordinates (x, y).

        Returns:
            str: The selected button.
        """
        selected_button = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(mouse_pos):
                    selected_button = "Resume"
                elif menu_rect.collidepoint(mouse_pos):
                    selected_button = "Menu"
        return selected_button

    selected_button = None
    while True:
        mouse_pos = pygame.mouse.get_pos()
        draw_buttons(selected_button)
        selected_button = handle_button_selection(mouse_pos)
        pygame.display.flip()
        clock.tick(FPS)
        if selected_button:
            return selected_button

def display_game_over_screen(player, enemies_killed, projectile_enemies_killed, waves, player_health):
    """
    Displays the game over screen with relevant statistics.

    Args:
        player (Player): The player instance.
        enemies_killed (int): Number of melee enemies killed.
        projectile_enemies_killed (int): Number of projectile enemies killed.
        waves (int): The wave number reached.
    """
    font_large = pygame.font.Font(None, 60)
    font_medium = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 30)

    if waves == 17: # If waves reached 17 (completed), the Player wins and win screen is displayed
        congrats_text = font_large.render("Congratulations! You Win!", True, (255, 255, 255))
    else: # If anything happens and 17 is not completed, a Game Over screen is displayed
        congrats_text = font_large.render("Game Over!", True, (255, 255, 255))
        
    # Render Player statistics
    enemies_killed_text = font_medium.render(f"Melee Enemies Killed: {enemies_killed}", True, (255, 255, 255))
    projectile_killed_text = font_medium.render(f"Projectile Enemies Killed: {projectile_enemies_killed}", True, (255, 255, 255))
    waves_text = font_medium.render(f"Waves: {waves}", True, (255, 255, 255))
    exit_text = font_small.render("Exit to Menu", True, (255, 255, 255))

    congrats_rect = congrats_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    enemies_killed_rect = enemies_killed_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    projectile_killed_rect = projectile_killed_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    waves_rect = waves_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

    # Restore Player health
    player.set_health(player_health)

    while True:
        game_screen.fill((0, 0, 0))
        game_screen.blit(congrats_text, congrats_rect)
        game_screen.blit(enemies_killed_text, enemies_killed_rect)
        game_screen.blit(projectile_killed_text, projectile_killed_rect)
        game_screen.blit(waves_text, waves_rect)
        game_screen.blit(exit_text, exit_rect)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(mouse_pos):
                    return "Exit"

        pygame.display.flip()
        clock.tick(FPS)


            
def spawn_wave(enemies, projectile_enemies, fluid_enemies, wave_number, player):
    """
    Spawns a wave of enemies based on the current wave number.

    Args:
        enemies (list): List of melee enemies.
        projectile_enemies (list): List of projectile enemies.
        fluid_enemies (list): List of fluid enemies.
        wave_number (int): The current wave number.
        player (Player): The player instance.
    """
    #Stage One Enemies Images
    left_image_enemy = pygame.image.load("Images/EnemyAssets/StageOne/CombineCivilProtectionLeft.png")
    right_image_enemy = pygame.image.load("Images/EnemyAssets/StageOne/CombineCivilProtectionRight.png")
    
    left_image_projectile_regular_enemy = pygame.image.load("Images/EnemyAssets/StageOne/CombineRegularSoldierLeft.png")
    right_image_projectile_regular_enemy = pygame.image.load("Images/EnemyAssets/StageOne/CombineRegularSoldierRight.png")
    
    left_image_projectile_grunt = pygame.image.load("Images/EnemyAssets/StageOne/CombineHeavyLeft.png")
    right_image_projectile_grunt = pygame.image.load("Images/EnemyAssets/StageOne/CombineHeavyRight.png")
    
    left_image_projectile_elite = pygame.image.load("Images/EnemyAssets/StageOne/CombineEliteLeft.png")
    right_image_projectile_elite = pygame.image.load("Images/EnemyAssets/StageOne/CombineEliteRight.png")

    #Stage Two Enemies Images
    left_image_worker = pygame.image.load("Images/EnemyAssets/StageTwo/CombineWorkerLeft.png")
    right_image_worker = pygame.image.load("Images/EnemyAssets/StageTwo/CombineWorkerRight.png")

    left_image_hazmat = pygame.image.load("Images/EnemyAssets/StageTwo/CombineHazmatWorkerLeft.png")
    right_image_hazmat = pygame.image.load("Images/EnemyAssets/StageTwo/CombineHazmatWorkerRight.png")

    left_image_hazmat_2 = pygame.image.load("Images/EnemyAssets/StageTwo/CombineHazmatWorkerV2Left.png")
    right_image_hazmat_2 = pygame.image.load("Images/EnemyAssets/StageTwo/CombineHazmatWorkerV2Right.png")

    #Stage Three Enemies Images
    left_image_qz_soldier = pygame.image.load("Images/EnemyAssets/StageThree/CombineQZSoldierLeft.png")
    right_image_qz_soldier = pygame.image.load("Images/EnemyAssets/StageThree/CombineQZSoldierRight.png")

    left_image_qz_commander = pygame.image.load("Images/EnemyAssets/StageThree/CombineQZCommanderLeft.png")
    right_image_qz_commander = pygame.image.load("Images/EnemyAssets/StageThree/CombineQZCommanderRight.png")

    left_image_qz_suppressor = pygame.image.load("Images/EnemyAssets/StageThree/CombineQZSuppressorLeft.png")
    right_image_qz_suppressor = pygame.image.load("Images/EnemyAssets/StageThree/CombineQZSuppressorRight.png")

    left_image_qz_charger = pygame.image.load("Images/EnemyAssets/StageThree/CombineQZChargerLeft.png")
    right_image_qz_charger = pygame.image.load("Images/EnemyAssets/StageThree/CombineQZChargerRight.png")

    #Projectiles Images
    regular_projectile_image = pygame.image.load("Images/Bullet.png")
    grunt_projectile_image = pygame.image.load("Images/GruntBullet.png")
    elite_projectile_image = pygame.image.load("Images/EliteBullet.png")
    acid_projectile_image = pygame.image.load("Images/AcidicBullet.png")
    flame_effect_left = pygame.image.load("Images/FlameEffectLeft.png")
    flame_effect_right = pygame.image.load("Images/FlameEffectRight.png")

    #Stage One
    if wave_number <= 8:
        num_enemies = wave_number + 3
        num_regular_projectile_enemies = wave_number + 2
        num_grunt_enemies = wave_number - 3
        num_elite_enemies = wave_number - 5

        for i in range(num_enemies):
            enemy = Enemy(100 * (i + 1), 100 * (i + 1), 70, 3, player, left_image_enemy, right_image_enemy, 5, 360)
            enemies.append(enemy)

        for i in range(num_regular_projectile_enemies):
            projectile_enemy = ProjectileEnemy(200 * (i + 1), 200 * (i + 1), 100, 0.7, player, left_image_projectile_regular_enemy, right_image_projectile_regular_enemy, 8, 60, regular_projectile_image, 6.5)
            projectile_enemies.append(projectile_enemy)

        for i in range(num_grunt_enemies):
            grunt_enemy = ProjectileEnemy(300 * (i + 1), 300 * (i + 1), 300, 0.4, player, left_image_projectile_grunt, right_image_projectile_grunt, 10, 45, grunt_projectile_image, 4)
            projectile_enemies.append(grunt_enemy)

        for i in range(num_elite_enemies):
            elite_enemy = ProjectileEnemy(400 * (i + 1), 400 * (i + 1), 200, 1.2, player, left_image_projectile_elite, right_image_projectile_elite, 20, 30, elite_projectile_image, 8)
            projectile_enemies.append(elite_enemy)

    #Stage 2
    elif wave_number <= 13 and wave_number > 8:
        num_worker = (wave_number) * 3 - 20
        num_hazmat = wave_number + 3
        num_hazmat_2 = wave_number - 5

        for i in range(num_worker):
            worker_enemy = FluidEnemy(100 * (i + 1), 100 * (i + 1), 25, 4, player, left_image_worker, right_image_worker, 10, 20, flame_effect_left, flame_effect_right, 300000)
            fluid_enemies.append(worker_enemy)

        for i in range(num_hazmat):
            hazmat_enemy = ProjectileEnemy(400 * (i + 1), 400 * (i + 1), 100, 1.2, player, left_image_hazmat, right_image_hazmat, 20, 30, acid_projectile_image, 8)
            projectile_enemies.append(hazmat_enemy)

        for i in range(num_hazmat_2):
            hazmat_enemy_2 = ProjectileEnemy(400 * (i + 1), 400 * (i + 1), 400, 3, player, left_image_hazmat_2, right_image_hazmat_2, 50, 160, grunt_projectile_image, 4)
            projectile_enemies.append(hazmat_enemy_2)

    #Stage 3
    elif wave_number <= 17 and wave_number > 13:
        num_qz_soldier = wave_number - 5
        num_qz_commander = wave_number - 8
        num_qz_suppressor = wave_number - 7
        num_qz_charger = wave_number - 8

        for i in range(num_qz_soldier):
            qz_soldier_enemy = ProjectileEnemy(200 * (i + 1), 200 * (i + 1), 100, 0.7, player, left_image_qz_soldier, right_image_qz_soldier, 8, 40, regular_projectile_image, 7.5)
            projectile_enemies.append(qz_soldier_enemy)

        for i in range(num_qz_commander):
            qz_commander_enemy = ProjectileEnemy(200 * (i + 1), 200 * (i + 1), 100, 0.7, player, left_image_qz_commander, right_image_qz_commander, 10, 60, regular_projectile_image, 7)
            projectile_enemies.append(qz_commander_enemy)

        for i in range(num_qz_suppressor):
            qz_suppressor_enemy = ProjectileEnemy(300 * (i + 1), 300 * (i + 1), 300, 0.4, player, left_image_qz_suppressor, right_image_qz_suppressor, 8, 45, grunt_projectile_image, 5)
            projectile_enemies.append(qz_suppressor_enemy)

        for i in range(num_qz_charger):
            qz_charger_enemy = ProjectileEnemy(400 * (i + 1), 400 * (i + 1), 200, 1.2, player, left_image_qz_charger, right_image_qz_charger, 3, 5, elite_projectile_image, 4)
            projectile_enemies.append(qz_charger_enemy)

    
            
    



#Main loop
selected = None
while selected != "Exit Game":
    selected = create_main_menu(game_screen)

    if selected == "Start":
        run_start_screen()
    
    if selected == "Tutorial":
        run_tutorial_screen()
        

#Quit Pygame
pygame.quit()
