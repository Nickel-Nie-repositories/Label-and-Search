from PySide2.QtCore import QSize, QCoreApplication
from PySide2.QtGui import QTransform
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem, QWidget


class StartLabelBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ////////////////////////////////<UI生成代码>////////////////////////////////
        self.resize(400, 50)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName(u"label_horizontalLayout")
        self.button_add = QPushButton()
        self.button_add.setObjectName(u"button_add")
        self.button_add.setMinimumSize(QSize(133, 0))

        self.horizontalLayout.addWidget(self.button_add)

        self.horizontalSpacer = QSpacerItem(235, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_add.setText("添加Label")

        # QMetaObject.connectSlotsByName(Form)

        # ////////////////////////////////<UI生成代码>////////////////////////////////
