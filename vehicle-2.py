import random
import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Braitenberg Vehicle 2")

pygame.font.init()
font = pygame.font.SysFont("Arial", 20)

clock = pygame.time.Clock()
fps = 120

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Circle:
    def __init__(self, position, radius=50, color=RED):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)


class Vehicle:
    def __init__(self, position, direction, radius=30, color=RED):
        self.position = pygame.math.Vector2(position)
        self.direction = direction
        self.radius = radius
        self.color = color

        self.speed_scaling = 50
        self.rotation_scaling = 5
        self.sensor_spacing = 50

        self.sensor_radius = 10
        self.sensor_offset = self.radius + self.sensor_radius
        self.sensor_color = GREEN

        self.left_sensor_position = self.position
        self.right_sensor_position = self.position

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
        pygame.draw.circle(surface, self.sensor_color, self.left_sensor_position, self.sensor_radius)
        pygame.draw.circle(surface, self.sensor_color, self.right_sensor_position, self.sensor_radius)

    def move(self, sun_position):
        forward = pygame.math.Vector2(0, -1).rotate(self.direction)
        right = forward.rotate(-90)

        # Update sensor positions
        self.left_sensor_position = self.position + forward * self.sensor_offset - right * self.sensor_spacing / 2
        self.right_sensor_position = self.position + forward * self.sensor_offset + right * self.sensor_spacing / 2

        # Simulate noisy sensors
        left_distance = self.left_sensor_position.distance_to(sun_position) + random.uniform(-5, 5)
        right_distance = self.right_sensor_position.distance_to(sun_position) + random.uniform(-5, 5)

        left_distance = max(left_distance, 0.01)
        right_distance = max(right_distance, 0.01)

        # Calculate speeds
        # this is fear
        left_speed = self.speed_scaling * (1 / left_distance)
        right_speed = self.speed_scaling * (1 / right_distance)

        # #this is aggression
        # left_speed = self.speed_scaling * (1 / right_distance)
        # right_speed = self.speed_scaling * (1 / left_distance)

        speed = (left_speed + right_speed) / 2

        # Making the vehicle wiggle by adding rotation to the direction
        rotation_noise = random.uniform(-0.5, 0.5)
        rotation = (right_speed - left_speed) * self.rotation_scaling + rotation_noise
        self.direction += rotation

        # Sometimes it goes in random direction like an ant
        if random.random() < 0.01:  # 0.01 indicates that there is 1% chance per frame
            self.direction += random.uniform(-30, 30)

        direction = pygame.math.Vector2(0, -1).rotate(self.direction)
        self.position += direction * speed
        self.position.x %= WIDTH
        self.position.y %= HEIGHT

        avg_distance = (left_distance + right_distance) / 2
        debug_text = f"Distance: {avg_distance:.2f} | Speed: {speed:.2f}"
        text_surface = font.render(debug_text, True, WHITE)
        screen.blit(text_surface, (10, 10))


sun = Circle((WIDTH // 2, HEIGHT // 2), radius=30, color=YELLOW)
vehicle = Vehicle((300, 500), 55)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    sun.draw(screen)
    vehicle.move(sun.position)
    vehicle.draw(screen)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
