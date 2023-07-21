from PySide2.QtCore import Qt, QMetaObject, QCoreApplication, QSize
from PySide2.QtGui import QWheelEvent, QMouseEvent, QTransform, QKeySequence
from PySide2.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QKeySequenceEdit, QSpacerItem, QPushButton, QLayout, \
    QLineEdit


class LabelBar(QWidget):
    """自定义部件，一个标签行"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # ////////////////////////////////<UI生成代码>////////////////////////////////
        self.resize(400, 50)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.widget_layout = QHBoxLayout(self)
        self.widget_layout.setObjectName(u"widget_layout")
        self.widget_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy1)
        self.lineEdit.setPlaceholderText("XXXLabel")

        self.widget_layout.addWidget(self.lineEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.widget_layout.addItem(self.horizontalSpacer_2)

        self.button_modify = QPushButton(self)
        self.button_modify.setObjectName(u"button_modify")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.button_modify.sizePolicy().hasHeightForWidth())
        self.button_modify.setSizePolicy(sizePolicy2)
        self.button_modify.setMinimumSize(QSize(10, 10))
        self.button_modify.setMaximumSize(QSize(40, 40))
        self.button_modify.setIconSize(QSize(20, 20))

        self.widget_layout.addWidget(self.button_modify)

        self.button_delete = QPushButton(self)
        self.button_delete.setObjectName(u"button_delete")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.button_delete.sizePolicy().hasHeightForWidth())
        self.button_delete.setSizePolicy(sizePolicy3)
        self.button_delete.setMinimumSize(QSize(10, 10))
        self.button_delete.setMaximumSize(QSize(40, 40))
        self.button_delete.setSizeIncrement(QSize(0, 0))
        self.button_delete.setIconSize(QSize(10, 10))
        self.button_delete.setAutoRepeat(False)
        self.button_delete.setAutoExclusive(False)
        self.button_delete.setAutoRepeatDelay(300)
        self.button_delete.setFlat(False)

        self.widget_layout.addWidget(self.button_delete)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.widget_layout.addItem(self.horizontalSpacer)

        self.keySequenceEdit = CustomKeySequenceEdit(self)
        self.keySequenceEdit.setObjectName(u"keySequenceEdit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.keySequenceEdit.sizePolicy().hasHeightForWidth())
        self.keySequenceEdit.setSizePolicy(sizePolicy4)

        self.widget_layout.addWidget(self.keySequenceEdit)

        self.button_modify.setText("修改")
        self.button_delete.setText("删除")

        # QMetaObject.connectSlotsByName(self)
        # ////////////////////////////////<UI生成代码>////////////////////////////////

        # 备用widget：文本框\按钮 互转。
        self.button_label = QPushButton()
        self.button_label.setObjectName(u"button_label")
        self.button_label.setMinimumSize(QSize(133, 0))
        self.button_label.setText("...")

        # 当前状态：
        self.current_state = "文本框"

        # 绑定各项事件处理：
        self.lineEdit.editingFinished.connect(self.finish_lineEdit)
        self.button_modify.clicked.connect(self.handle_button_modify)

    # 处理：文本框编辑结束事件
    def finish_lineEdit(self):
        self.widget_layout.replaceWidget(self.lineEdit, self.button_label)
        self.lineEdit.hide()
        self.button_label.show()
        self.button_label.setText(self.lineEdit.text())
        self.current_state = "按钮"

    def handle_button_modify(self):
        if self.current_state == "按钮":
            self.widget_layout.replaceWidget(self.button_label, self.lineEdit)
            self.button_label.hide()
            self.lineEdit.show()
            self.current_state = "文本框"


class CustomKeySequenceEdit(QKeySequenceEdit):
    """自定义部件键，仅取一个快捷键的键输入框"""
    def __init__(self, parent=None):
        super(CustomKeySequenceEdit, self).__init__(parent)

    def keyPressEvent(self, QKeyEvent):
        super(CustomKeySequenceEdit, self).keyPressEvent(QKeyEvent)
        value = self.keySequence()
        self.setKeySequence(QKeySequence(value))
        # 它的基本思路时，对于每一个键盘按下事件，当第一个key输入时，此时它的keySeq 是 key，0,0,0 ；
        # 这个时候，直接set为它自身，下一次输入将会重新从第一次输起。
        # 可能是 qt处理这个快捷键输入框处理顺序的问题，这样永远无法结束输入，也就永远无法给出信号，所以这样要手动触发信号？
        self.editingFinished.emit()
