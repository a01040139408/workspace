import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QColorDialog, QSlider, QFileDialog, QWidget
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QIcon
from PyQt5.QtCore import Qt, QPoint


class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 기본 설정
        self.setWindowTitle("그림판 앱")
        self.setGeometry(100, 100, 800, 600)

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 레이아웃
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # 캔버스 위젯
        self.canvas = QLabel()
        self.canvas.setPixmap(QPixmap(800, 500))
        self.canvas.pixmap().fill(Qt.white)

        # 버튼: 색상 선택
        color_button = QPushButton("색상 선택")
        color_button.setIcon(QIcon("palette.png"))
        color_button.clicked.connect(self.select_color)
        button_layout.addWidget(color_button)

        # 버튼: 브러시 크기
        self.brush_size_slider = QSlider(Qt.Horizontal)
        self.brush_size_slider.setRange(1, 20)
        self.brush_size_slider.setValue(3)
        button_layout.addWidget(QLabel("브러시 크기"))
        button_layout.addWidget(self.brush_size_slider)

        # 버튼: 초기화
        clear_button = QPushButton("초기화")
        clear_button.setIcon(QIcon("clear.png"))
        clear_button.clicked.connect(self.clear_canvas)
        button_layout.addWidget(clear_button)

        # 버튼: 저장
        save_button = QPushButton("저장")
        save_button.setIcon(QIcon("save2.png"))
        save_button.clicked.connect(self.save_canvas)
        button_layout.addWidget(save_button)

        # 캔버스와 버튼 추가
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)

        # 초기 값
        self.last_point = QPoint()
        self.drawing = False
        self.brush_color = Qt.black
        self.brush_size = 3

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.canvas.underMouse():
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.canvas.pixmap())
            pen = QPen(self.brush_color, self.brush_size_slider.value(), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.brush_color = color

    def clear_canvas(self):
        self.canvas.pixmap().fill(Qt.white)
        self.update()

    def save_canvas(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "저장", "", "PNG Files (*.png);;JPEG Files (*.jpg)", options=options)
        if file_path:
            self.canvas.pixmap().save(file_path, "PNG")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawingApp()
    window.show()
    sys.exit(app.exec_())
