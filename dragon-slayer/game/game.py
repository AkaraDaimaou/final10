import random
import pygame
import os
import sys
import json

# Initialize Pygame
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Paths to sound files
flap_sound_path = os.path.join(script_dir, "sounds", "wing.wav")
collision_sound_path = os.path.join(script_dir, "sounds", "hit.wav")
score_sound_path = os.path.join(script_dir, "sounds", "point.wav")

# Load sounds with exception handling
def load_sound(sound_path):
    try:
        return pygame.mixer.Sound(sound_path)
    except Exception as e:
        print(f"Unable to load sound {sound_path}: {e}")
        sys.exit(1)

flap_sound = load_sound(flap_sound_path)
collision_sound = load_sound(collision_sound_path)
score_sound = load_sound(score_sound_path)

# Screen dimensions and settings
window_width = 600
window_height = 499
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Dragon Game")

# Game constants
elevation = window_height * 0.8
framepersecond = 60
framepersecond_clock = pygame.time.Clock()
PIPE_GAP_MIN = 150
PIPE_GAP_MAX = 250
PIPE_VELOCITY_X = -4

# Load game images
def load_image(image_name):
    try:
        image_path = os.path.join(script_dir, "images", image_name)
        image = pygame.image.load(image_path)
    except Exception as e:
        print(f"Unable to load image {image_path}: {e}")
        sys.exit(1)
    return image

game_images = {
    "background": load_image("background.png"),
    "flappydragon": load_image("bluebird.png"),
    "pipeimage": (load_image("pipe_up.png"), load_image("pipe_bottom.png")),
    "sea_level": load_image("base.png"),
    "scoreimages": [load_image(f"{i}.png") for i in range(10)],
    "game_over": load_image("game_over.png"),  # Load game over image
    "message": load_image("message.png"),      # Load message image
    "restart_button": load_image("restart_button.png")  # Load restart button image
}

# Path to the leaderboard file
leaderboard_file = os.path.join(script_dir, "leaderboard.json")

# Load leaderboard
def load_leaderboard():
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, "r") as file:
            return json.load(file)
    return []

# Save leaderboard
def save_leaderboard(leaderboard):
    with open(leaderboard_file, "w") as file:
        json.dump(leaderboard, file)

# Update leaderboard
def update_leaderboard(your_score):
    leaderboard = load_leaderboard()
    leaderboard.append(your_score)
    leaderboard = sorted(leaderboard, reverse=True)[:10]  # Keep top 10 scores
    save_leaderboard(leaderboard)

# Display leaderboard
def display_leaderboard():
    leaderboard = load_leaderboard()
    title_font = pygame.font.SysFont("Arial", 40)
    score_font = pygame.font.SysFont("Arial", 28)
    title_surf = title_font.render("Leaderboard", True, (255, 255, 255))
    window.blit(title_surf, (window_width / 2 - title_surf.get_width() / 2, window_height / 4))
    
    for i, score in enumerate(leaderboard):
        score_surf = score_font.render(f"{i + 1}. {score}", True, (255, 255, 255))
        window.blit(score_surf, (window_width / 2 - score_surf.get_width() / 2, window_height / 3 + i * 30))
    
    pygame.display.update()
    pygame.time.wait(3000)  # Display for 3 seconds

# Create pipes
def create_pipe():
    y_pos = random.randint(int(window_height * 0.3), int(window_height * 0.6))
    gap = random.randint(PIPE_GAP_MIN, PIPE_GAP_MAX)  # Varying pipe gap
    pipe_height = game_images["pipeimage"][0].get_height()
    return [
        {"x": window_width, "y": y_pos - pipe_height},
        {"x": window_width, "y": y_pos + gap},
    ]

# Game over function
def game_over(your_score):
    window.blit(pygame.transform.smoothscale(game_images["background"], window.get_size()), (0, 0))
    window.blit(game_images["game_over"], (window_width / 2 - game_images["game_over"].get_width() / 2, window_height / 2 - game_images["game_over"].get_height() / 2))
    show_score(your_score)
    
    # Update and display leaderboard
    update_leaderboard(your_score)
    display_leaderboard()
    
    # Display restart button
    restart_button_rect = game_images["restart_button"].get_rect(center=(window_width / 2, window_height / 1.5))
    window.blit(game_images["restart_button"], restart_button_rect.topleft)
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and restart_button_rect.collidepoint(event.pos):
                main()  # Restart the game
        pygame.time.wait(100)

