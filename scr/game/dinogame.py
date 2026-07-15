import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)

ground_y = 320

dino = pygame.Rect(80, ground_y - 50, 40, 50)
velocity_y = 0
gravity = 1
jump_power = -18
on_ground = True

obstacles = []
obstacle_timer = 0
speed = 8

score = 0
game_over = False

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_SPACE and on_ground:
                    velocity_y = jump_power
                    on_ground = False
            else:
                if event.key == pygame.K_r:
                    dino.y = ground_y - 50
                    velocity_y = 0
                    obstacles.clear()
                    score = 0
                    speed = 8
                    game_over = False

    if not game_over:
        velocity_y += gravity
        dino.y += velocity_y

        if dino.bottom >= ground_y:
            dino.bottom = ground_y
            velocity_y = 0
            on_ground = True

        obstacle_timer += 1
        if obstacle_timer > 60:
            h = random.randint(40, 70)
            obstacles.append(pygame.Rect(WIDTH, ground_y - h, 20, h))
            obstacle_timer = 0

        for obs in obstacles[:]:
            obs.x -= speed

            if obs.right < 0:
                obstacles.remove(obs)
                score += 1

            if dino.colliderect(obs):
                game_over = True

        if score > 0 and score % 10 == 0:
            speed = min(20, 8 + score // 10)

    screen.fill(WHITE)

    pygame.draw.line(screen, BLACK, (0, ground_y), (WIDTH, ground_y), 2)

    pygame.draw.rect(screen, GREEN, dino)

    for obs in obstacles:
        pygame.draw.rect(screen, BLACK, obs)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if game_over:
        text = font.render("GAME OVER - Press R to Restart", True, (200, 0, 0))
        screen.blit(text, (120, 150))

    pygame.display.flip()

pygame.quit()