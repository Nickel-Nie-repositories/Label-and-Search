from PySide2.QtCore import QSize, QCoreApplication, QRect, Signal, QObject
from PySide2.QtGui import QTransform, Qt
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem, QWidget, QProgressBar, QLabel, QDialog


class CurrentProgressSignal(QObject):
    current_progress_signal = Signal(int, str)


class ProgressBarWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # ////////////////////////////////<UI生成代码>////////////////////////////////

        self.resize(497, 317)
        self.setFixedSize(497, 317)
        self.progressBar = QProgressBar(self)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(90, 120, 321, 23))
        self.progressBar.setValue(0)
        self.label_text = QLabel(self)
        self.label_text.setObjectName(u"label_text")
        self.label_text.setGeometry(QRect(20, 150, 400, 16))
        self.button_close = QPushButton(self)
        self.button_close.setObjectName(u"button_close")
        self.button_close.setGeometry(QRect(330, 250, 93, 28))
        self.label_title = QLabel(self)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(30, 30, 200, 15))

        self.setWindowTitle("子窗口")
        self.label_text.setText(" ")
        self.button_close.setText("取消")
        self.label_title.setText(" ")

        # QMetaObject.connectSlotsByName(self)

        # ////////////////////////////////<UI生成代码>////////////////////////////////

        self.signal = CurrentProgressSignal()
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        # self.signal.current_progress_signal.connect(self.handle_current_progress_signal)

    def handle_current_progress_signal(self, progress: int, file: str):
        self.progressBar.setValue(progress)
        self.label_text.setText(file)
