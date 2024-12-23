import pygame
import random
import sys

# Initialize PyGame
pygame.init()

# Screen dimensionss
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Scavenger")

# Load assets
spaceship_img = pygame.image.load('spaceship.png')
asteroid_img = pygame.image.load('asteroid.png')
energy_crystal_img = pygame.image.load('energy_crystal.png')
background_music = 'background_music.wav'
clash_sound = pygame.mixer.Sound('clash_sound.wav')

# Scale images
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
energy_crystal_img = pygame.transform.scale(energy_crystal_img, (30, 30))

# Load and play background music
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Spaceship class
class Spaceship:
    def __init__(self):
        self.image = spaceship_img
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - 50:
            self.x += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Asteroid class
class Asteroid:
    def __init__(self):
        self.image = asteroid_img
        self.x = random.randint(0, SCREEN_WIDTH - 50)
        self.y = random.randint(-100, -40)
        self.speed = random.randint(3, 6)

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = random.randint(-100, -40)
            self.x = random.randint(0, SCREEN_WIDTH - 50)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Energy Crystal class
class EnergyCrystal:
    def __init__(self):
        self.image = energy_crystal_img
        self.x = random.randint(0, SCREEN_WIDTH - 30)
        self.y = random.randint(-100, -40)
        self.speed = 4

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = random.randint(-100, -40)
            self.x = random.randint(0, SCREEN_WIDTH - 30)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Check collision
def check_collision(obj1, obj2):
    return pygame.Rect(obj1.x, obj1.y, 50, 50).colliderect(pygame.Rect(obj2.x, obj2.y, 50, 50))

# Main function
def main():
    spaceship = Spaceship()
    asteroids = [Asteroid() for _ in range(5)]
    crystals = [EnergyCrystal() for _ in range(3)]

    score = 0
    running = True
    game_over = False

    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # Move and draw spaceship
            spaceship.move(keys)
            spaceship.draw()

            # Move and draw asteroids
            for asteroid in asteroids:
                asteroid.move()
                asteroid.draw()
                if check_collision(spaceship, asteroid):
                    pygame.mixer.Sound.play(clash_sound)
                    game_over = True

            # Move and draw energy crystals
            for crystal in crystals:
                crystal.move()
                crystal.draw()
                if check_collision(spaceship, crystal):
                    score += 10
                    crystals.remove(crystal)
                    crystals.append(EnergyCrystal())

        # Display score
        font = pygame.font.SysFont(None, 36)
        if game_over:
            game_over_text = font.render("Game Over! Press Enter to Retry", True, WHITE)

            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            if keys[pygame.K_RETURN]:
                main()
        else:
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()