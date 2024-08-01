import random
import sys
import os
import pygame
from pygame.locals import *

# Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
FPS = 60
PIPE_VELOCITY_X = -4
DRAGON_FLAP_VELOCITY = -8
DRAGON_FRAMES = 4

class GameState:
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    DIFFICULTY_SELECTION = 4

class Difficulty:
    EASY = 1
    MEDIUM = 2
    HARD = 3

class AssetManager:
    def __init__(self, script_dir):
        self.script_dir = script_dir
        self.sounds = {}
        self.images = {}
        self.dragon_frames = []

    def load_image(self, image_name):
        try:
            image_path = os.path.join(self.script_dir, "images", image_name)
            return pygame.image.load(image_path)
        except Exception as e:
            print(f"Unable to load image {image_path}: {e}")
            sys.exit(1)

    def load_sound(self, file_name):
        try:
            sound_path = os.path.join(self.script_dir, "sounds", file_name)
            return pygame.mixer.Sound(sound_path)
        except Exception as e:
            print(f"Unable to load sound {sound_path}: {e}")
            sys.exit(1)

    def load_assets(self):
        self.sounds = {
            "flap": self.load_sound("wing.wav"),
            "collision": self.load_sound("hit.wav"),
            "score": self.load_sound("point.wav"),
        }
        self.images = {
            "background": self.load_image("background.png"),
            "pipe": (self.load_image("pipe_up.png"), self.load_image("pipe_bottom.png")),
            "sea_level": self.load_image("base.png"),
            "score": [self.load_image(f"{i}.png") for i in range(10)],
        }
        self.dragon_frames = [
            self.load_image("dragon_spritesheet/frame-1.png"),
            self.load_image("dragon_spritesheet/frame-2.png"),
            self.load_image("dragon_spritesheet/frame-3.png"),
            self.load_image("dragon_spritesheet/frame-4.png")
        ]

class Player:
    def __init__(self, asset_manager):
        self.images = asset_manager.dragon_frames
        self.x = WINDOW_WIDTH // 5
        self.y = WINDOW_HEIGHT // 2
        self.velocity_y = -9
        self.flapped = False
        self.frame = 0
        self.frame_counter = 0
        self.animation_speed = 5

    def update(self):
        if self.flapped:
            self.velocity_y = DRAGON_FLAP_VELOCITY
            self.flapped = False
        else:
            self.velocity_y += 1
        self.y = min(self.y + self.velocity_y, WINDOW_HEIGHT - self.images[0].get_height())

    def draw(self, window):
        window.blit(self.images[self.frame], (self.x, self.y))
        self.frame_counter += 1
        if self.frame_counter % self.animation_speed == 0:
            self.frame = (self.frame + 1) % len(self.images)

class Pipe:
    def __init__(self, asset_manager, x):
        self.image_up = asset_manager.images["pipe"][0]
        self.image_down = asset_manager.images["pipe"][1]
        self.x = x
        self.y = random.randint(int(WINDOW_HEIGHT * 0.3), int(WINDOW_HEIGHT * 0.6))
        self.gap = 200

    def update(self):
        self.x += PIPE_VELOCITY_X

    def draw(self, window):
        window.blit(self.image_up, (self.x, self.y - self.image_up.get_height()))
        window.blit(self.image_down, (self.x, self.y + self.gap))

class FlappyDragonGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Dragon Game")
        self.frame_per_second_clock = pygame.time.Clock()
        self.asset_manager = AssetManager(self.script_dir)
        self.asset_manager.load_assets()
        self.player = Player(self.asset_manager)
        self.pipes = [Pipe(self.asset_manager, WINDOW_WIDTH + 200), Pipe(self.asset_manager, WINDOW_WIDTH + 200 + (WINDOW_WIDTH / 2))]
        self.game_state = GameState.MENU
        self.difficulty = Difficulty.EASY  # Default difficulty
        self.score = 0

    def reset_game(self):
        self.player = Player(self.asset_manager)
        self.pipes = [Pipe(self.asset_manager, WINDOW_WIDTH + 200), Pipe(self.asset_manager, WINDOW_WIDTH + 200 + (WINDOW_WIDTH / 2))]
        self.score = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                self.player.flapped = True
                self.asset_manager.sounds["flap"].play()

    def update_score(self):
        pipe_width = self.asset_manager.images["pipe"][0].get_width()
        for pipe in self.pipes:
            if not hasattr(pipe, "passed") and pipe.x + pipe_width < self.player.x:
                pipe.passed = True
                self.score += 1
                self.asset_manager.sounds["score"].play()

    def render_game(self):
        self.window.blit(pygame.transform.smoothscale(self.asset_manager.images["background"], self.window.get_size()), (0, 0))
        for pipe in self.pipes:
            pipe.draw(self.window)
        self.player.draw(self.window)
        self.show_score()
        pygame.display.update()

    def show_score(self):
        score_digits = [int(x) for x in str(self.score)]
        total_width = sum(self.asset_manager.images["score"][digit].get_width() for digit in score_digits)
        X_offset = (WINDOW_WIDTH - total_width) / 2
        for digit in score_digits:
            self.window.blit(self.asset_manager.images["score"][digit], (X_offset, WINDOW_HEIGHT * 0.1))
            X_offset += self.asset_manager.images["score"][digit].get_width()

    def show_main_menu(self):
        title_font = pygame.font.SysFont("Arial", 40)
        button_font = pygame.font.SysFont("Arial", 28)
        title_surf = title_font.render("Flappy Dragon Game", True, (255, 255, 255))
        start_surf = button_font.render("Start Game", True, (255, 255, 255))
        quit_surf = button_font.render("Quit Game", True, (255, 255, 255))
        difficulty_surf = button_font.render("Select Difficulty", True, (255, 255, 255))

        start_button = pygame.Rect(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 - 50, 200, 50)
        quit_button = pygame.Rect(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 70, 200, 50)
        difficulty_button = pygame.Rect(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 10, 200, 50)

        while self.game_state == GameState.MENU:
            self.window.blit(pygame.transform.smoothscale(self.asset_manager.images["background"], self.window.get_size()), (0, 0))
            self.window.blit(title_surf, (WINDOW_WIDTH / 2 - title_surf.get_width() / 2, WINDOW_HEIGHT / 4))

            pygame.draw.rect(self.window, (0, 0, 0), start_button)
            pygame.draw.rect(self.window, (0, 0, 0), quit_button)
            pygame.draw.rect(self.window, (0, 0, 0), difficulty_button)

            self.window.blit(start_surf, (start_button.x + (start_button.width - start_surf.get_width()) / 2, start_button.y + (start_button.height - start_surf.get_height()) / 2))
            self.window.blit(quit_surf, (quit_button.x + (quit_button.width - quit_surf.get_width()) / 2, quit_button.y + (quit_button.height - quit_surf.get_height()) / 2))
            self.window.blit(difficulty_surf, (difficulty_button.x + (difficulty_button.width - difficulty_surf.get_width()) / 2, difficulty_button.y + (difficulty_button.height - difficulty_surf.get_height()) / 2))

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if start_button.collidepoint(mouse_x, mouse_y):
                        self.game_state = GameState.PLAYING
                        self.reset_game()
                    elif quit_button.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        sys.exit()
                    elif difficulty_button.collidepoint(mouse_x, mouse_y):
                        self.game_state = GameState.DIFFICULTY_SELECTION

            pygame.display.update()
            self.frame_per_second_clock.tick(FPS)

    def show_difficulty_menu(self):
        button_font = pygame.font.SysFont("Arial", 28)
        easy_surf = button_font.render("Easy", True, (255, 255, 255))
        medium_surf = button_font.render("Medium", True, (255, 255, 255))
        hard_surf = button_font.render("Hard", True, (255, 255, 255))

        easy_button = pygame.Rect(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 - 50, 200, 50)
        medium_button = pygame.Rect(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 10, 200, 50)
        hard_button = pygame.Rect(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 70, 200, 50)

        while self.game_state == GameState.DIFFICULTY_SELECTION:
            self.window.blit(pygame.transform.smoothscale(self.asset_manager.images["background"], self.window.get_size()), (0, 0))
            
            pygame.draw.rect(self.window, (0, 0, 0), easy_button)
            pygame.draw.rect(self.window, (0, 0, 0), medium_button)
            pygame.draw.rect(self.window, (0, 0, 0), hard_button)
            
            self.window.blit(easy_surf, (easy_button.x + (easy_button.width - easy_surf.get_width()) / 2, easy_button.y + (easy_button.height - easy_surf.get_height()) / 2))
            self.window.blit(medium_surf, (medium_button.x + (medium_button.width - medium_surf.get_width()) / 2, medium_button.y + (medium_button.height - medium_surf.get_height()) / 2))
            self.window.blit(hard_surf, (hard_button.x + (hard_button.width - hard_surf.get_width()) / 2, hard_button.y + (hard_button.height - hard_surf.get_height()) / 2))

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if easy_button.collidepoint(mouse_x, mouse_y):
                        self.difficulty = Difficulty.EASY
                        self.game_state = GameState.MENU
                    elif medium_button.collidepoint(mouse_x, mouse_y):
                        self.difficulty = Difficulty.MEDIUM
                        self.game_state = GameState.MENU
                    elif hard_button.collidepoint(mouse_x, mouse_y):
                        self.difficulty = Difficulty.HARD
                        self.game_state = GameState.MENU

            pygame.display.update()
            self.frame_per_second_clock.tick(FPS)

    def show_game_over_screen(self):
        game_over_font = pygame.font.SysFont("Arial", 40)
        restart_font = pygame.font.SysFont("Arial", 28)
        game_over_surf = game_over_font.render("Game Over", True, (255, 255, 255))
        restart_surf = restart_font.render("Restart Game", True, (255, 255, 255))
        main_menu_surf = restart_font.render("Main Menu", True, (255, 255, 255))

        restart_button = pygame.Rect(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2, 200, 50)
        main_menu_button = pygame.Rect(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 60, 200, 50)

        while self.game_state == GameState.GAME_OVER:
            self.window.blit(pygame.transform.smoothscale(self.asset_manager.images["background"], self.window.get_size()), (0, 0))
            self.window.blit(game_over_surf, (WINDOW_WIDTH / 2 - game_over_surf.get_width() / 2, WINDOW_HEIGHT / 4))
            
            pygame.draw.rect(self.window, (0, 0, 0), restart_button)
            pygame.draw.rect(self.window, (0, 0, 0), main_menu_button)
            
            self.window.blit(restart_surf, (restart_button.x + (restart_button.width - restart_surf.get_width()) / 2, restart_button.y + (restart_button.height - restart_surf.get_height()) / 2))
            self.window.blit(main_menu_surf, (main_menu_button.x + (main_menu_button.width - main_menu_surf.get_width()) / 2, main_menu_button.y + (main_menu_button.height - main_menu_surf.get_height()) / 2))

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if restart_button.collidepoint(mouse_x, mouse_y):
                        self.game_state = GameState.PLAYING
                        self.reset_game()
                    elif main_menu_button.collidepoint(mouse_x, mouse_y):
                        self.game_state = GameState.MENU

            pygame.display.update()
            self.frame_per_second_clock.tick(FPS)

    def main_game_loop(self):
        self.reset_game()
        while True:
            if self.game_state == GameState.MENU:
                self.show_main_menu()
            elif self.game_state == GameState.DIFFICULTY_SELECTION:
                self.show_difficulty_menu()
            elif self.game_state == GameState.PLAYING:
                self.handle_input()
                self.update_game_state()
                self.render_game()
            elif self.game_state == GameState.GAME_OVER:
                self.show_game_over_screen()
            self.frame_per_second_clock.tick(FPS)

    def update_game_state(self):
        self.player.update()

        for pipe in self.pipes:
            pipe.update()

        if 0 < self.pipes[0].x < 5:
            self.pipes.append(Pipe(self.asset_manager, WINDOW_WIDTH + 200))

        if self.pipes[0].x < -self.pipes[0].image_up.get_width():
            self.pipes.pop(0)

        self.update_score()

        if self.is_collision():
            self.asset_manager.sounds["collision"].play()
            self.game_state = GameState.GAME_OVER

    def is_collision(self):
        if self.player.y > WINDOW_HEIGHT - 25 or self.player.y < 0:
            return True

        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.images[0].get_width(), self.player.images[0].get_height())

        for pipe in self.pipes:
            pipe_rect_up = pygame.Rect(pipe.x, pipe.y - pipe.image_up.get_height(), pipe.image_up.get_width(), pipe.image_up.get_height())
            pipe_rect_down = pygame.Rect(pipe.x, pipe.y + pipe.gap, pipe.image_down.get_width(), pipe.image_down.get_height())
            if player_rect.colliderect(pipe_rect_up) or player_rect.colliderect(pipe_rect_down):
                return True

        return False

if __name__ == "__main__":
    FlappyDragonGame().main_game_loop()
