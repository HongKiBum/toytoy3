import pygame
import math
import random
import os


class Roulette:
    def __init__(self, values):
        self.values = values
        self.segments = len(values)
        self.angle = 0
        self.speed = 0
        self.is_spinning = False
        self.is_stopping = False  # 멈추는 중인지 상태를 확인
        self.width, self.height = 500, 500
        self.center = (self.width // 2, self.height // 2)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Roulette")

        # 기본 한글 폰트 사용 (맑은 고딕 또는 시스템 한글 폰트 자동 선택)
        self.font = pygame.font.SysFont("malgungothic", 20)

        self.clock = pygame.time.Clock()

    def draw_roulette(self):
        self.screen.fill((60, 0, 0))  # 배경 색 갈색
        radius = min(self.width, self.height) // 2 - 40
        triangle_size = 15

        # 룰렛 섹션 그리기
        colors = [
            (255, 0, 0),    # 빨간색
            (0, 0, 0)       # 검은색
        ]

        for i in range(self.segments):
            start_angle = math.radians(360 / self.segments * i + self.angle)
            end_angle = math.radians(360 / self.segments * (i + 1) + self.angle)
            color = colors[i % len(colors)]

            # 섹션을 반원으로 그리기
            points = [self.center]  # 섹션의 중심점 추가
            num_points = 50  # 반원을 구성할 점 개수
            for j in range(num_points + 1):
                t = j / num_points
                angle = start_angle + (end_angle - start_angle) * t
                x = self.center[0] + radius * math.cos(angle)
                y = self.center[1] + radius * math.sin(angle)
                points.append((x, y))
            pygame.draw.polygon(self.screen, color, points)

            # 텍스트 표시
            text_angle = (start_angle + end_angle) / 2
            text_x = self.center[0] + radius * 0.7 * math.cos(text_angle)
            text_y = self.center[1] + radius * 0.7 * math.sin(text_angle)
            text_surface = self.font.render(self.values[i], True, (255, 255, 255))  # 흰 텍스트
            self.screen.blit(text_surface, (text_x - text_surface.get_width() // 2,
                                            text_y - text_surface.get_height() // 2))

        # 중심 원
        pygame.draw.circle(self.screen, (60, 0, 0), self.center, 10)

        # 삼각형 포인터 (아래 방향)
        pygame.draw.polygon(self.screen, (255, 255, 255), [
            (self.center[0], self.center[1] - radius + triangle_size),
            (self.center[0] - triangle_size, self.center[1] - radius),
            (self.center[0] + triangle_size, self.center[1] - radius)
        ])

    def update(self):
        if self.is_spinning:
            self.angle += self.speed
            if self.is_stopping:  # 멈추는 중일 때 감속
                self.speed *= 0.98
                if self.speed < 0.1:  # 감속이 끝났으면 멈춤
                    self.speed = 0
                    self.is_spinning = False
                    self.is_stopping = False
                    result = self.get_result()
                    print(f"Selected value: {result}")

    def get_result(self):
        # 화살표는 아래쪽(270도)을 기준으로 결과를 계산
        arrow_angle = (270 - self.angle) % 360
        index = int(arrow_angle // (360 / self.segments))
        return self.values[index]

    def toggle_spin(self):
        if not self.is_spinning:  # 멈춘 상태라면 회전 시작
            self.speed = random.uniform(10, 15)
            self.is_spinning = True
        elif not self.is_stopping:  # 회전 중일 때 멈추도록 설정
            self.is_stopping = True

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.toggle_spin()

            self.update()
            self.draw_roulette()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()