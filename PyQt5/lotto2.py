import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer


class LottoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 창 설정
        self.setWindowTitle('🌟 로또 번호 생성기 🌟')
        self.setGeometry(300, 100, 800, 600)
        self.setWindowIcon(QIcon('lotto_icon.png'))

        # 메인 위젯
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 메인 레이아웃 설정
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # 제목 라벨
        title_label = QLabel('✨ 로또 번호 추첨기 ✨')
        title_label.setFont(QFont('Verdana', 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: gold; text-shadow: 2px 2px black;")
        layout.addWidget(title_label)

        # 공을 표시할 라벨들을 담을 레이아웃
        self.ball_layout = QHBoxLayout()
        self.ball_labels = []
        for _ in range(6):
            ball_label = QLabel(self)
            ball_label.setPixmap(QPixmap('lotto_ball.png').scaled(100, 100, Qt.KeepAspectRatio))
            ball_label.setAlignment(Qt.AlignCenter)
            ball_label.setVisible(False)  # 처음에는 숨김
            self.ball_labels.append(ball_label)
            self.ball_layout.addWidget(ball_label)
        layout.addLayout(self.ball_layout)

        # 추첨 결과 출력 라벨
        self.result_label = QLabel('번호가 곧 추첨됩니다!')
        self.result_label.setFont(QFont('Courier', 20, QFont.Bold))
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            color: white;
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 10px;
            padding: 20px;
        """)
        layout.addWidget(self.result_label)

        # 번호 생성 버튼
        self.generate_button = QPushButton('🎰 추첨 시작 🎰')
        self.generate_button.setFont(QFont('Arial', 18, QFont.Bold))
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4500;
                color: white;
                border: 2px solid gold;
                padding: 15px 30px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #FF6347;
            }
        """)
        self.generate_button.clicked.connect(self.start_lotto_animation)
        layout.addWidget(self.generate_button)

        central_widget.setLayout(layout)
        self.show()

    def start_lotto_animation(self):
        # 추첨 번호 생성 및 애니메이션 초기화
        self.lotto_numbers = random.sample(range(1, 46), 6)
        self.current_ball_index = 0

        # 버튼 비활성화
        self.generate_button.setEnabled(False)

        # 애니메이션 타이머 설정
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.reveal_next_ball)
        self.animation_timer.start(500)  # 0.5초 간격으로 공 표시

    def reveal_next_ball(self):
        if self.current_ball_index < len(self.lotto_numbers):
            # 현재 공과 번호 표시
            number = self.lotto_numbers[self.current_ball_index]
            ball_label = self.ball_labels[self.current_ball_index]
            ball_label.setPixmap(QPixmap('lotto_ball.png').scaled(100, 100, Qt.KeepAspectRatio))
            ball_label.setText(str(number))
            ball_label.setAlignment(Qt.AlignCenter)
            ball_label.setStyleSheet("""
                color: black;
                font-size: 20px;
                font-weight: bold;
                background-color: white;
                border-radius: 50px;
                border: 2px solid black;
                padding: 20px;
            """)
            ball_label.setVisible(True)
            self.current_ball_index += 1
        else:
            # 모든 공 표시 완료 후 애니메이션 종료
            self.animation_timer.stop()
            self.result_label.setText(f'🎉 최종 번호: {sorted(self.lotto_numbers)} 🎉')
            self.generate_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LottoApp()
    sys.exit(app.exec_())
