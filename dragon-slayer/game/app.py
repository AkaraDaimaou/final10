import random
import sys
import os
import pygame
from pygame.locals import *

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 499
FPS = 60
PIPE_VELOCITY_X = -4
DRAGON_FLAP_VELOCITY = -8

class GameState:
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class Difficulty:
    EASY = 1
    MEDIUM = 2
    HARD = 3

class FlappyDragonGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Dragon Game")
        self.frame_per_second_clock = pygame.time.Clock()
        self.load_assets()
        self.game_state = GameState.MENU
        self.difficulty = Difficulty.EASY  # Default difficulty

    def load_assets(self):
        self.sounds = {
            "flap": self.load_sound("wing.wav"),
            "collision": self.load_sound("hit.wav"),
            "score": self.load_sound("point.wav"),
        }
        self.images = {
            "background": self.load_image("background.png"),
            "dragon": self.load_image("bluebird.png"),
            "pipe": (self.load_image("pipe_up.png"), self.load_image("pipe_bottom.png")),
            "sea_level": self.load_image("base.png"),
            "score": [self.load_image(f"{i}.png") for i in range(10)],
        }

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

    def reset_game(self):
        self.vertical = WINDOW_HEIGHT // 2
        self.horizontal = WINDOW_WIDTH // 5
        self.ground = WINDOW_HEIGHT - self.images["sea_level"].get_height()
        self.score = 0
        self.pipes = [self.create_pipe(), self.create_pipe()]
        self.down_pipes = [
            {"x": WINDOW_WIDTH + 200, "y": self.pipes[0][1]["y"]},
            {"x": WINDOW_WIDTH + 200 + (WINDOW_WIDTH / 2), "y": self.pipes[1][1]["y"]},
        ]
        self.up_pipes = [
            {"x": WINDOW_WIDTH + 200, "y": self.pipes[0][0]["y"]},
            {"x": WINDOW_WIDTH + 200 + (WINDOW_WIDTH / 2), "y": self.pipes[1][0]["y"]},
        ]
        self.dragon_velocity_y = -9
        self.dragon_flapped = False
        
        if self.difficulty == Difficulty.EASY:
            global PIPE_VELOCITY_X
            PIPE_VELOCITY_X = -4
        elif self.difficulty == Difficulty.MEDIUM:
            PIPE_VELOCITY_X = -6
        elif self.difficulty == Difficulty.HARD:
            PIPE_VELOCITY_X = -8

    def create_pipe(self):
        y_pos = random.randint(int(WINDOW_HEIGHT * 0.3), int(WINDOW_HEIGHT * 0.6))
        gap = 200
        pipe_height = self.images["pipe"][0].get_height()
        return [
            {"x": WINDOW_WIDTH, "y": y_pos - pipe_height},
            {"x": WINDOW_WIDTH, "y": y_pos + gap},
        ]

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                self.dragon_flapped = True
                self.sounds["flap"].play()

    def update_score(self):
        pipe_width = self.images["pipe"][0].get_width()
        for pipe in self.up_pipes:
            if not pipe.get("passed", False) and pipe["x"] + pipe_width < self.horizontal:
                pipe["passed"] = True
                self.score += 1
                self.sounds["score"].play()

    def render_game(self):
        self.window.blit(pygame.transform.smoothscale(self.images["background"], self.window.get_size()), (0, 0))
        for u_pipe, d_pipe in zip(self.up_pipes, self.down_pipes):
            self.window.blit(self.images["pipe"][0], (u_pipe["x"], u_pipe["y"]))
            self.window.blit(self.images["pipe"][1], (d_pipe["x"], d_pipe["y"]))
        sea_level_scaled = pygame.transform.scale(self.images["sea_level"], (WINDOW_WIDTH, self.images["sea_level"].get_height()))
        self.window.blit(sea_level_scaled, (0, WINDOW_HEIGHT - sea_level_scaled.get_height()))
        self.window.blit(self.images["dragon"], (self.horizontal, self.vertical))
        self.show_score()
        pygame.display.update()

    def show_score(self):
        score_digits = [int(x) for x in str(self.score)]
        total_width = sum(self.images["score"][digit].get_width() for digit in score_digits)
        X_offset = (WINDOW_WIDTH - total_width) / 2
        for digit in score_digits:
            self.window.blit(self.images["score"][digit], (X_offset, WINDOW_HEIGHT * 0.1))
            X_offset += self.images["score"][digit].get_width()

    def show_welcome_screen(self):
        title_font = pygame.font.SysFont("Arial", 40)
        start_font = pygame.font.SysFont("Arial", 28)
        title_surf = title_font.render("Flappy Dragon Game", True, (255, 255, 255))
        start_surf = start_font.render("Press SPACE to start", True, (255, 255, 255))
        
        while self.game_state == GameState.MENU:
            self.window.blit(pygame.transform.smoothscale(self.images["background"], self.window.get_size()), (0, 0))
            self.window.blit(title_surf, (WINDOW_WIDTH / 2 - title_surf.get_width() / 2, WINDOW_HEIGHT / 4))
            self.window.blit(start_surf, (WINDOW_WIDTH / 2 - start_surf.get_width() / 2, WINDOW_HEIGHT / 2))
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    self.game_state = GameState.PLAYING

            self.frame_per_second_clock.tick(FPS)

    def game_over_screen(self):
        title_font = pygame.font.SysFont("Arial", 40)
        game_over_surf = title_font.render(f"Game Over! Your Score: {self.score}", True, (255, 255, 255))
        restart_surf = pygame.font.SysFont("Arial", 28).render("Press SPACE to restart or ESC to exit", True, (255, 255, 255))
        
        while self.game_state == GameState.GAME_OVER:
            self.window.blit(pygame.transform.smoothscale(self.images["background"], self.window.get_size()), (0, 0))
            self.window.blit(game_over_surf, (WINDOW_WIDTH / 2 - game_over_surf.get_width() / 2, WINDOW_HEIGHT / 4))
            self.window.blit(restart_surf, (WINDOW_WIDTH / 2 - restart_surf.get_width() / 2, WINDOW_HEIGHT / 2))
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.reset_game()
                    self.game_state = GameState.PLAYING

            self.frame_per_second_clock.tick(FPS)

    def show_difficulty_menu(self):
        title_font = pygame.font.SysFont("Arial", 40)
        diff_font = pygame.font.SysFont("Arial", 28)
        title_surf = title_font.render("Select Difficulty", True, (255, 255, 255))
        easy_surf = diff_font.render("1. Easy", True, (255, 255, 255))
        medium_surf = diff_font.render("2. Medium", True, (255, 255, 255))
        hard_surf = diff_font.render("3. Hard", True, (255, 255, 255))

        while True:
            self.window.blit(pygame.transform.smoothscale(self.images["background"], self.window.get_size()), (0, 0))
            self.window.blit(title_surf, (WINDOW_WIDTH / 2 - title_surf.get_width() / 2, WINDOW_HEIGHT / 4))
            self.window.blit(easy_surf, (WINDOW_WIDTH / 2 - easy_surf.get_width() / 2, WINDOW_HEIGHT / 3))
            self.window.blit(medium_surf, (WINDOW_WIDTH / 2 - medium_surf.get_width() / 2, WINDOW_HEIGHT / 2.5))
            self.window.blit(hard_surf, (WINDOW_WIDTH / 2 - hard_surf.get_width() / 2, WINDOW_HEIGHT / 2))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        self.difficulty = Difficulty.EASY
                        return
                    elif event.key == K_2:
                        self.difficulty = Difficulty.MEDIUM
                        return
                    elif event.key == K_3:
                        self.difficulty = Difficulty.HARD
                        return

    def main(self):
        self.show_difficulty_menu()  # Show difficulty menu before starting the game
        self.reset_game()
        while True:
            if self.game_state == GameState.MENU:
                self.show_welcome_screen()
            elif self.game_state == GameState.PLAYING:
                self.handle_input()
                self.vertical += self.dragon_velocity_y
                self.dragon_velocity_y += 1 if self.vertical < self.ground else 0
                self.vertical = min(self.vertical, self.ground)
                
                for u_pipe, d_pipe in zip(self.up_pipes, self.down_pipes):
                    u_pipe["x"] += PIPE_VELOCITY_X
                    d_pipe["x"] += PIPE_VELOCITY_X

                if self.up_pipes[0]["x"] < -self.images["pipe"][0].get_width():
                    new_pipe = self.create_pipe()
                    self.up_pipes.append(new_pipe[0])
                    self.down_pipes.append(new_pipe[1])
                    self.up_pipes.pop(0)
                    self.down_pipes.pop(0)

                if self.dragon_flapped:
                    if self.vertical > 0:
                        self.dragon_velocity_y = DRAGON_FLAP_VELOCITY
                    self.dragon_flapped = False

                self.update_score()
                self.render_game()

                for u_pipe, d_pipe in zip(self.up_pipes, self.down_pipes):
                    pipe_height = self.images["pipe"][0].get_height()
                    if (
                        (self.vertical < u_pipe["y"] + pipe_height
                         or self.vertical + self.images["dragon"].get_height() > d_pipe["y"])
                        and self.horizontal + self.images["dragon"].get_width() > u_pipe["x"]
                        and self.horizontal < u_pipe["x"] + self.images["pipe"][0].get_width()
                        and self.horizontal + self.images["dragon"].get_width() > d_pipe["x"]
                        and self.horizontal < d_pipe["x"] + self.images["pipe"][0].get_width()
                        or self.vertical + self.images["dragon"].get_height() > self.ground
                    ):
                        self.sounds["collision"].play()
                        self.game_state = GameState.GAME_OVER

            elif self.game_state == GameState.GAME_OVER:
                self.game_over_screen()

            self.frame_per_second_clock.tick(FPS)

if __name__ == "__main__":
    game = FlappyDragonGame()
    game.main()
