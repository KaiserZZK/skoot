import pygame
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
PINK = (255, 105, 180)
WHITE = (255, 255, 255)
DOT_RADIUS = 10
STICK_LENGTH = 20

# Physics variables
speed = 2.0
steer_angle = 0
tilt = 0
friction_factor = 1.0

# Position and trajectory
x, y = 0, 0  # World coordinates
trajectory = []
angle = 0  # Camera orientation

# Pygame window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weeeeee")
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BLACK)
    
    # Event handling
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        speed += 0.1
    if keys[pygame.K_s]:
        speed = max(0.5, speed - 0.1)
    if keys[pygame.K_a]:
        steer_angle = max(-30, steer_angle - 2)
    if keys[pygame.K_d]:
        steer_angle = min(30, steer_angle + 2)
    if keys[pygame.K_LEFT]:
        tilt = max(-20, tilt - 1)
    if keys[pygame.K_RIGHT]:
        tilt = min(20, tilt + 1)
    
    # Movement restoration
    steer_angle *= 0.9 if not keys[pygame.K_a] and not keys[pygame.K_d] else 1
    tilt *= 0.9 if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] else 1
    
    # Compute physics
    r = max(1, abs(steer_angle))  # Turning radius
    friction_factor = max(0.5, 1.0 - abs(tilt) / 40)  # More tilt = less friction
    angular_velocity = (speed ** 2) / r * friction_factor
    
    # Compute movement
    angle += math.radians(steer_angle)
    x += tilt * 0.1  # Lateral movement due to tilt
    x += speed * math.sin(angle)
    y -= speed * math.cos(angle)
    
    trajectory.append((x, y))
    if len(trajectory) > 200:
        trajectory.pop(0)
    
    # Adjust camera to align with direction of movement
    camera_x, camera_y = x, y
    
    # Draw trajectory rotated to align with movement direction
    for point in trajectory:
        rel_x = point[0] - camera_x
        rel_y = point[1] - camera_y
        screen_x = int(rel_x * math.cos(-angle) - rel_y * math.sin(-angle) + WIDTH // 2)
        screen_y = int(rel_x * math.sin(-angle) + rel_y * math.cos(-angle) + HEIGHT // 2)
        pygame.draw.circle(screen, WHITE, (screen_x, screen_y), 2)
    
    # Draw dot
    dot_screen_x = WIDTH // 2
    dot_screen_y = HEIGHT // 2
    pygame.draw.circle(screen, PINK, (dot_screen_x, dot_screen_y), DOT_RADIUS)
    
    # Draw stick to indicate direction
    stick_x = dot_screen_x + STICK_LENGTH * math.sin(angle)
    stick_y = dot_screen_y - STICK_LENGTH * math.cos(angle)
    pygame.draw.line(screen, WHITE, (dot_screen_x, dot_screen_y), (stick_x, stick_y), 3)
    
    pygame.display.flip()
    clock.tick(60)
    
    # Exit condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
