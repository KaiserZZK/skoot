import pygame
import math
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
PINK = (255, 105, 180)
WHITE = (255, 255, 255)
DOT_RADIUS = 10
STICK_LENGTH = 20
SUB_DISPLAY_SIZE = (80, 100)  # Sub-display for tilt indicator

# Physics variables
speed = 2.0
steer_angle = 0
tilt = 0
friction_factor = 1.0

# Position and trajectory
x, y = 0, 0  # World coordinates
trajectory = []

# Pygame window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Steering and Tilting Dot")
clock = pygame.time.Clock()

# Sub-display setup
sub_display = pygame.Surface(SUB_DISPLAY_SIZE)
sub_rect = pygame.Rect(WIDTH - SUB_DISPLAY_SIZE[0] - 10, HEIGHT - SUB_DISPLAY_SIZE[1] - 10, *SUB_DISPLAY_SIZE)

running = True
straight_count = random.randint(1, 20)

while running:
    screen.fill(BLACK)
    
    # Event handling
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        speed += 0.1
    if keys[pygame.K_s]:
        speed = max(0.5, speed - 0.1)
    if keys[pygame.K_a]:
        steer_angle = max(-90, steer_angle - 2)
    if keys[pygame.K_d]:
        steer_angle = min(90, steer_angle + 2)
    if keys[pygame.K_LEFT]:
        tilt = max(-20, tilt - 1)
    if keys[pygame.K_RIGHT]:
        tilt = min(20, tilt + 1)
    
    if not keys[pygame.K_a] and not keys[pygame.K_d]:
        steer_angle *= 0.9  # Gradual return to center
    if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        tilt *= 0.9  # Gradual return to neutral

    # Compute physics
    r = max(1, abs(steer_angle))  # Turning radius
    friction_factor = max(0.5, 1.0 - abs(tilt) / 40)  # More tilt = less friction
    angular_velocity = (speed ** 2) / r * friction_factor
    
    # Compute movement
    angle_radians = math.radians(steer_angle)
    x += speed * math.sin(angle_radians)
    y -= speed * math.cos(angle_radians)
    x += tilt * 0.1  # Lateral movement due to tilt
    
    trajectory.append((x, y))
    if len(trajectory) > 200:
        trajectory.pop(0)
    
    # Adjust camera so the dot remains centered
    camera_x = int(x - WIDTH // 2)
    camera_y = int(y - HEIGHT // 2)
    
    # Draw trajectory
    for point in trajectory:
        screen_x = int(point[0] - camera_x)
        screen_y = int(point[1] - camera_y)
        pygame.draw.circle(screen, WHITE, (screen_x, screen_y), 2)
    
    # Draw dot
    dot_screen_x = WIDTH // 2
    dot_screen_y = HEIGHT // 2
    pygame.draw.circle(screen, PINK, (dot_screen_x, dot_screen_y), DOT_RADIUS)
    
    # Draw stick to indicate direction
    stick_x = dot_screen_x + STICK_LENGTH * math.sin(angle_radians)
    stick_y = dot_screen_y - STICK_LENGTH * math.cos(angle_radians)
    pygame.draw.line(screen, WHITE, (dot_screen_x, dot_screen_y), (stick_x, stick_y), 3)
    
    # Draw sub-display for tilt indicator
    sub_display.fill((50, 50, 50))  # Dark gray background
    pygame.draw.rect(screen, WHITE, sub_rect, 2)
    center_x = SUB_DISPLAY_SIZE[0] // 2
    center_y = SUB_DISPLAY_SIZE[1] // 2
    tilt_stick_x = center_x
    tilt_stick_y = center_y + int(tilt * (SUB_DISPLAY_SIZE[1] // 40))
    pygame.draw.line(sub_display, PINK, (center_x, center_y - 20), (tilt_stick_x, tilt_stick_y + 20), 4)
    screen.blit(sub_display, sub_rect.topleft)
    
    pygame.display.flip()
    clock.tick(60)
    
    # Exit condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
