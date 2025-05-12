import pygame

pygame.init()

width, height = 1200, 600
my_screen = pygame.display.set_mode(size=(width, height))
pygame.display.set_caption("Braitenberg Vehicle")

clock = pygame.time.Clock()
fps = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont('arial', 20)

class Circle:
    def __init__(self, position, radius=50, color=RED):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)

class Vehicle:
    def __init__(self, position, direction, radius=50, color=RED):
        self.position = pygame.math.Vector2(position)
        self.direction = direction  # angle in degrees
        self.radius = radius
        self.color = color

        self.sensor_radius = 15
        self.sensor_offset = self.radius + self.sensor_radius
        self.sensor_position = self.get_sensor_position()
        self.sensor_color = GREEN

        self.speed_scaling = 0.05
        self.max_speed = 5
        self.current_speed = 0
        self.min_speed = float('inf')
        self.max_speed_achieved = 0

    def get_sensor_position(self):
        return self.position + pygame.math.Vector2(0, -self.sensor_offset).rotate(self.direction)

    def calculate_distance_to_sun(self, sun_position):
        return self.sensor_position.distance_to(sun_position)

    def move(self, sun_position):
        direction_vector = pygame.math.Vector2(0, -1).rotate(self.direction)
        distance = self.calculate_distance_to_sun(sun_position)

        if distance > 0:
            self.current_speed = min(self.max_speed, self.speed_scaling * (1000 / distance))
        else:
            self.current_speed = 0

        # Update min and max speed
        if self.current_speed < self.min_speed:
            self.min_speed = self.current_speed
        if self.current_speed > self.max_speed_achieved:
            self.max_speed_achieved = self.current_speed

        self.position += direction_vector * self.current_speed
        self.sensor_position = self.get_sensor_position()

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        pygame.draw.circle(surface, self.sensor_color, (int(self.sensor_position.x), int(self.sensor_position.y)), self.sensor_radius)

        distance = self.calculate_distance_to_sun(sun.position)

        # Display info
        surface.blit(font.render(f"Distance to sun: {int(distance)}", True, BLACK), (10, 10))
        surface.blit(font.render(f"Current speed: {self.current_speed:.2f}", True, BLACK), (10, 35))
        surface.blit(font.render(f"Min speed: {self.min_speed:.2f}", True, BLACK), (10, 60))
        surface.blit(font.render(f"Max speed: {self.max_speed_achieved:.2f}", True, BLACK), (10, 85))

# Main loop
sun = Circle((600, 300), radius=30, color=YELLOW)
vehicle = Vehicle((300, 200), 90)

s_running = True
while s_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s_running = False

    my_screen.fill(WHITE)
    sun.draw(my_screen)
    vehicle.move(sun.position)
    vehicle.draw(my_screen)
    pygame.display.flip()

    clock.tick(fps)

pygame.quit()
