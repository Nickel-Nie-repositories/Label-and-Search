# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shortcut_setting.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(405, 299)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.keySequenceEdit = QKeySequenceEdit(Dialog)
        self.keySequenceEdit.setObjectName(u"keySequenceEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.keySequenceEdit.sizePolicy().hasHeightForWidth())
        self.keySequenceEdit.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.keySequenceEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.horizontalSpacer_2 = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.keySequenceEdit_2 = QKeySequenceEdit(Dialog)
        self.keySequenceEdit_2.setObjectName(u"keySequenceEdit_2")
        sizePolicy1.setHeightForWidth(self.keySequenceEdit_2.sizePolicy().hasHeightForWidth())
        self.keySequenceEdit_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.keySequenceEdit_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.horizontalSpacer_3 = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.keySequenceEdit_3 = QKeySequenceEdit(Dialog)
        self.keySequenceEdit_3.setObjectName(u"keySequenceEdit_3")
        sizePolicy1.setHeightForWidth(self.keySequenceEdit_3.sizePolicy().hasHeightForWidth())
        self.keySequenceEdit_3.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.keySequenceEdit_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.horizontalSpacer_4 = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.keySequenceEdit_4 = QKeySequenceEdit(Dialog)
        self.keySequenceEdit_4.setObjectName(u"keySequenceEdit_4")
        sizePolicy1.setHeightForWidth(self.keySequenceEdit_4.sizePolicy().hasHeightForWidth())
        self.keySequenceEdit_4.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.keySequenceEdit_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u9002\u5e94\u5c4f\u5e55", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u4e0a\u4e00\u5f20", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u4e0b\u4e00\u5f20", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Backspace", None))
    # retranslateUi

