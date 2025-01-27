import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer


class LottoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 창 제목 및 크기 설정
        self.setWindowTitle('🎊 Lotto Generator 🎊')
        self.setGeometry(400, 200, 600, 500)
        self.setWindowIcon(QIcon('lotto_icon.png'))

        # 메인 위젯
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # 제목 라벨
        title_label = QLabel('✨ 행운의 Lotto 번호판  ✨')
        title_label.setFont(QFont('Comic Sans MS', 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #ffcc00; text-shadow: 2px 2px #000;")
        layout.addWidget(title_label)

        # 번호 출력 라벨
        self.number_label = QLabel('번호가 여기 표시됩니다!')
        self.number_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.number_label.setAlignment(Qt.AlignCenter)
        self.number_label.setStyleSheet("""
            color: white;
            background-color: #333;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        """)
        layout.addWidget(self.number_label)

        # 번호 생성 버튼
        self.generate_button = QPushButton('🎰번호 뽑기 시작🎰')
        self.generate_button.setFont(QFont('Arial', 18, QFont.Bold))
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #00bfff;
                color: white;
                border: 2px solid #007acc;
                padding: 15px 30px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #007acc;
            }
        """)
        self.generate_button.clicked.connect(self.start_lotto_animation)
        layout.addWidget(self.generate_button)

        # 설명 라벨
        instruction_label = QLabel('※ 로또 번호는 1~45 사이에서 무작위로 선택됩니다.')
        instruction_label.setFont(QFont('Arial', 12))
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("color: #999; margin-top: 15px;")
        layout.addWidget(instruction_label)

        # 스타일 설정
        central_widget.setLayout(layout)
        central_widget.setStyleSheet("""
            background-color: #222;
            border: none;
            border-radius: 15px;
            margin: 15px;
        """)

        self.show()

    def start_lotto_animation(self):
        # 애니메이션용 타이머
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.show_random_numbers)
        self.animation_timer.start(100)  # 0.1초마다 실행

        # 버튼 비활성화
        self.generate_button.setEnabled(False)

        # 2초 후에 최종 번호 출력
        QTimer.singleShot(2000, self.generate_numbers)

    def show_random_numbers(self):
        # 애니메이션 동안 임시 번호를 표시
        temp_numbers = random.sample(range(1, 46), 6)
        self.number_label.setText(f'🎲 {sorted(temp_numbers)} 🎲')

    def generate_numbers(self):
        # 애니메이션 종료 및 최종 번호 출력
        self.animation_timer.stop()
        final_numbers = random.sample(range(1, 46), 6)
        self.number_label.setText(f'🎉 최종 번호: {sorted(final_numbers)} 🎉')
        self.number_label.setStyleSheet("""
            color: #ff5733;
            background-color: white;
            font-size: 22px;
            border: 3px solid #ff5733;
            border-radius: 15px;
            padding: 20px;
        """)
        self.generate_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LottoApp()
    sys.exit(app.exec_())
