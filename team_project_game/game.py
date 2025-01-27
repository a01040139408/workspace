import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("치킨 타워 쌓기")

# 색상 설정
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)

# 이미지 로드
chicken_img = pygame.image.load("drumstick.png")
chicken_img = pygame.transform.scale(chicken_img, (50, 50))  # 크기 조정

# 치킨 위치와 속도
chicken_x = WIDTH // 2 - 25  # 중앙에서 시작
chicken_y = 0
chicken_speed_x = 6  # 좌우 움직임 속도
moving_right = True  # 치킨이 오른쪽으로 이동 중인지 여부

# 점수와 타워
score = 0
tower = []

# 폰트 설정
font = pygame.font.Font(None, 36)

# 게임 루프 상태
running = True
is_dropping = False

# 바닥 높이
ground_height = HEIGHT - 50

# 카메라 오프셋
camera_offset = 0

# 게임 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # 스페이스바를 눌렀을 때
                is_dropping = True

    screen.fill(WHITE)

    # 카메라 오프셋 계산
    max_visible_height = HEIGHT - 100
    if len(tower) * 50 > max_visible_height:
        camera_offset = (len(tower) * 50) - max_visible_height

    # 바닥 그리기 (카메라 오프셋 적용)
    pygame.draw.rect(screen, BROWN, (0, ground_height - camera_offset, WIDTH, 50))

    # 치킨 움직임
    if not is_dropping:
        if moving_right:
            chicken_x += chicken_speed_x
            if chicken_x + 50 > WIDTH:
                moving_right = False
        else:
            chicken_x -= chicken_speed_x
            if chicken_x < 0:
                moving_right = True
    else:
        chicken_y += 30  # 치킨이 빠르게 떨어짐
        if chicken_y > ground_height - len(tower) * 50 - camera_offset:
            chicken_y = ground_height - len(tower) * 50 - camera_offset
            if len(tower) > 0 and abs(chicken_x - tower[-1][0]) > 50:  # 중심 기준 검사 제거
                running = False  # 게임 오버 조건
            else:
                tower.append((chicken_x, chicken_y + camera_offset))  # 치킨 위치 저장
                chicken_y = 0
                is_dropping = False
                score += 1

    # 타워 그리기 (카메라 오프셋 적용)
    for pos in tower:
        screen.blit(chicken_img, (pos[0], pos[1] - camera_offset))

    # 치킨 그리기 (카메라 오프셋 적용)
    screen.blit(chicken_img, (chicken_x, chicken_y - camera_offset))

    # 점수 표시 (오른쪽 상단)
    score_text = font.render(f"점수: {score}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH - 150, 10))

    # 화면 업데이트
    pygame.display.flip()
    pygame.time.delay(10)  # 속도 조절 (10ms 딜레이로 빠르게 설정)

pygame.quit()
sys.exit()