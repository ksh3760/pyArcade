import pygame
import sys

pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Obstacle Avoidance Game")

# 폰트 설정
font = pygame.font.Font(None, 36)

# 컬러 설정
white = (255, 255, 255)

# 캐릭터 설정
character = pygame.image.load("character.png")
character_rect = character.get_rect()
character_rect.center = (screen_width // 2, screen_height - 50)

# 장애물 설정
obstacle = pygame.image.load("obstacle.png")
obstacle_rect = obstacle.get_rect()
obstacle_rect.center = (screen_width // 2, 50)

# 게임 오버 관련 설정
game_over = False
game_over_text = font.render("Game Over", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
ok_text = font.render("OK", True, (0, 0, 0))
ok_rect = ok_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        character_rect.x += 5

    # 충돌 검사
    if character_rect.colliderect(obstacle_rect):
        game_over = True

    screen.fill(white)
    
    # 캐릭터와 장애물 그리기
    screen.blit(character, character_rect)
    screen.blit(obstacle, obstacle_rect)
    
    if game_over:
        screen.blit(game_over_text, game_over_rect)
        pygame.draw.rect(screen, white, ok_rect)
        screen.blit(ok_text, ok_rect)

    pygame.display.flip()

    clock.tick(60)

    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

pygame.quit()
sys.exit()
