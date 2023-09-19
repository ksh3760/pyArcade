import pygame
import sys

pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("kaede banashi")

# 색상 설정
WHITE = (255, 255, 255)

# 캐릭터 설정
character = pygame.Rect(50, 50, 40, 60)
character_dx = 0
character_dy = 0
gravity = 0.981

# 바닥 설정
ground = pygame.Rect(0, screen_height - 40, screen_width, 40)

# 점프 관련 설정
jumping = False
jump_power = -15

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:
                jumping = True
                character_dy = jump_power

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_dx = -5  
    elif keys[pygame.K_RIGHT]:
        character_dx = 5
    elif keys[pygame.K_UP] and not jumping:
            jumping = True
            character_dy = jump_power
    else:
        character_dx = 0

    # 중력 적용
    character_dy += gravity

    # 캐릭터 이동
    character.x += character_dx
    character.y += character_dy

    # 바닥과 충돌 검사
    if character.colliderect(ground):
        character.y = screen_height - 40 - character.height  # 바닥 위에 정확히 머무르도록 조정
        character_dy = 0
        jumping = False

    # 화면 업데이트
    screen.fill(WHITE)
    pygame.draw.rect(screen, (0, 0, 255), character)
    pygame.draw.rect(screen, (0, 255, 0), ground)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
