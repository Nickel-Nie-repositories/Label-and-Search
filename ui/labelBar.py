# # -*- coding: utf-8 -*-
#
# ################################################################################
# ## Form generated from reading UI file 'labelBar.ui'
# ##
# ## Created by: Qt User Interface Compiler version 5.15.2
# ##
# ## WARNING! All changes made in this file will be lost when recompiling UI file!
# ################################################################################
#
# from PySide2.QtCore import *
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
#
#
# class Ui_labelBar(object):
#     def setupUi(self, labelBar):
#         if not labelBar.objectName():
#             labelBar.setObjectName(u"labelBar")
#         labelBar.resize(400, 50)
#         sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(labelBar.sizePolicy().hasHeightForWidth())
#         labelBar.setSizePolicy(sizePolicy)
#         self.widget_layout = QHBoxLayout(labelBar)
#         self.widget_layout.setObjectName(u"widget_layout")
#         self.widget_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
#         self.lineEdit = QLineEdit(labelBar)
#         self.lineEdit.setObjectName(u"lineEdit")
#         sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
#         sizePolicy1.setHorizontalStretch(3)
#         sizePolicy1.setVerticalStretch(0)
#         sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
#         self.lineEdit.setSizePolicy(sizePolicy1)
#
#         self.widget_layout.addWidget(self.lineEdit)
#
#         self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
#
#         self.widget_layout.addItem(self.horizontalSpacer_2)
#
#         self.button_modify = QPushButton(labelBar)
#         self.button_modify.setObjectName(u"button_modify")
#         sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
#         sizePolicy2.setHorizontalStretch(1)
#         sizePolicy2.setVerticalStretch(0)
#         sizePolicy2.setHeightForWidth(self.button_modify.sizePolicy().hasHeightForWidth())
#         self.button_modify.setSizePolicy(sizePolicy2)
#         self.button_modify.setMinimumSize(QSize(10, 10))
#         self.button_modify.setMaximumSize(QSize(40, 40))
#         self.button_modify.setIconSize(QSize(20, 20))
#
#         self.widget_layout.addWidget(self.button_modify)
#
#         self.button_delete = QPushButton(labelBar)
#         self.button_delete.setObjectName(u"button_delete")
#         sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
#         sizePolicy3.setHorizontalStretch(1)
#         sizePolicy3.setVerticalStretch(0)
#         sizePolicy3.setHeightForWidth(self.button_delete.sizePolicy().hasHeightForWidth())
#         self.button_delete.setSizePolicy(sizePolicy3)
#         self.button_delete.setMinimumSize(QSize(10, 10))
#         self.button_delete.setMaximumSize(QSize(40, 40))
#         self.button_delete.setSizeIncrement(QSize(0, 0))
#         self.button_delete.setIconSize(QSize(10, 10))
#         self.button_delete.setAutoRepeat(False)
#         self.button_delete.setAutoExclusive(False)
#         self.button_delete.setAutoRepeatDelay(300)
#         self.button_delete.setFlat(False)
#
#         self.widget_layout.addWidget(self.button_delete)
#
#         self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
#
#         self.widget_layout.addItem(self.horizontalSpacer)
#
#         self.keySequenceEdit = QKeySequenceEdit(labelBar)
#         self.keySequenceEdit.setObjectName(u"keySequenceEdit")
#         sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#         sizePolicy4.setHorizontalStretch(1)
#         sizePolicy4.setVerticalStretch(0)
#         sizePolicy4.setHeightForWidth(self.keySequenceEdit.sizePolicy().hasHeightForWidth())
#         self.keySequenceEdit.setSizePolicy(sizePolicy4)
#
#         self.widget_layout.addWidget(self.keySequenceEdit)
#
#         self.retranslateUi(labelBar)
#
#         QMetaObject.connectSlotsByName(labelBar)
#
#     # setupUi
#
#     def retranslateUi(self, labelBar):
#         labelBar.setWindowTitle(QCoreApplication.translate("labelBar", u"Form", None))
#         self.button_modify.setText(QCoreApplication.translate("labelBar", u"\u4fee\u6539", None))
#         self.button_delete.setText(QCoreApplication.translate("labelBar", u"\u5220\u9664", None))
#     # retranslateUi
