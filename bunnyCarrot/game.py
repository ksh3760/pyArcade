import pygame
import random
from constant import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        
        # game display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.speed = 0 # difficulty
        self.start_time = pygame.time.get_ticks() // 100
        self.running = True
        self.clock = pygame.time.Clock() # fps clock
        
        # game over
        self.is_game_over = False
        self.game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        self.game_over_rect = self.game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # game bgm
        self.bgm = pygame.mixer.Sound(BGM_PATH)
        self.bgm.play(-1)
        self.coin_sound_effect = pygame.mixer.Sound(COIN_SOUND_EFFECT_PATH)
        self.game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND_PATH)

        # character
        self.character = pygame.image.load(CHARACTER_IMG_PATH)
        self.character = pygame.transform.scale(self.character, (OBJ_SIZE, OBJ_SIZE)) # 캐릭터 크기
        self.character_rect = self.character.get_rect() # 캐릭터 이미지의 rect 정보 저장
        self.character_rect.centerx = round(SCREEN_WIDTH / 2)
        self.character_rect.centery = round(SCREEN_HEIGHT / 2)
        self.character_width = OBJ_SIZE
        self.character_height = OBJ_SIZE
        self.character_x = SCREEN_WIDTH / 2 
        self.character_y = SCREEN_HEIGHT / 2

        # enemy
        self.enemy = pygame.image.load(ENEMY_IMG_PATH)
        self.enemy_width = OBJ_SIZE
        self.enemy_height = OBJ_SIZE
        self.enemy_x = random.randint(0, SCREEN_WIDTH - self.enemy_width)
        self.enemy_y = 0
        self.enemy_speed = 5

        # score target
        self.carrot = pygame.image.load(CARROT_IMG_PATH)
        self.carrot_width = OBJ_SIZE
        self.carrot_height = OBJ_SIZE
        self.carrot_x = random.randint(0, SCREEN_WIDTH - self.enemy_width)
        self.carrot_y = random.randint(0, SCREEN_HEIGHT - self.enemy_height)
        
        self.run()

    def run(self):
        while self.running:
            self.screen.fill(WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            if not self.is_game_over:
                current_time = pygame.time.get_ticks() // 100 - self.start_time
                
                # user control
                # character default speed = 10
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.character_x -= 10 + self.speed
                    if self.character_x < 0:  # 화면 왼쪽 벽을 벗어나지 않도록 제한
                        self.character_x = 0
                if keys[pygame.K_RIGHT]:
                    self.character_x += 10 + self.speed
                    if self.character_x > SCREEN_WIDTH - self.character_width:  # 화면 오른쪽 벽을 벗어나지 않도록 제한
                        self.character_x = SCREEN_WIDTH - self.character_width
                if keys[pygame.K_UP]:
                    self.character_y -= 10 + self.speed
                    if self.character_y < 0:  # 화면 위쪽 벽을 벗어나지 않도록 제한
                        self.character_y = 0
                if keys[pygame.K_DOWN]:
                    self.character_y += 10 + self.speed
                    if self.character_y > SCREEN_HEIGHT - self.character_height: # 화면 아래쪽 벽을 벗어나지 않도록 제한
                        self.character_y = SCREEN_HEIGHT - self.character_height
                        
            # enemy move
            # default speed = 3
            if self.enemy_x > self.character_x:
                self.enemy_x -= 3 + self.speed
            if self.enemy_x < self.character_x:
                self.enemy_x += 3 + self.speed
            if self.enemy_y > self.character_y:
                self.enemy_y -= 3 + self.speed
            if self.enemy_y < self.character_y:
                self.enemy_y += 3 + self.speed

            # enemy screen limit
            # if self.enemy_x < 0:
            #     self.enemy_x = 0
            # if self.enemy_x >  SCREEN_WIDTH - self.enemy_width:
            #     self.enemy_x = SCREEN_WIDTH - self.enemy_width
            # if self.enemy_y < 0:
            #     self.enemy_y = 0
            # if self.enemy_y > SCREEN_HEIGHT - self.enemy_height:
            #     self.enemy_y = SCREEN_HEIGHT - self.enemy_height
            
            # rectangle 정의 (오브젝트 판정)
            character_rect = pygame.Rect(self.character_x, self.character_y, self.character_width, self.character_height)
            enemy_rect = pygame.Rect(self.enemy_x, self.enemy_y, self.enemy_width, self.enemy_height)
            carrot_rect = pygame.Rect(self.carrot_x, self.carrot_y, self.carrot_width, self.carrot_height)
            
            # character gets socre(carrot)
            if character_rect.colliderect(carrot_rect):
                self.score += 1
                self.carrot_x = random.randint(30, SCREEN_WIDTH-30)
                self.carrot_y = random.randint(30, SCREEN_HEIGHT-30)
                self.coin_sound_effect.play()
            
            # when character & enemy crush (game over)
            if character_rect.colliderect(enemy_rect):
                self.bgm.stop()
                self.is_game_over = True
                self.screen.blit(self.game_over_text, self.game_over_rect)
            
            if self.is_game_over:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        running = False
            
            # 오브젝트 스크린 출력
            self.screen.blit(self.character, (self.character_x, self.character_y))
            self.screen.blit(self.enemy, (self.enemy_x, self.enemy_y))
            self.screen.blit(self.carrot, (self.carrot_x, self.carrot_y))
            
            # 폰트 스크린 출력
            time_text = self.font.render(f"Time: {current_time}", True, (0, 0, 0))
            self.screen.blit(time_text, (10, 10))
            
            score_text = self.font.render(f"score: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_text, (10, 30))
            
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
