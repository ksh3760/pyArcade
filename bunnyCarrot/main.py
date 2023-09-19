import pygame
import random

pygame.init()


# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("usagi game")

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
enemy = pygame.image.load("./enemy.png")
enemy_width = 50
enemy_height = 50
enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
enemy_y = 0
enemy_speed = 5

# 점수 타켓 설정
carrot = pygame.image.load("./carrot.png")
carrot_width = 50
carrot_height = 50
carrot_x = random.randint(0, SCREEN_WIDTH - enemy_width)
carrot_y = random.randint(0, SCREEN_HEIGHT - enemy_height)

# 게임 변수 정의
font = pygame.font.Font(None, 36) # 폰트 설정
score = 0
start_time = pygame.time.get_ticks() // 100
speed = 0

# 게임 오버 (장애물 충돌 시)
is_game_over = False
game_over_text = font.render("Game Over", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
# ok_text = font.render("OK", True, (0, 0, 0))
# ok_rect = ok_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

# 게임 루프
running = True
clock = pygame.time.Clock() # fps clock 생성

bgm = pygame.mixer.Sound("./bgm.mp3")
bgm.play(-1)
coin_sound_effect = pygame.mixer.Sound("./coinSoundEffect.mp3")

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 게임 오버 시
    if not is_game_over:
        current_time = pygame.time.get_ticks() // 100 - start_time
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_x -= 10 + speed
            if character_x < 0:  # 화면 왼쪽 벽을 벗어나지 않도록 제한
                character_x = 0
        if keys[pygame.K_RIGHT]:
            character_x += 10 + speed
            if character_x > SCREEN_WIDTH - character_width:  # 화면 오른쪽 벽을 벗어나지 않도록 제한
                character_x = SCREEN_WIDTH - character_width
        if keys[pygame.K_UP]:
            character_y -= 10 + speed
            if character_y < 0:  # 화면 위쪽 벽을 벗어나지 않도록 제한
                character_y = 0
        if keys[pygame.K_DOWN]:
            character_y += 10 + speed
            if character_y > SCREEN_HEIGHT - character_height: # 화면 아래쪽 벽을 벗어나지 않도록 제한
                character_y = SCREEN_HEIGHT - character_height
    
    # 방해물 이동
    if enemy_x > character_x:
        enemy_x -= 3 + speed
    if enemy_x < character_x:
        enemy_x += 3 + speed
    if enemy_y > character_y:
        enemy_y -= 3 + speed
    if enemy_y < character_y:
        enemy_y += 3 + speed

    # 방해물 스크린 제한
    if enemy_x < 0:
        enemy_x = 0
    if enemy_x >  SCREEN_WIDTH - enemy_width:
        enemy_x = SCREEN_WIDTH - enemy_width
    if enemy_y < 0:
        enemy_y = 0
    if enemy_y > SCREEN_HEIGHT - enemy_height:
        enemy_y = SCREEN_HEIGHT - enemy_height
    
    # rectangle 정의 (오브젝트 판정)
    character_rect = pygame.Rect(character_x, character_y, character_width, character_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    carrot_rect = pygame.Rect(carrot_x, carrot_y, carrot_width, carrot_height)
    
    # 점수 획득
    if character_rect.colliderect(carrot_rect):
        score += 1
        carrot_x = random.randint(30, SCREEN_WIDTH-30)
        carrot_y = random.randint(30, SCREEN_HEIGHT-30)
        coin_sound_effect.play()
    
    # 장애물 충돌
    if character_rect.colliderect(enemy_rect): # 충돌 시 게임 종료
        bgm.stop()
        is_game_over = True
        screen.blit(game_over_text, game_over_rect)
        
    # if is_game_over:
        # pygame.draw.rect(screen, WHITE, ok_rect)
        # screen.blit(ok_text, ok_rect)
        
    if is_game_over:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
    
    # 오브젝트 화면 표시: screen.blit
    screen.blit(character, (character_x, character_y))
    screen.blit(enemy, (enemy_x, enemy_y))
    screen.blit(carrot, (carrot_x, carrot_y))
    
    # 폰트 출력
    time_text = font.render(f"Time: {current_time}", True, (0, 0, 0))
    screen.blit(time_text, (10, 10))
    
    score_text = font.render(f"score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()