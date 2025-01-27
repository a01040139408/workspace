import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QDateTime


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 상태바 설정
        self.statusBar().showMessage('Ready')  # 상태바 초기 메시지
        self.updateStatusBarWithDateTime()

        # 타이머 설정
        timer = QTimer(self)
        timer.timeout.connect(self.updateStatusBarWithDateTime)
        timer.start(1000)  # 1초마다 업데이트

        # 메뉴바 설정
        menubar = self.menuBar()

        # File 메뉴 생성
        fileMenu = menubar.addMenu('File')
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QApplication.instance().quit)
        fileMenu.addAction(exitAction)

        # Edit 메뉴 생성
        editMenu = menubar.addMenu('Edit')
        copyAction = QAction('Copy', self)
        copyAction.setShortcut('Ctrl+C')
        copyAction.setStatusTip('Copy selected text')
        copyAction.triggered.connect(self.copyActionTriggered)
        editMenu.addAction(copyAction)

        pasteAction = QAction('Paste', self)
        pasteAction.setShortcut('Ctrl+V')
        pasteAction.setStatusTip('Paste text')
        pasteAction.triggered.connect(self.pasteActionTriggered)
        editMenu.addAction(pasteAction)

        # View 메뉴 생성
        viewMenu = menubar.addMenu('View')
        statusBarToggle = QAction('Toggle Status Bar', self, checkable=True)
        statusBarToggle.setChecked(True)
        statusBarToggle.setStatusTip('Show or hide the status bar')
        statusBarToggle.triggered.connect(self.toggleStatusBar)
        viewMenu.addAction(statusBarToggle)

        # Tools 메뉴 생성
        toolsMenu = menubar.addMenu('Tools')
        settingsAction = QAction('Settings', self)
        settingsAction.setStatusTip('Open settings')
        settingsAction.triggered.connect(self.settingsActionTriggered)
        toolsMenu.addAction(settingsAction)

        # Help 메뉴 생성
        helpMenu = menubar.addMenu('Help')
        aboutAction = QAction('About', self)
        aboutAction.setStatusTip('About this application')
        aboutAction.triggered.connect(self.aboutActionTriggered)
        helpMenu.addAction(aboutAction)

        # 툴바 설정
        toolbar = QToolBar('Main Toolbar', self)
        self.addToolBar(toolbar)

        # 툴바에 액션 추가
        toolbar.addAction(exitAction)

        # 저장 액션 추가
        saveAction = QAction(QIcon('save.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current progress')
        saveAction.triggered.connect(self.saveActionTriggered)
        toolbar.addAction(saveAction)

        # Edit 액션 추가
        editAction = QAction(QIcon('edit.png'), 'Edit', self)
        editAction.setShortcut('Ctrl+E')
        editAction.setStatusTip('Edit content')
        editAction.triggered.connect(self.editActionTriggered)
        toolbar.addAction(editAction)

        # Print 액션 추가
        printAction = QAction(QIcon('print.png'), 'Print', self)
        printAction.setShortcut('Ctrl+P')
        printAction.setStatusTip('Print content')
        printAction.triggered.connect(self.printActionTriggered)
        toolbar.addAction(printAction)

        # 메인 윈도우 설정
        self.setWindowTitle('나만의 창 만들기')  # 창 제목
        self.setWindowIcon(QIcon('web icon.png'))  # 아이콘 추가
        self.resize(600, 400)  # 창 크기 설정
        self.center()  # 창을 화면 중앙에 배치

        # Quit 버튼 생성
        btn = QPushButton('Quit', self)
        btn.move(250, 300)  # 버튼 위치 설정
        btn.setToolTip('툴팁 적용 완료')  # 툴팁 텍스트 설정
        btn.clicked.connect(QApplication.instance().quit)

        self.show()  # 창 표시

    def center(self):
        # 화면 중심으로 창 이동
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def updateStatusBarWithDateTime(self):
        # 현재 날짜와 시간 업데이트
        currentDateTime = QDateTime.currentDateTime()
        self.statusBar().showMessage(currentDateTime.toString('yyyy년 MM월 dd일 hh:mm:ss'))

    # 트리거 메서드 추가
    def saveActionTriggered(self):
        self.statusBar().showMessage('Save clicked!')

    def openActionTriggered(self):
        self.statusBar().showMessage('Open clicked!')

    def editActionTriggered(self):
        self.statusBar().showMessage('Edit clicked!')

    def printActionTriggered(self):
        self.statusBar().showMessage('Print clicked!')

    def copyActionTriggered(self):
        self.statusBar().showMessage('Copy clicked!')

    def pasteActionTriggered(self):
        self.statusBar().showMessage('Paste clicked!')

    def toggleStatusBar(self, state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def settingsActionTriggered(self):
        self.statusBar().showMessage('Settings clicked!')

    def aboutActionTriggered(self):
        self.statusBar().showMessage('About clicked!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
