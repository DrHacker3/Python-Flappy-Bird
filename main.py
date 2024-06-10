# Author: Sean Aitken
# Date Created: 06/06/2024
# Last Update: 10/06/2024
# V1.0
# Flappy Bird

# Imports
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 488
SCREEN_HEIGHT = 512
FPS = 60

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Remake')

# Clock object to control the frame rate
clock = pygame.time.Clock()

# Load game assets
background = pygame.image.load('.assets/background.png')
bird_downflap = pygame.image.load('.assets/bird-downflap.png')
bird_midflap = pygame.image.load('.assets/bird.png')
bird_upflap = pygame.image.load('.assets/bird-upflap.png')
bird_list = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird = bird_list[bird_index]
pipe = pygame.image.load('.assets/pipe.png')

# Load sounds
flap_sound = pygame.mixer.Sound('.assets/wing.wav')
hit_sound = pygame.mixer.Sound('.assets/hit.wav')
score_sound = pygame.mixer.Sound('.assets/point.wav')
die_sound = pygame.mixer.Sound('.assets/fortnite-death.mp3')
pygame.mixer.music.load('.assets/background-music.mp3')
pygame.mixer.music.play(-1)  # Play background music in a loop
pygame.mixer.Sound.set_volume(flap_sound, 0.5)
pygame.mixer.Sound.set_volume(hit_sound, 0.5)
pygame.mixer.Sound.set_volume(score_sound, 0.5)

# Font for score display
font = pygame.font.Font('.assets/04B_19.TTF', 20)

# Game variables
bird_x = 50
bird_y = 256
bird_velocity = 0
gravity = 0.25
flap_power = -4

pipe_width = pipe.get_width() - 50
pipe_height = pipe.get_height() - 50
pipe_gap = 100
pipe_speed = 2

# List to store pipes
pipes = []

# Score
score = 0
high_score = 0

# Game states
game_active = True
flap_animation_time = 5  # Time between bird animation frames

def draw_background():
    screen.blit(background, (0, 0))

def draw_bird(x, y):
    screen.blit(bird, (x, y))

def draw_pipes(pipes):
    for pipe_rect in pipes:
        if pipe_rect.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe, pipe_rect)
        else:
            screen.blit(pygame.transform.flip(pipe, False, True), pipe_rect)

def move_pipes(pipes):
    for pipe_rect in pipes:
        pipe_rect.centerx -= pipe_speed
    return [pipe for pipe in pipes if pipe.centerx > -pipe_width]

def check_collision(pipes):
    global game_active
    for pipe_rect in pipes:
        if bird_rect.colliderect(pipe_rect):
            hit_sound.play()
            die_sound.play()
            game_active = False
    if bird_rect.top <= -50 or bird_rect.bottom >= SCREEN_HEIGHT + 0:
        die_sound.play()
        game_active = False
        
def check_death():
    global game_active
    if game_active == False:
        game_over = font.render('Game Over', True, (255, 255, 255))
        game_over_rect = game_over.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(game_over, game_over_rect)
        pygame.display.update()
        game_active = False

def create_pipe():
    random_pipe_pos = random.choice([200, 300, 400])
    bottom_pipe = pipe.get_rect(midtop=(SCREEN_WIDTH + 100, random_pipe_pos))
    top_pipe = pipe.get_rect(midbottom=(SCREEN_WIDTH + 100, random_pipe_pos - pipe_gap))
    return bottom_pipe, top_pipe

def display_score(score):
    score_surface = font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, 50))
    screen.blit(score_surface, score_rect)

def update_bird_animation():
    global bird_index, bird
    bird_index = (bird_index + 1) % len(bird_list)
    bird = bird_list[bird_index]

# Main game loop
animation_counter = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_velocity = flap_power
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipes.clear()
                bird_x, bird_y = 50, 256
                bird_velocity = 0
                score = 0

    if game_active:
        bird_velocity += gravity
        bird_y += bird_velocity
        bird_rect = bird.get_rect(center=(bird_x, bird_y))
        
        pipes = move_pipes(pipes)
        if len(pipes) == 0 or pipes[-1].centerx < SCREEN_WIDTH - 150:
            pipes.extend(create_pipe())
        
        check_collision(pipes)
        
        # Increment score when passing pipes
        for pipe_rect in pipes:
            if pipe_rect.centerx == bird_x:
                score += 0.5
                if score % 1 == 0:
                    score_sound.play()
        
        draw_background()
        draw_pipes(pipes)
        draw_bird(bird_x, bird_y)
        display_score(score)
        check_death()
        
        # Bird animation
        animation_counter += 1
        if animation_counter >= flap_animation_time:
            update_bird_animation()
            animation_counter = 0
        
    else:
        draw_background()
        draw_pipes(pipes)
        draw_bird(bird_x, bird_y)
        display_score(score)
        check_death()
    
    pygame.display.update()
    clock.tick(FPS)
