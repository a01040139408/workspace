import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class LottoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('로또 번호 생성기')
        self.setGeometry(300, 300, 600, 700)

        # 메인 위젯과 레이아웃
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()

        # 상단 제목
        self.title_label = QLabel('행운의 번호를 잡아라!')
        self.title_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label, 0, 0, 1, 7)

        # 번호 공 표시 영역
        self.result_labels = []
        for i in range(6):
            label = QLabel()
            pixmap = QPixmap('lotto_ball.png').scaled(80, 80, Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label, 1, i + 1)
            self.result_labels.append(label)

        # 번호판 생성
        self.number_labels = []
        colors = ['#FFD700', '#87CEEB', '#FF6347', '#32CD32', '#D3D3D3']
        for i in range(1, 46):
            number_label = QLabel(str(i))
            number_label.setFont(QFont('Arial', 14, QFont.Bold))
            number_label.setAlignment(Qt.AlignCenter)
            number_label.setStyleSheet(f"background-color: {colors[(i - 1) // 9]}; border: 2px solid black; border-radius: 20px; padding: 10px;")
            layout.addWidget(number_label, (i - 1) // 9 + 2, (i - 1) % 9)
            self.number_labels.append(number_label)

        # 버튼 레이아웃
        self.generate_button = QPushButton('로또 번호 생성')
        self.generate_button.setFont(QFont('Arial', 16))
        self.generate_button.setStyleSheet("background-color: #32CD32; color: white; padding: 10px; border-radius: 10px;")
        self.generate_button.clicked.connect(self.generate_numbers)
        layout.addWidget(self.generate_button, 8, 2, 1, 2)

        self.exit_button = QPushButton('종료')
        self.exit_button.setFont(QFont('Arial', 16))
        self.exit_button.setStyleSheet("background-color: #FF6347; color: white; padding: 10px; border-radius: 10px;")
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button, 8, 5, 1, 2)

        central_widget.setLayout(layout)

    def generate_numbers(self):
        numbers = sorted(random.sample(range(1, 46), 6))
        for i, num in enumerate(numbers):
            self.result_labels[i].setText(str(num))
            self.result_labels[i].setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
            self.result_labels[i].setAlignment(Qt.AlignCenter)

        for label in self.number_labels:
            label.setStyleSheet(label.styleSheet().replace('border: 4px solid black;', ''))

        for num in numbers:
            self.number_labels[num - 1].setStyleSheet(
                self.number_labels[num - 1].styleSheet() + 'border: 4px solid black;'
            )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LottoApp()
    ex.show()
    sys.exit(app.exec_())