# Update score function
def update_score(your_score, up_pipes, dragon_x):
    pipe_width = game_images["pipeimage"][0].get_width()
    for pipe in up_pipes:
        if not pipe.get("passed", False) and pipe["x"] + pipe_width < dragon_x:
            pipe["passed"] = True
            your_score += 1
            score_sound.play()
    return your_score

# Handle input
def handle_input():
    dragon_flapped = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            dragon_flapped = True
            flap_sound.play()
    return dragon_flapped

# Render game
def render_game(vertical, horizontal, up_pipes, down_pipes, your_score):
    window.blit(pygame.transform.smoothscale(game_images["background"], window.get_size()), (0, 0))
    for u_pipe, d_pipe in zip(up_pipes, down_pipes):
        window.blit(game_images["pipeimage"][0], (u_pipe["x"], u_pipe["y"]))
        window.blit(game_images["pipeimage"][1], (d_pipe["x"], d_pipe["y"]))
    
    sea_level_scaled = pygame.transform.scale(game_images["sea_level"], (window_width, game_images["sea_level"].get_height()))
    window.blit(sea_level_scaled, (0, window_height - sea_level_scaled.get_height()))
    
    window.blit(game_images["flappydragon"], (horizontal, vertical))
    show_score(your_score)
    pygame.display.update()

# Show score
def show_score(your_score):
    score_digits = [int(x) for x in list(str(your_score))]
    total_width = sum(game_images["scoreimages"][digit].get_width() for digit in score_digits)
    X_offset = (window_width - total_width) / 2
    for digit in score_digits:
        window.blit(game_images["scoreimages"][digit], (X_offset, window_height * 0.1))
        X_offset += game_images["scoreimages"][digit].get_width()

# Show welcome screen
def show_welcome_screen():
    title_font = pygame.font.SysFont("Arial", 40)
    start_font = pygame.font.SysFont("Arial", 28)
    title_surf = title_font.render("Flappy Dragon Game", True, (255, 255, 255))
    start_surf = start_font.render("Press SPACE to start", True, (255, 255, 255))
    while True:
        window.blit(pygame.transform.smoothscale(game_images["background"], window.get_size()), (0, 0))
        window.blit(title_surf, (window_width / 2 - title_surf.get_width() / 2, window_height / 4))
        window.blit(start_surf, (window_width / 2 - start_surf.get_width() / 2, window_height / 2))
        window.blit(game_images["message"], (window_width / 2 - game_images["message"].get_width() / 2, window_height / 1.5))  # Display message
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                return
        framepersecond_clock.tick(framepersecond)

# Check for collisions
def check_collision(vertical, horizontal, up_pipes, down_pipes, ground):
    for u_pipe, d_pipe in zip(up_pipes, down_pipes):
        pipe_height = game_images["pipeimage"][0].get_height()
        if (
            (vertical < u_pipe["y"] + pipe_height or vertical + game_images["flappydragon"].get_height() > d_pipe["y"]) and
            horizontal + game_images["flappydragon"].get_width() > u_pipe["x"] and
            horizontal < u_pipe["x"] + game_images["pipeimage"][0].get_width()
        ):
            collision_sound.play()
            return True

    if vertical + game_images["flappydragon"].get_height() >= ground:
        return True

    return False

