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
FIELD_OF_VIEW = 64

# Define RoadPiece class
class RoadPiece:
    def __init__(self, count, turn):
        self.count: int = count  # Length of the segment
        self.turn: float = turn  # Tilt/turn of the segment

# Define the road data
road = [
    RoadPiece(10, 0),
    RoadPiece(6, -1),
    RoadPiece(8, 0),
    RoadPiece(4, 1.5),
    RoadPiece(10, 0.2),
    RoadPiece(4, 0),
    RoadPiece(5, -1),
]

# Pygame window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Road Renderer with Projection")
clock = pygame.time.Clock()

CAMERA_ROAD_PIECE_INDEX, CAMERA_DISTANCE_TRAVELED = 0, 1

# Projection function
def project(x, y, z):
    if z == 0:
        z = 0.1
    scale = FIELD_OF_VIEW / z
    screen_x = x * scale + WIDTH // 2
    screen_y = y * scale + HEIGHT // 2
    return screen_x, screen_y, scale

# Advance along road
def advance(road_piece_index, distance_traveled):
    distance_traveled += 1
    if distance_traveled > road[road_piece_index].count:
        distance_traveled = 1
        road_piece_index = (road_piece_index + 1) % len(road)
    return road_piece_index, distance_traveled

# Update function
def update():
    global CAMERA_ROAD_PIECE_INDEX, CAMERA_DISTANCE_TRAVELED
    CAMERA_ROAD_PIECE_INDEX, CAMERA_DISTANCE_TRAVELED = advance(CAMERA_ROAD_PIECE_INDEX, CAMERA_DISTANCE_TRAVELED)

# Draw function
def draw():
    screen.fill(BLACK)
    x, y, z = 0, 1, 1
    xd, yd, zd = 0, 0, 1
    road_piece_index, distance_traveled = CAMERA_ROAD_PIECE_INDEX, CAMERA_DISTANCE_TRAVELED
    
    for _ in range(30):
        px, py, scale = project(x, y, z)
        road_width = 3 * scale
        pygame.draw.line(screen, PINK, (px - road_width, py), (px + road_width, py), 2)
        x += xd
        y += yd
        z += zd
        xd += road[road_piece_index].turn
        road_piece_index, distance_traveled = advance(road_piece_index, distance_traveled)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    update()
    draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
