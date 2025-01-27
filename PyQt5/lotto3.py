import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QTimer, QPropertyAnimation, QEasingCurve, QRect, Qt

class LottoGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("멋진 로또 번호 생성기")
        self.setGeometry(100, 100, 400, 500)
        
        layout = QVBoxLayout()
        
        self.generate_button = QPushButton("로또 번호 생성")
        self.generate_button.setFont(QFont("Arial", 20))
        self.generate_button.clicked.connect(self.generate_numbers)
        layout.addWidget(self.generate_button)
        
        self.number_labels = []
        for _ in range(6):
            label = QLabel("00")
            label.setFont(QFont("Arial", 36, QFont.Bold))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color: yellow; border-radius: 30px;")
            layout.addWidget(label)
            self.number_labels.append(label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.animations = []

    def generate_numbers(self):
        numbers = random.sample(range(1, 46), 6)
        numbers.sort()
        
        for i, number in enumerate(numbers):
            animation = QPropertyAnimation(self.number_labels[i], b"geometry")
            animation.setDuration(1000)
            animation.setStartValue(QRect(0, 0, 0, 0))
            animation.setEndValue(self.number_labels[i].geometry())
            animation.setEasingCurve(QEasingCurve.OutBounce)
            
            self.animations.append(animation)
            
            QTimer.singleShot(i * 200, lambda i=i, number=number: self.update_label(i, number))
    
    def update_label(self, index, number):
        self.number_labels[index].setText(f"{number:02d}")
        self.animations[index].start()
        
        color_animation = QPropertyAnimation(self.number_labels[index], b"styleSheet")
        color_animation.setDuration(1000)
        color_animation.setStartValue("background-color: yellow; border-radius: 30px;")
        color_animation.setEndValue(f"background-color: {self.get_random_color()}; border-radius: 30px;")
        color_animation.start()

    def get_random_color(self):
        return f"rgb({random.randint(100,255)}, {random.randint(100,255)}, {random.randint(100,255)})"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LottoGenerator()
    window.show()
    sys.exit(app.exec_())
