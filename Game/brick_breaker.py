import pygame
import random
import os

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("서울의닭 미니게임 - 치킨으로 벽돌을 깨라!")

# 색상 설정
WHITE = (255, 255, 255)   # 배경색 (흰색)
RED = (255, 0, 0)         # 패들 색상 (빨강)
ORANGE = (255, 165, 0)    # 벽돌 색상 (오렌지)
BLACK = (0, 0, 0)         # 텍스트 색상

# 현재 파일 위치 기준으로 이미지 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHICKEN_IMAGE_PATH = os.path.join(BASE_DIR, "drumstick.png")

# 이미지 로드 (닭다리)
chicken_img = pygame.image.load(CHICKEN_IMAGE_PATH)
chicken_img = pygame.transform.scale(chicken_img, (120, 120))  # 크기 2배 증가

# 패들 설정
paddle_width = 100
paddle_height = 10
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 50, paddle_width, paddle_height)
paddle_speed = 10

# 공 (치킨 닭다리) 설정
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 80, 80)  # 크기 조정
ball_dx = random.choice([-6, 6])  # 속도 1.5배 증가
ball_dy = -6

# 벽돌 설정
brick_rows = 5
brick_cols = 8
brick_width = WIDTH // brick_cols
brick_height = 30
bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        brick = pygame.Rect(col * brick_width, row * brick_height, brick_width, brick_height)
        bricks.append(brick)

# 게임 상태 변수
game_started = False

# 폰트 설정
font = pygame.font.Font(None, 50)

# 게임 루프 실행
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)  # 배경색 변경 (하얀색)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_started = True  # 스페이스바를 누르면 게임 시작

    if not game_started:
        # 게임 시작 전 Start 버튼 표시
        start_text = font.render("Press SPACE to Start", True, BLACK)
        screen.blit(start_text, (WIDTH // 2 - 150, HEIGHT // 2))
    else:
        # 키 입력
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-paddle_speed, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(paddle_speed, 0)

        # 공 이동 (치킨 닭다리)
        ball.move_ip(ball_dx, ball_dy)

        # 벽과 충돌
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_dx = -ball_dx
        if ball.top <= 0:
            ball_dy = -ball_dy

        # 패들과 충돌
        if ball.colliderect(paddle):
            ball_dy = -ball_dy

        # 벽돌과 충돌
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_dy = -ball_dy
                break

        # 공이 바닥에 떨어지면 게임 오버
        if ball.bottom >= HEIGHT:
            print("Game Over")
            running = False

        # 모든 벽돌을 부수면 승리
        if not bricks:
            print("You Win!")
            running = False

        # 패들 그리기 (빨간색)
        pygame.draw.rect(screen, RED, paddle)

        # 공 대신 치킨 닭다리 이미지 그리기
        screen.blit(chicken_img, (ball.x, ball.y))

        # 벽돌 그리기 (오렌지색)
        for brick in bricks:
            pygame.draw.rect(screen, ORANGE, brick)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