# Main game loop
def main():
    show_welcome_screen()
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_height / 2)
    ground = window_height - game_images["sea_level"].get_height()
    first_pipe = create_pipe()
    second_pipe = create_pipe()

    down_pipes = [
        {"x": window_width + 200, "y": first_pipe[1]["y"]},
        {"x": window_width + 200 + (window_width / 2), "y": second_pipe[1]["y"]},
    ]

    up_pipes = [
        {"x": window_width + 200, "y": first_pipe[0]["y"]},
        {"x": window_width + 200 + (window_width / 2), "y": second_pipe[0]["y"]},
    ]

    dragon_velocity_y = -9
    dragon_max_vel_y = 10
    dragon_min_vel_y = -8
    dragon_acc_y = 1
    dragon_flap_velocity = -8
    dragon_flapped = False

    while True:
        dragon_flapped = handle_input()

        vertical += dragon_velocity_y
        dragon_velocity_y += dragon_acc_y if vertical < ground else 0
        vertical = min(vertical, ground)

        for u_pipe, d_pipe in zip(up_pipes, down_pipes):
            u_pipe["x"] += PIPE_VELOCITY_X
            d_pipe["x"] += PIPE_VELOCITY_X

        if up_pipes[0]["x"] < -game_images["pipeimage"][0].get_width():
            new_pipe = create_pipe()
            up_pipes.append(new_pipe[0])
            down_pipes.append(new_pipe[1])
            up_pipes.pop(0)
            down_pipes.pop(0)

        if dragon_flapped:
            if vertical > 0:
                dragon_velocity_y = dragon_flap_velocity
            dragon_flapped = False

        your_score = update_score(your_score, up_pipes, horizontal)

        render_game(vertical, horizontal, up_pipes, down_pipes, your_score)

        if check_collision(vertical, horizontal, up_pipes, down_pipes, ground):
            game_over(your_score)

        framepersecond_clock.tick(framepersecond)

# Main game loop for multiplayer
def main_multiplayer():
    show_welcome_screen()
    your_score1 = 0
    your_score2 = 0
    horizontal1 = int(window_width / 5)
    vertical1 = int(window_height / 2)
    horizontal2 = int(window_width / 5)
    vertical2 = int(window_height / 2)
    ground = window_height - game_images["sea_level"].get_height()
    first_pipe = create_pipe()
    second_pipe = create_pipe()

    down_pipes = [
        {"x": window_width + 200, "y": first_pipe[1]["y"]},
        {"x": window_width + 200 + (window_width / 2), "y": second_pipe[1]["y"]},
    ]

    up_pipes = [
        {"x": window_width + 200, "y": first_pipe[0]["y"]},
        {"x": window_width + 200 + (window_width / 2), "y": second_pipe[0]["y"]},
    ]

    dragon_velocity_y1 = -9
    dragon_velocity_y2 = -9
    dragon_max_vel_y = 10
    dragon_min_vel_y = -8
    dragon_acc_y = 1
    dragon_flap_velocity = -8
    dragon_flapped1 = False
    dragon_flapped2 = False

    while True:
        dragon_flapped1 = handle_input()
        dragon_flapped2 = handle_input()

        vertical1 += dragon_velocity_y1
        dragon_velocity_y1 += dragon_acc_y if vertical1 < ground else 0
        vertical1 = min(vertical1, ground)

        vertical2 += dragon_velocity_y2
        dragon_velocity_y2 += dragon_acc_y if vertical2 < ground else 0
        vertical2 = min(vertical2, ground)

        for u_pipe, d_pipe in zip(up_pipes, down_pipes):
            u_pipe["x"] += PIPE_VELOCITY_X
            d_pipe["x"] += PIPE_VELOCITY_X

        if up_pipes[0]["x"] < -game_images["pipeimage"][0].get_width():
            new_pipe = create_pipe()
            up_pipes.append(new_pipe[0])
            down_pipes.append(new_pipe[1])
            up_pipes.pop(0)
            down_pipes.pop(0)

        if dragon_flapped1:
            if vertical1 > 0:
                dragon_velocity_y1 = dragon_flap_velocity
            dragon_flapped1 = False

        if dragon_flapped2:
            if vertical2 > 0:
                dragon_velocity_y2 = dragon_flap_velocity
            dragon_flapped2 = False

        your_score1 = update_score(your_score1, up_pipes, horizontal1)
        your_score2 = update_score(your_score2, up_pipes, horizontal2)

        render_game(vertical1, horizontal1, up_pipes, down_pipes, your_score1)
        render_game(vertical2, horizontal2, up_pipes, down_pipes, your_score2)

        if check_collision(vertical1, horizontal1, up_pipes, down_pipes, ground) or check_collision(vertical2, horizontal2, up_pipes, down_pipes, ground):
            game_over(max(your_score1, your_score2))

        framepersecond_clock.tick(framepersecond)

if __name__ == "__main__":
    main()
