import pygame
import random

pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("테스트 게임")

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 오브젝트 상수 설정
OBJ_SPEED = 10

# 캐릭터 설정
character = pygame.image.load("./character.png")
character = pygame.transform.scale(character, (50, 50)) # 캐릭터 크기
character_rect = character.get_rect() # 캐릭터 이미지의 rect 정보 저장
character_rect.centerx = round(SCREEN_WIDTH / 2)
character_rect.centery = round(SCREEN_HEIGHT / 2)

character_width = 50
character_height = 50
character_x = SCREEN_WIDTH / 2 
character_y = SCREEN_HEIGHT / 2

# 장애물 설정
obstacle = pygame.image.load("./obstacle.png")
obstacle_width = 50
obstacle_height = 50
obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
obstacle_y = 0
obstacle_speed = 5

# 포인트 오브젝트
carrot = pygame.image.load("./carrot.png")
carrot_width = 50
carrot_height = 50
carrot_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
carrot_y = random.randint(0, SCREEN_HEIGHT - obstacle_height)

# 게임 변수 정의
font = pygame.font.Font(None, 36) # 폰트 설정
score = 0
start_time = pygame.time.get_ticks() // 100

# 장애물 충돌 시
game_over = False
game_over_text = font.render("Game Over", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
ok_text = font.render("OK", True, (0, 0, 0))
ok_rect = ok_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))


# 게임 루프
running = True
clock = pygame.time.Clock() # fps clock 생성

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 게임 오버 시
    if not game_over:
        current_time = pygame.time.get_ticks() // 100 - start_time
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_x -= OBJ_SPEED
            if character_x < 0:  # 화면 왼쪽 벽을 벗어나지 않도록 제한
                character_x = 0
        if keys[pygame.K_RIGHT]:
            character_x += OBJ_SPEED
            if character_x > SCREEN_WIDTH - character_width:  # 화면 오른쪽 벽을 벗어나지 않도록 제한
                character_x = SCREEN_WIDTH - character_width
        if keys[pygame.K_UP]:
            character_y -= OBJ_SPEED
            if character_y < 0:  # 화면 위쪽 벽을 벗어나지 않도록 제한
                character_y = 0
        if keys[pygame.K_DOWN]:
            character_y += OBJ_SPEED
            if character_y > SCREEN_HEIGHT - character_height:
                character_y = SCREEN_HEIGHT - character_height
    
    # 방해물 이동
    if obstacle_x > character_x:
        obstacle_x -= 3
    if obstacle_x < character_x:
        obstacle_x += 3
    if obstacle_y > character_y:
            obstacle_y -= 3
    if obstacle_y < character_y:
        obstacle_y += 3

    # 방해물 스크린 제한
    if obstacle_x < 0:
        obstacle_x = 0
    if obstacle_x >  SCREEN_WIDTH - obstacle_width:
        obstacle_x = SCREEN_WIDTH - obstacle_width
    if obstacle_y < 0:
        obstacle_y = 0
    if obstacle_y > SCREEN_HEIGHT - obstacle_height:
        obstacle_y = SCREEN_HEIGHT - obstacle_height
    
    # rectangle 정의
    character_rect = pygame.Rect(character_x, character_y, character_width, character_height)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    carrot_rect = pygame.Rect(carrot_x, carrot_y, carrot_width, carrot_height)
    
    # 오브젝트 충돌
    if character_rect.colliderect(carrot_rect):
        score += 1
        carrot_x = random.randint(0, SCREEN_WIDTH)
        carrot_y = random.randint(0, SCREEN_HEIGHT)
    
    if character_rect.colliderect(obstacle_rect): # 충돌 시 게임 종료
        # running = False
        game_over = True
        
    if game_over:
        screen.blit(game_over_text, game_over_rect)
        pygame.draw.rect(screen, WHITE, ok_rect)
        screen.blit(ok_text, ok_rect)
        
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
    
    # 오브젝트 화면 표시: screen.blit
    screen.blit(character, (character_x, character_y))
    screen.blit(obstacle, (obstacle_x, obstacle_y))
    screen.blit(carrot, (carrot_x, carrot_y))
    
    # 게임 변수 
    time_text = font.render(f"Time: {current_time}", True, (0, 0, 0))
    screen.blit(time_text, (10, 10))
    
    score_text = font.render(f"score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 30))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()