import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("치킨을 잡아라")

# 색상 설정
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 이미지 로드
chicken_img = pygame.image.load("drumstick.png")
chicken_img = pygame.transform.scale(chicken_img, (50, 50))  # 치킨 크기 조정

# 플레이어(바구니) 설정
basket_width, basket_height = 100, 20
basket_x = WIDTH // 2 - basket_width // 1
basket_y = HEIGHT - 80
basket_speed = 30

# 치킨 설정
chicken_x = random.randint(0, WIDTH - 50)
chicken_y = -50
chicken_speed = 30

# 점수와 목숨
score = 0
lives = 10

# 폰트 설정
font = pygame.font.Font(None, 36)

# 게임 루프 상태
running = True

# 게임 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += basket_speed

    # 치킨 이동
    chicken_y += chicken_speed

    # 치킨이 바닥에 닿으면 목숨 감소
    if chicken_y > HEIGHT:
        chicken_x = random.randint(0, WIDTH - 50)
        chicken_y = -50
        lives -= 1
        if lives == 0:
            running = False  # 게임 종료

    # 치킨과 바구니 충돌 체크
    if (basket_x < chicken_x < basket_x + basket_width or basket_x < chicken_x + 50 < basket_x + basket_width) and basket_y < chicken_y + 50 < basket_y + basket_height:
        chicken_x = random.randint(0, WIDTH - 50)
        chicken_y = -50
        score += 1
        chicken_speed += 0.5  # 치킨 속도 증가

    # 화면 그리기
    screen.fill(WHITE)

    # 치킨 그리기
    screen.blit(chicken_img, (chicken_x, chicken_y))

    # 바구니 그리기
    pygame.draw.rect(screen, BLACK, (basket_x, basket_y, basket_width, basket_height))

    # 점수 표시
    score_text = font.render(f"점수: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # 목숨 표시
    lives_text = font.render(f"목숨: {lives}", True, RED)
    screen.blit(lives_text, (WIDTH - 120, 10))

    # 화면 업데이트
    pygame.display.flip()
    pygame.time.delay(30)  # 속도 조절

# 게임 종료 화면
screen.fill(WHITE)
game_over_text = font.render("게임 종료", True, RED)
final_score_text = font.render(f"최종 점수: {score}", True, BLACK)
screen.blit(game_over_text, (WIDTH // 2 - 70, HEIGHT // 2 - 50))
screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2))
pygame.display.flip()
pygame.time.delay(3000)

pygame.quit()
sys.exit()
