import pygame
import os
from math import cos, sin, pi
import random

# Import constants
from config import (
    width, height, fps, x, y, 
    white, whitest, grey, black, deepblue, bluish_white, bg,
    BALL_CONFIGS, g, RING_MARGIN, bigr, centx, centy, SPAWN_RADIUS,
    RING_SPIN_SPEED, JERK_ANGLE_DEG, GAP_SEGMENT_DEG
)

# Import classes and helpers
# Import classes and helpers
from flag import Flags
from utils import draw_spinning_ring, angle_in_gap

# Game presets logic
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing balls")
clock = pygame.time.Clock()

background = pygame.image.load("img/start_img.png")

# initialize pygame mixer and load audio file
pygame.mixer.init()
# pygame.mixer.music.load('audio/golf_ball.wav') 

frames = 0
ring_angle = 0  # rotation of outer ring (degrees)
speed = 4       # Initial speed for balls

# Create 50 balls, spread on spawn circle at startup
num_balls = 50
for i in range(num_balls):
    # Iterate through configs cyclically if needed, or just dummy values since flags override
    name, color = BALL_CONFIGS[i % len(BALL_CONFIGS)]
    
    angle = 2 * pi * i / num_balls
    px = centx + SPAWN_RADIUS * cos(angle)
    py = centy - SPAWN_RADIUS * sin(angle)
    # Increased radius from 8 to 20 for visibility
    Flags(name, color, 20, 0, px, py, "golf_ball.wav")

def reset_round():
    """Respawn each ball at a different spot in the spawn circle (90° apart + jitter), random direction."""
    for i, ball in enumerate(Flags.flags):
        ball.escaped = False
        ball.track.clear()
        # Different location per ball: 4 base angles (0°, 90°, 180°, 270°) + random jitter
        base_angle = 2 * pi * i / len(Flags.flags) + random.uniform(-0.15, 0.15)
        r = random.uniform(SPAWN_RADIUS * 0.4, SPAWN_RADIUS)
        ball.posx = centx + r * cos(base_angle)
        ball.posy = centy - r * sin(base_angle)
        # Random direction (different for each ball)
        vel_angle = random.uniform(0, 2 * pi)
        ball.velx = speed * cos(vel_angle)
        ball.vely = speed * sin(vel_angle)
        ball.acc = 0

# Initial random velocity setup
for ball in Flags.flags:
    angle = random.uniform(0, 2 * pi)
    ball.velx = speed * cos(angle)
    ball.vely = speed * sin(angle)
    ball.acc = 0   # no gravity, straight lines between bounces

pause = False
start_sim = False 

# Initialize fonts once
try:
    title_font = pygame.font.Font(None, 72)
    hint_font = pygame.font.Font(None, 40)
    counter_font = pygame.font.Font(None, 36)
except Exception as e:
    print(f"Warning: Font initialization failed: {e}")
    title_font = None
    hint_font = None
    counter_font = None

# Intro loop
while start_sim is False:
    screen.fill(bg)
    # Centered content only
    if title_font and hint_font:
        try:
            title = title_font.render("Bouncing Balls", True, whitest)
            hint = hint_font.render("Press TAB to start", True, bluish_white)
            tr_title = title.get_rect(center=(width // 2, height // 2 - 35))
            tr_hint = hint.get_rect(center=(width // 2, height // 2 + 25))

            screen.blit(title, tr_title)
            screen.blit(hint, tr_hint)
        except Exception:
            pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                start_sim = True

    pygame.display.update()
    clock.tick(fps)

import traceback

# Main game loop
try:
    while True:
        screen.fill(bg)
        # Top 3 score card at top
        if counter_font:
            try:
                top3 = sorted(Flags.flags, key=lambda b: b.wins, reverse=True)[:3]
                parts = [f"{b.name}: {b.wins}" for b in top3]
                counter_text = counter_font.render("  |  ".join(parts), True, whitest)
                tr_counter = counter_text.get_rect(midtop=(width // 2, 12))
                screen.blit(counter_text, tr_counter)
            except Exception as e:
                print(f"Error drawing score: {e}")

        draw_spinning_ring(screen, bigr, centx, centy, ring_angle, whitest, grey, num_segments=24, thickness=2)
        if not pause:
            ring_angle = (ring_angle + RING_SPIN_SPEED) % 360

        active_balls = [b for b in Flags.flags if not b.escaped]
        if len(active_balls) <= 1:
            if len(active_balls) == 1:
                active_balls[0].wins += 1
            reset_round()
            active_balls = list(Flags.flags)
        
        for ball in active_balls:
            if len(ball.track) > 2 and Flags.trail:
                pygame.draw.aalines(screen, ball.color, False, ball.track, 2)
        for ball in active_balls:
            ball.draw(screen)
            if not pause:
                ball.collision_handling(ring_angle)
                ball.update(frames)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                if event.key == pygame.K_t:
                    Flags.trail = not Flags.trail
        
        pygame.display.update()
        clock.tick(fps)
        frames += 1
except Exception:
    traceback.print_exc()
    pygame.quit()