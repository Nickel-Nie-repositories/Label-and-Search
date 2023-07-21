import imghdr
import os
import ast
import time
from math import floor
from threading import Thread
from typing import TextIO

from PySide2.QtCore import QSize, Signal, QThread, QObject, Qt
from PySide2.QtWidgets import QFileSystemModel, QFileDialog, QListWidgetItem, QDockWidget, QInputDialog, QLineEdit, \
    QMessageBox, QTreeView, QTextEdit, QPushButton, QKeySequenceEdit, QShortcut, QLabel, QListWidget, QListView, QAction
from PySide2.QtUiTools import QUiLoader
import PySide2.QtGui as QtGui

# from mytools.stop_thread import stop_thread
from mytools.File_Operation import *
from mytools.import_function import import_function
from mytools.reconnect_signal import *

from ui_widgets.ImageViewer import ImageViewer
from ui_widgets.LabelBar import LabelBar, CustomKeySequenceEdit
from ui_widgets.StartLabelBar import StartLabelBar
from ui_widgets.ProgressBarWindow import ProgressBarWindow, CurrentProgressSignal
from ui_widgets.shortcut_setting import ShortcutDialog

imgType_list = {'jpg', 'bmp', 'png', 'jpeg', 'jfif'}


class CustomSignal(QObject):
    statistics_end_signal = Signal(str)
    search_signal = Signal(str)


class MainWindow:

    def __init__(self):

        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        self.ui = QUiLoader().load('ui/main_window.ui')

        # 一些自定义配置项：
        self.separator = ";"  # 自定义Label格式的分割符号
        # 自定义一些按钮的快捷键：
        self.button_next_shortcut = Qt.Key_Space
        self.button_fix_to_view_shortcut = Qt.Key_0
        self.button_last_shortcut = Qt.Key_Left
        self.button_backspace_shortcut = Qt.Key_Backspace
        # 自定义搜索结果缩略图的大小：
        self.thumb_image_height = 200
        self.thumb_image_width = 200
        # 设置快捷键的时候要考虑两件事：
        # 1.如果这个快捷键正在被其他按钮使用，要将原先的按钮解绑
        # 2.如果这个快捷键正显示在其他的KeyEdit中，要将原先的KeyEdit清空
        # 所以要准备两个字典：
        self.dict_button = {}  # 快捷键id：button对象
        self.dict_keyEdit = {}  # 快捷键id：keyEdit对象
        self.dict_QShortcut = {}  # 快捷键id：QShortcut对象

        self.setShortcut_safely(self.button_fix_to_view_shortcut, self.ui.button_fix_to_view)
        # self.ui.button_fix_to_view.setShortcut(QtGui.QKeySequence(self.button_fix_to_view_shortcut))
        # temp_shortcut = QShortcut(QtGui.QKeySequence(self.button_fix_to_view_shortcut), self.ui)
        # temp_shortcut.activated.connect(self.test_slot_function)
        # temp_shortcut2 = QShortcut(QtGui.QKeySequence(self.button_fix_to_view_shortcut), self.ui)
        # temp_shortcut2.activated.connect(self.handle_button_fix_to_view)
        self.setShortcut_safely(self.button_last_shortcut, self.ui.button_last)
        self.setShortcut_safely(self.button_next_shortcut, self.ui.button_next)
        self.setShortcut_safely(self.button_backspace_shortcut, self.ui.button_backspace)

        # 设置中间的图片查看器：
        self.imageViewer = ImageViewer()
        # self.imageViewer = ImageViewer(self.ui.frame_mid_layout)
        self.ui.frame_mid_layout.addWidget(self.imageViewer)
        self.imageViewer.finish_Draw_rect.connect(self.handle_finish_Draw_rect)
        self.imageViewer.finish_Draw_Point.connect(self.handle_fine_Draw_Point)

        # 左侧文件目录栏的显示：
        # self.current_path = "D:/"
        self.current_path = r"D:\PythonProject\Label_and_Search\test_images"
        self.model = QFileSystemModel()
        # model.setRootPath(QDir.currentPath())
        self.model.setRootPath(self.current_path)
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(self.model.index(self.current_path))
        self.ui.treeView.doubleClicked.connect(self.handle_click_treeView)

        # 设置当前文件：
        self.current_file = None
        self.current_index = 0

        # 当前Label_save文件：
        self.current_label_name = "labels"
        self.current_label_file = None

        # 左右两侧停靠栏的显示动作，加入菜单栏：
        self.ui.menu_window.addAction(self.ui.dockWidget_right.toggleViewAction())
        self.ui.menu_window.addAction(self.ui.dockWidget_left.toggleViewAction())

        # 菜单各项绑定处理函数：
        self.ui.action_open_path.triggered.connect(self.handle_open_dir)
        self.ui.action_create_label.triggered.connect(self.handle_create_label)
        self.ui.action_update_label.triggered.connect(self.handle_update_label)
        self.ui.action_open_label.triggered.connect(self.handle_open_label)
        self.ui.action_locate_label.triggered.connect(self.handle_locate_label)
        self.ui.action_import_label_func.triggered.connect(self.handle_action_import_label_func)

        # 中下方工具栏绑定处理函数：
        self.ui.button_fix_to_view.clicked.connect(self.handle_button_fix_to_view)
        self.ui.button_last.clicked.connect(self.handle_button_last)
        self.ui.button_next.clicked.connect(self.handle_button_next)
        self.ui.button_point.clicked.connect(self.handle_button_point)
        self.ui.button_rect.clicked.connect(self.handle_button_rect)

        # 右下方label列表的处理：
        self.list_num = 0
        # 加入最底下新建的那一行。
        item = QListWidgetItem()
        item.setSizeHint(QSize(400, 50))
        widget = StartLabelBar()
        self.ui.listWidget.addItem(item)
        self.ui.listWidget.setItemWidget(item, widget)
        # 将新建按钮和添加一行的处理绑定：
        widget.button_add.clicked.connect(self.add_listWidget_item)

        # 进度条弹窗：
        self.threadFlag = 0  # 用于控制线程中断。
        self.progress_window = ProgressBarWindow()  # 进度条窗口。
        # self.current_progress_signal = Signal(int, str)  # 信号：用于异步线程向小弹窗发送信号。
        self.current_progress_signal = CurrentProgressSignal()  # 信号：用于异步线程向小弹窗发送信号。
        self.current_progress_signal.current_progress_signal.connect(
            self.progress_window.handle_current_progress_signal)  # 信号绑定
        self.customSignal = CustomSignal()
        self.customSignal.statistics_end_signal.connect(self.handle_statistics_end_signal)
        self.counter = 0

        # 右上方文本框：
        self.ui.textEdit.setText("暂无Label文件...")
        self.ui.textEdit.setReadOnly(True)
        self.ui.button_backspace.clicked.connect(self.handle_button_backspace)

        # 设置分割符绑定函数：
        self.ui.action_setSeparator.triggered.connect(self.handle_action_setSeparator)

        # 设置快捷键绑定函数：
        self.ui.action_setShortcut.triggered.connect(self.handle_action_setShortcut)

        # 绑定两个添加标签项的动作：
        self.ui.action_add_point_label.triggered.connect(self.handle_action_add_point_label)
        self.ui.action_add_rect_label.triggered.connect(self.handle_action_add_rect_label)

        # 自动打标函数的列表：
        self.label_func_list = []
        self.ui.function_list.itemDoubleClicked.connect(self.handle_label_func_list_double_click)

        # 搜索板块的初始化设置：
        self.ui.search_result.setViewMode(QListView.ViewMode.IconMode)
        self.ui.search_result.setIconSize(QSize(self.thumb_image_width, self.thumb_image_height))
        self.ui.search_result.setSpacing(10)
        # self.add_into_searchResult(r"D:\PythonProject\Label_and_Search\test.png")
        self.ui.search_button.clicked.connect(self.handle_search_button)
        self.customSignal.search_signal.connect(self.handle_search_signal)
        # 模糊搜索开关:
        self.fuzzy_search = False
        self.ui.fuzzy_search.triggered.connect(self.handle_fuzzy_search)

    # 处理：进度条弹窗：取消：
    def handle_button_close(self, thread: Thread):
        # stop_thread(thread)
        self.threadFlag = 0
        self.counter = 0
        self.progress_window.close()

    # 处理：菜单 → 文件 → 打开文件夹
    def handle_open_dir(self):
        # 先打开文件目录，以询问用户打开的文件路径
        filePath = QFileDialog.getExistingDirectory(self.ui, "选择打开路径")
        # 如果路径不为空，更改 当前访问的路径
        if filePath != "":
            self.current_path = filePath
            self.model.setRootPath(self.current_path)
            self.ui.treeView.setRootIndex(self.model.index(self.current_path))
            if os.path.exists(os.path.join(self.current_path, self.current_label_name + ".txt")):
                reply = QMessageBox.question(self.ui, "问问：", f"当前目录下搜索到文件：{self.current_label_name}.txt ,\n"
                                                             f"是否将作为label文件？", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.current_label_file = os.path.join(self.current_path, self.current_label_name + ".txt")
                    self.ui.textEdit.setText("")
                    self.ui.treeView.setCurrentIndex(self.model.index(self.current_label_file))
                    QMessageBox.information(self.ui, "消息", f"已设置当前Label文件：{self.current_label_file}", QMessageBox.Yes)
                    self.start()

    # 处理：异步统计结束信号(就是先异步统计文件，结束后的后续操作)：
    def handle_statistics_end_signal(self, message: str):
        if message == "新建前统计完成":
            self.progress_window.close()
            if self.counter >= 10000:
                value = QMessageBox.question(self.ui, "选择：",
                                             f"当前目录下统计的文件数量为：{self.counter}\n"
                                             f"（我们认为该目录: {self.current_path} 过于庞大，可能不是你需要的，建议重新选择目录）\n"
                                             f"是否执意要继续:", QMessageBox.Yes | QMessageBox.No)
            else:
                value = QMessageBox.question(self.ui, "选择：",
                                             f"当前目录下统计的文件数量为：{self.counter}\n"
                                             f"当前目录为：{self.current_path} \n"
                                             f"请确认目录无误后继续:", QMessageBox.Yes | QMessageBox.No)
            if value != QMessageBox.Yes:
                return
            else:
                # 询问用户新建Label文件名。
                Loop = True
                while Loop:
                    value, ok = QInputDialog.getText(self.ui, "输入框", "新建Label文件\n\n请输入文件名:", QLineEdit.Normal, "labels")
                    if not ok:
                        return
                    if os.path.exists(os.path.join(self.current_path, value + ".txt")):
                        reply = QMessageBox.warning(self.ui, "警告", "该文件已存在, 请重新输入", QMessageBox.Yes)
                        if reply == QMessageBox.Yes:
                            Loop = True
                    else:
                        Loop = False
                        self.current_label_name = value
                self.progress_window.show()
                # 这里再启动了一个进度条窗口，现在开始正式生成label文件。
                self.progress_window.label_title.setText("正在生成Label：")
                temp_path = os.path.join(self.current_path, self.current_label_name + ".txt")

                # label_file = open(temp_path, "w")

                # 写一个异步函数，以当前目录生成label文件：
                def gen_label_file(_label_file_path: str):
                    _label_file = open(_label_file_path, "w")
                    for root, dirs, files in os.walk(self.current_path):  # 遍历统计
                        if self.threadFlag == 0:
                            _label_file.close()
                            os.remove(_label_file_path)
                            return
                        for index, file in enumerate(files):
                            if os.path.isfile(os.path.join(root, file)):
                                if imghdr.what(os.path.join(root, file)) in imgType_list:
                                    _label_file.write(os.path.join(root, file).
                                                      replace(self.current_path, "", 1)[1:] + "\t\n")
                                    self.current_progress_signal.current_progress_signal.emit(
                                        int(index * 100 / len(files)), os.path.join(root, file))
                    # 创建完再发一个信息。
                    self.customSignal.statistics_end_signal.emit("新建label文件完成")
                    self.current_label_file = temp_path
                    _label_file.close()

                tempThread = Thread(target=gen_label_file, args=(temp_path,))
                self.progress_window.button_close.clicked.connect(
                    lambda: self.handle_button_close(tempThread))
                self.threadFlag = 1
                tempThread.start()
        elif message == "新建label文件完成":
            self.progress_window.close()
            self.ui.textEdit.setText("")
            QMessageBox.information(self.ui, "消息", f"创建label文件成功：\n{self.current_label_file}")
            self.start()
        elif message == "打标完成":
            self.progress_window.close()
            QMessageBox.information(self.ui, "消息", f"打标完成：\n{self.current_label_file}")

    # 处理：菜单 → 文件 → 新建label文件
    def handle_create_label(self):
        # 打开一个进度条窗：
        self.progress_window.show()
        self.progress_window.label_title.setText("正在统计文件：")
        self.counter = 0

        # 开一个线程统计当前文件夹下的文件个数：
        def statistic():
            for index, (root, dirs, files) in enumerate(os.walk(self.current_path)):  # 遍历统计
                if self.threadFlag == 0:
                    return
                self.counter += len(files)  # 统计文件夹下文件个数
                # self.progress_window.signal.current_progress_signal.emit(root, index % 100)
                self.current_progress_signal.current_progress_signal.emit(index % 100, root)
                # time.sleep(0.1)
            # 统计结束后的工作：
            # 向主线程发送信号。
            self.customSignal.statistics_end_signal.emit("新建前统计完成")

        tempThread = Thread(target=statistic)
        self.progress_window.button_close.clicked.connect(lambda: self.handle_button_close(tempThread))
        self.threadFlag = 1
        tempThread.start()

    # 处理：菜单 → 文件 → 更新label文件
    def handle_update_label(self):
        # 遍历整个当前目录，移动原来文件文件的对应行到新文件，创建新行。。。
        pass

    # 处理：菜单 → 文件 → 打开label文件
    def handle_open_label(self):
        file_, filetype = QFileDialog.getOpenFileName(self.ui, "选择label文件", self.current_path,
                                                      "All Files (*);;Text Files (*.txt)")
        if file_.endswith(".txt"):
            self.current_label_file = file_
            self.ui.textEdit.setText("")
            self.ui.treeView.setCurrentIndex(self.model.index(file_))
            QMessageBox.information(self.ui, "消息", f"已设置当前Label文件：{self.current_label_file}", QMessageBox.Yes)
            self.start()

    # 处理：菜单 → 文件 → 定位到label文件
    def handle_locate_label(self):
        if self.current_label_file is None:
            QMessageBox.warning(self.ui, "警告", "你还未设置Label文件，请打开或新建！ ", QMessageBox.Yes)
        elif os.path.exists(self.current_label_file):
            self.ui.treeView.setCurrentIndex(self.model.index(self.current_label_file))
        else:
            QMessageBox.warning(self.ui, "警告", f"文件 {self.current_label_file} 不存在！ ", QMessageBox.Yes)

    # 为 imageView 设置图片。
    def set_Image(self, imgName):
        # jpg = QtGui.QPixmap(imgName).scaled(self.ui.showImage.width(), self.ui.showImage.height())
        # 这里应该自适应初始大小。
        jpg = QtGui.QPixmap(imgName)
        # self.ui.showImage.setPixmap(jpg)
        self.imageViewer.setImage(imgName)
        self.redraw_graphics_on_imageView()

    # 处理：点击文件目录事件
    def handle_click_treeView(self):
        file_index = self.ui.treeView.currentIndex()
        file = self.model.filePath(file_index)
        if self.current_label_file is None:
            # if file.endswith(".jpg"):
            if os.path.isfile(file):
                if imghdr.what(file) in imgType_list:
                    self.current_file = file
                    self.set_Image(file)
        else:
            # self.locate_to_file(file=file)  # 奇怪的事情，这里的文件目录的path 偏偏用的/ 而os.path 用的\
            # self.locate_to_file(file=file.replace("/", "\\"))
            self.locate_to_file(file=os.path.normpath(file))

    # 处理：图片适应屏幕 按钮
    def handle_button_fix_to_view(self):
        self.imageViewer.fitInView(self.imageViewer.pixmapItem)

    # 处理：上一张图片 按钮
    def handle_button_last(self):
        # 在生成的记录label的txt上取url
        # 然后更改各个当前状态值
        if self.current_label_file is not None:
            if not self.locate_to_file(index=self.current_index - 1):
                QMessageBox.warning(self.ui, "提示", "没有更多的图片了。", QMessageBox.Yes)

    # 处理：下一张图片 按钮
    def handle_button_next(self):
        # 同上
        if self.current_label_file is not None:
            if not self.locate_to_file(index=self.current_index + 1):
                QMessageBox.warning(self.ui, "提示", "没有更多的图片了。", QMessageBox.Yes)

    # 处理：绘制点 按钮
    def handle_button_point(self):
        self.imageViewer.StartDrawPoint()

    # 处理: 绘制矩形 按钮
    def handle_button_rect(self):
        self.imageViewer.StartDrawRect()

    # 操作：添加label list中的一行
    def add_listWidget_item(self):
        item = QListWidgetItem()  # 创建QListWidgetItem对象
        item.setSizeHint(QSize(400, 50))  # 设置QListWidgetItem大小
        widget = LabelBar()  # 调用上面的函数获取对应
        # self.ui.listWidget.addItem(item)  # 添加item
        self.ui.listWidget.insertItem(self.list_num, item)
        self.ui.listWidget.setItemWidget(item, widget)  # 为item设置widget
        self.list_num += 1
        # 绑定其中按钮的事件处理：
        widget.button_delete.clicked.connect(lambda: self.delete_listWidget_item(item))
        widget.button_label.clicked.connect(lambda: self.handle_button_label(widget))
        # 绑定快捷键指定框的完成事件：即安全地替换快捷键：
        # widget.keySequenceEdit.editingFinished.connect(lambda: self.setShortcut_safely(
        #     widget.keySequenceEdit.keySequence()[0],
        #     widget.button_label,
        #     widget.keySequenceEdit
        # ))
        # widget.keySequenceEdit.keySequenceChanged.connect(lambda: self.setShortcut_safely(
        #     widget.keySequenceEdit.keySequence()[0],
        #     widget.button_label,
        #     widget.keySequenceEdit
        # ))
        # 这里有一个问题，我们为按钮设置快捷键，但是 为hide的按钮设置快捷键会导致快捷键不起作用，
        # 此外，如果为在场的按钮设置了快捷键，然后，那个按钮hide再show，快捷键也会失效。
        # 原因暂时未知。
        # 所以考虑：快捷键不对按钮绑定，而是快捷键和按钮一样对处理函数绑定。
        widget.keySequenceEdit.editingFinished.connect(lambda: self.setShortcut_safely(
            widget.keySequenceEdit.keySequence()[0],
            None,
            widget.keySequenceEdit,
            lambda: self.handle_button_label(widget)
        ))

    # 操作：删除label list 中的一行，输入为item。
    def delete_listWidget_item(self, item):
        self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
        self.list_num -= 1

    # 操作：label自身的点击事件：
    def handle_button_label(self, widget):
        # print("label按钮调用：", widget.button_label.text())
        if self.current_label_file is not None:
            text = widget.button_label.text()
            # 首先要将内容加进右上文本框：
            self.append_on_textEdit(text + self.separator)
            # 然后要将文本框的内容整行写回文件：
            self.write_back()

    # 在已有label_file的前提下，定位到文件：file
    def locate_to_file(self, file=None, index=0):
        if file is not None:
            if os.path.isfile(file):
                if imghdr.what(file) in imgType_list:
                    self.current_file = file
                    self.ui.treeView.setCurrentIndex(self.model.index(file))
                    line, _index = get_line_by_filename(self.current_label_file, file)  # 暂时写成同步。
                    self.ui.textEdit.setText(line[:-1])
                    self.set_Image(file)
                    if _index == -1:
                        QMessageBox.warning(self.ui, "提示", "当前文件未在label文件中找到，建议更新label文件。", QMessageBox.Yes)
                        return False
                    else:
                        self.current_index = _index
                        return True
            return False
        else:
            line = get_line_by_index(self.current_label_file, index)
            self.ui.textEdit.setText(line[:-1])
            file = line.split("\t")[0]
            if file == "":
                return False
            else:
                file = os.path.join(self.current_path, file)
                if os.path.isfile(file):
                    if imghdr.what(file) in imgType_list:
                        self.current_file = file
                        self.current_index = index
                        self.set_Image(file)
                        self.ui.treeView.setCurrentIndex(self.model.index(self.current_file))
                        return True
                return False

    # 定位到当前label_file 指示的第一个文件。
    def start(self):
        self.locate_to_file(index=0)

    # 向文字追加到右上方的文本框中
    def append_on_textEdit(self, text: str):
        # self.ui.textEdit.append(text)
        textCursor = self.ui.textEdit.textCursor()
        textCursor.movePosition(QtGui.QTextCursor.End)
        textCursor.insertText(text)

    # 将文本框中的文字写回到label文件中
    def write_back(self):
        if os.path.exists(self.current_label_file):
            write_line_by_index(self.current_label_file, self.current_index
                                , self.ui.textEdit.toPlainText())

    # 处理：文本框下退格按钮：
    def handle_button_backspace(self):
        if self.current_label_file is not None:
            new_text, pop_label = backspace_label(self.ui.textEdit.toPlainText(), self.separator)
            if is_coordinate(pop_label):
                self.imageViewer.pop_graphics(pop_label)
            self.ui.textEdit.setText(new_text)
            self.write_back()

    # 处理：菜单 → 编辑 → 设置分割符：
    def handle_action_setSeparator(self):
        value, ok = QInputDialog.getText(self.ui, "输入框", "设置分割符：\n\n请输入分割符：", QLineEdit.Normal, self.separator)
        if ok:
            self.separator = value

    # 处理：菜单 → 编辑 → 设置快捷键：
    def handle_action_setShortcut(self):
        tempDialog = ShortcutDialog()
        if not self.ui.button_fix_to_view.shortcut().isEmpty():
            self.button_fix_to_view_shortcut = self.ui.button_fix_to_view.shortcut()[0]
        else:
            self.button_fix_to_view_shortcut = 0
        if not self.ui.button_last.shortcut().isEmpty():
            self.button_last_shortcut = self.ui.button_last.shortcut()[0]
        else:
            self.button_last_shortcut = 0
        if not self.ui.button_next.shortcut().isEmpty():
            self.button_next_shortcut = self.ui.button_next.shortcut()[0]
        else:
            self.button_next_shortcut = 0
        if not self.ui.button_backspace.shortcut().isEmpty():
            self.button_backspace_shortcut = self.ui.button_backspace.shortcut()[0]
        else:
            self.button_backspace_shortcut = 0
        tempDialog.keySequenceEdit.setKeySequence(QtGui.QKeySequence(self.button_fix_to_view_shortcut))
        tempDialog.keySequenceEdit_2.setKeySequence(QtGui.QKeySequence(self.button_last_shortcut))
        tempDialog.keySequenceEdit_3.setKeySequence(QtGui.QKeySequence(self.button_next_shortcut))
        tempDialog.keySequenceEdit_4.setKeySequence(QtGui.QKeySequence(self.button_backspace_shortcut))
        if tempDialog.exec_():
            if not tempDialog.get_data()[0].isEmpty():
                self.setShortcut_safely(tempDialog.get_data()[0][0], self.ui.button_fix_to_view)
            if not tempDialog.get_data()[1].isEmpty():
                self.setShortcut_safely(tempDialog.get_data()[1][0], self.ui.button_last)
            if not tempDialog.get_data()[2].isEmpty():
                self.setShortcut_safely(tempDialog.get_data()[2][0], self.ui.button_next)
            if not tempDialog.get_data()[3].isEmpty():
                self.setShortcut_safely(tempDialog.get_data()[3][0], self.ui.button_backspace)
            if not self.ui.button_fix_to_view.shortcut().isEmpty():
                self.button_fix_to_view_shortcut = self.ui.button_fix_to_view.shortcut()[0]
            else:
                self.button_fix_to_view_shortcut = 0
            if not self.ui.button_last.shortcut().isEmpty():
                self.button_last_shortcut = self.ui.button_last.shortcut()[0]
            else:
                self.button_last_shortcut = 0
            if not self.ui.button_next.shortcut().isEmpty():
                self.button_next_shortcut = self.ui.button_next.shortcut()[0]
            else:
                self.button_next_shortcut = 0
            if not self.ui.button_backspace.shortcut().isEmpty():
                self.button_backspace_shortcut = self.ui.button_backspace.shortcut()[0]
            else:
                self.button_backspace_shortcut = 0

    # 处理：标签 >> 添加“点”标签：
    def handle_action_add_point_label(self):
        # 需要向标签栏添加一个标签行，然后更改它的一些内容
        item = QListWidgetItem()  # 创建QListWidgetItem对象
        item.setSizeHint(QSize(400, 50))  # 设置QListWidgetItem大小
        widget = LabelBar()  # 调用上面的函数获取对应
        # 首先，这个标签行不能有编辑按钮：
        widget.button_modify.hide()
        # 然后，这个标签行不需要文本框，就是先让文本框形式结束，然后更改它按钮的文本：
        widget.finish_lineEdit()
        widget.button_label.setText("●")
        self.ui.listWidget.insertItem(self.list_num, item)
        self.ui.listWidget.setItemWidget(item, widget)  # 为item设置widget
        self.list_num += 1
        # 绑定其中按钮的事件处理(删除事件不变，label的点击事件变为开始绘制点的函数)
        widget.button_delete.clicked.connect(lambda: self.delete_listWidget_item(item))
        widget.button_label.clicked.connect(self.handle_button_point)
        widget.keySequenceEdit.editingFinished.connect(lambda: self.setShortcut_safely(
            widget.keySequenceEdit.keySequence()[0],
            None,
            widget.keySequenceEdit,
            self.handle_button_point
        ))

    # 处理：标签 >> 添加“矩形”标签：同理。
    def handle_action_add_rect_label(self):
        # 需要向标签栏添加一个标签行，然后更改它的一些内容
        item = QListWidgetItem()  # 创建QListWidgetItem对象
        item.setSizeHint(QSize(400, 50))  # 设置QListWidgetItem大小
        widget = LabelBar()  # 调用上面的函数获取对应
        # 首先，这个标签行不能有编辑按钮：
        widget.button_modify.hide()
        # 然后，这个标签行不需要文本框，就是先让文本框形式结束，然后更改它按钮的文本：
        widget.finish_lineEdit()
        widget.button_label.setText("▃▃")
        self.ui.listWidget.insertItem(self.list_num, item)
        self.ui.listWidget.setItemWidget(item, widget)  # 为item设置widget
        self.list_num += 1
        # 绑定其中按钮的事件处理(删除事件不变，label的点击事件变为开始绘制点的函数)
        widget.button_delete.clicked.connect(lambda: self.delete_listWidget_item(item))
        widget.button_label.clicked.connect(self.handle_button_rect)
        widget.keySequenceEdit.editingFinished.connect(lambda: self.setShortcut_safely(
            widget.keySequenceEdit.keySequence()[0],
            None,
            widget.keySequenceEdit,
            self.handle_button_rect
        ))

    # 处理：来自ImageView 的 finish_Draw_rect 信号。
    def handle_finish_Draw_rect(self, x1: float, y1: float, x2: float, y2: float):
        if self.current_label_file is not None:
            # 先生成字符串：
            coordinate_text = "(%.6f,%.6f,%.6f,%.6f)" % (x1, y1, x2, y2)
            # 然后写入
            self.append_on_textEdit(coordinate_text + self.separator)
            self.write_back()

    # 处理：来自ImageView 的 finish_Draw_Point 信号。
    def handle_fine_Draw_Point(self, x: float, y: float):
        # 同上。
        if self.current_label_file is not None:
            coordinate_text = "(%.6f,%.6f)" % (x, y)
            self.append_on_textEdit(coordinate_text + self.separator)
            self.write_back()

    def redraw_graphics_on_imageView(self):
        if self.current_label_file is not None:
            text = self.ui.textEdit.toPlainText()
            labels_list = text.split("\t", 1)[1].split(self.separator)[:-1]
            for label in labels_list:
                if is_coordinate(label):
                    self.imageViewer.redraw(label)

    # 这个函数单纯用于测试信号与槽的绑定和解绑
    def test_slot_function(self):
        print("test: ", self.ui.objectName())

    # 测试结果为：一个信号可以绑定多个处理函数，他们按次序执行。
    # 信号与处理函数解绑需要用到disconnect，它也需要输入一个函数签名。

    # 要安全的绑定快捷键，定义方法：
    def setShortcut_safely(self, shortcut, button=None, keyEdit: CustomKeySequenceEdit = None, button_function=None):
        """
        更新这个方法，因为需要同时处理 绑定按钮或直接绑定按钮的处理函数。
        基本逻辑为：如果快捷键需要绑定按钮：
            1.如果该按钮被绑定过，正常进行，即覆盖
            2.如果该快捷键正在被绑定为其他按钮的快捷键，查表获得这个前按钮，将那个按钮的快捷键设为0
            3.如果该快捷键正在显示在某个keyEdit框中，将那个框的内容清楚（先清除后写，这样能保证在一个框中重复填写时不出错）
            4.要填入字典，指示这个快捷键正在绑定哪个按钮，正在显示在哪个keyEdit框。
        如果快捷键需要绑定处理函数：
            1.如果这个快捷键此前绑定过函数，需要解绑。（这个过程不需要查表，直接解绑全部即可）
            2.然后将这个快捷键绑定到参数给定的函数。
            ↑ 实现了一个安全替换快捷键绑定函数的方法。
        更新后：这里出现了新的问题。
        一旦一个快捷键被设置两次，那么它将不再有效。
        经测试发现： 如果一个快捷键绑定了一个按钮 并同时存在一个QShortcut对象，那么两个都不起作用。
        如果一个按钮同时存在两个QShortcut对象，那么两个都不起作用。
        因此，这里应该修改为：
            1.建一张 快捷键与QShortcut对象 的字典，如果已经新建过对象则不再新建。
            2.如果本次操作是将快捷键绑定至按钮，则应当直接删除之前的QShortcut对象。
        :param shortcut: 可能是int 也可能是Key枚举类型。
        :param button: 应为QPushButton类型，可以不传，不传视为将快捷键绑定方法。
        :param keyEdit: 应为QKeySequenceEdit类型
        :param button_function: 函数签名
        :return: void
        """
        # print("绑定调用：\n\t", shortcut, "\n\t", button, "\n\t", keyEdit, "\n\t", button_function)
        # 判断那两个字典中这个快捷键是否存在：
        if int(shortcut) in self.dict_button.keys():
            # 如果此前绑定过按钮，将那个按钮的快捷键设置为0：
            if self.dict_button[int(shortcut)] is not None:
                self.dict_button[int(shortcut)].setShortcut(QtGui.QKeySequence(0))
        if int(shortcut) in self.dict_keyEdit.keys():
            # 如果有keyEdit正在显示这个shortcut，将它清除：
            if self.dict_keyEdit[int(shortcut)] is not None:
                self.dict_keyEdit[int(shortcut)].clear()

        # 如果shortcut此前被绑定了某个函数，解绑：
        # shortcut_obj = QShortcut(QtGui.QKeySequence(shortcut), self.ui)
        # reconnect(shortcut_obj.activated, None, None)

        # 然后直接设置快捷键：
        if button is not None:
            # 本次操作是绑定按钮：
            # 如果快捷键有一个QShortcut对象：删除那个对象：
            if int(shortcut) in self.dict_QShortcut.keys():
                if self.dict_QShortcut[int(shortcut)] is not None:
                    reconnect(self.dict_QShortcut[int(shortcut)].activated, None, None)
                    # self.ui.layout().removeWidget(self.dict_QShortcut[int(shortcut)])
                    self.ui.releaseShortcut(self.dict_QShortcut[int(shortcut)].id())
                    self.dict_QShortcut[int(shortcut)].deleteLater()
                    self.dict_QShortcut[int(shortcut)] = None
            # print("绑定：", shortcut_obj.activated, button)
            button.setShortcut(QtGui.QKeySequence(shortcut))
        elif button_function is not None:
            # 本次操作是绑定函数:
            # 获取原本的QShortcut对象，如果不存在，则应创建：
            shortcut_obj = self.dict_QShortcut.get(int(shortcut), None)
            if shortcut_obj is None:
                shortcut_obj = QShortcut(QtGui.QKeySequence(shortcut), self.ui)
                self.dict_QShortcut[int(shortcut)] = shortcut_obj
            reconnect(shortcut_obj.activated, button_function, None)
            # shortcut_obj.activated.connect(button_function)
        if keyEdit is not None:
            keyEdit.setKeySequence(QtGui.QKeySequence(shortcut))

        # 将现在的状态写进字典：
        self.dict_button[int(shortcut)] = button
        self.dict_keyEdit[int(shortcut)] = keyEdit
        # print("/////////////////////////////////////////////////////////////////////////////////////////////////////")

    # 导入label函数的函数，为自动打标做准备。
    def handle_action_import_label_func(self):
        # 首先，弹出文件选择框让用户选择.py文件：
        source_path, filetype = QFileDialog.getOpenFileName(self.ui, "选择label函数源码文件", self.current_path,
                                                            "All Files (*);;Text Files (*.txt);;Python Files (*.py)")

        # QMessageBox.critical(self.ui, "等待...", "正在从外部文件加载函数，请等待...", QMessageBox.NoButton)
        msgBox = QMessageBox(self.ui)
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setWindowTitle("正在从外部文件加载函数，请等待...")
        msgBox.show()

        names, funcs = import_function(source_path)  # 这是一个耗时操作，考虑异步进行。
        # print(names, funcs)

        msgBox.close()

        # 对于所有被检索出来的函数：
        for fun_name in names:
            # 将函数名作为一个项放入ui的列表
            self.ui.function_list.addItem(fun_name)
        # 同时将函数对象存入内存的列表
        self.label_func_list += funcs

        # 把tag_bar的状态以到二页：
        self.ui.tabWidget_2.setCurrentIndex(1)

    # 处理label函数列表中列表项的点击事件
    def handle_label_func_list_double_click(self, item):
        # print(item.text() + "被点击了")
        # 先打开一个消息框通知用户确认
        reply = QMessageBox.question(self.ui, "问问：", f"即将使用函数：{item.text()} 进行打标，"
                                                     f"这个过程将会改变label文件中的每一行，请问是否继续？", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        # 打开一个进度条窗：
        if self.current_label_file is None or not os.path.exists(self.current_label_file):
            QMessageBox.warning(self.ui, "提示", "当前的label文件未设置或不存在，请指定label文件", QMessageBox.Yes)
            return
        self.progress_window.show()
        self.progress_window.label_title.setText("正在自动打标：")
        output_lines = []

        def put_on_labels():
            with open(self.current_label_file, "r") as f:
                length = len(f.readlines())
            with open(self.current_label_file, "r") as f:
                for index, line in enumerate(f.readlines()):
                    if self.threadFlag == 0:
                        return
                    image = os.path.join(self.current_path, line.split("\t")[0])
                    label = self.label_func_list[self.ui.function_list.row(item)](image)
                    output_lines.append(line[:-1] + label + self.separator + "\n")
                    self.current_progress_signal.current_progress_signal.emit(floor(index * 100 / length), image)
            with open(self.current_label_file, 'w') as f:
                f.writelines(output_lines)
            self.customSignal.statistics_end_signal.emit("打标完成")

        # 启动进程：
        tempThread = Thread(target=put_on_labels)
        self.progress_window.button_close.clicked.connect(lambda: self.handle_button_close(tempThread))
        self.threadFlag = 1
        tempThread.start()

    # 向搜索结果的 list_widget 中添加缩略图项。
    def add_into_searchResult(self, filePath):
        imageItem = QListWidgetItem()
        imageItem.setIcon(QtGui.QIcon(filePath))
        imageItem.setText(filePath)
        imageItem.setSizeHint(QSize(self.thumb_image_width, int(self.thumb_image_height * 1.2)))
        self.ui.search_result.addItem(imageItem)

    def handle_search_button(self):
        if self.current_label_file is None:
            return
        if not os.path.isfile(self.current_label_file):
            return
        # 首先根据文本框的内容得出一个keyword_list
        keywords = self.ui.search_text.text().split()
        # print(keywords)

        # # 根据文本框的内容查找得文件列表
        # filelist = get_files_by_keywords(self.current_label_file, keywords)
        # # 将拿到的文件名一个一个加入进list_widget (记得先清空)。
        # self.ui.search_result.clear()
        # for file in filelist:
        #     self.add_into_searchResult(os.path.join(self.current_path, file))

        # 可能的耗时操作，写成异步：
        def search_and_append():
            with open(self.current_label_file, "r") as f:
                line_list = f.readlines()
                for line in line_list:
                    if self.threadFlag == 0:
                        return
                    if self.fuzzy_search:
                        if all_keywords_in_line_fuzzy(keywords, line):
                            file_name = line.split("\t")[0]
                            # print(file_name)
                            self.customSignal.search_signal.emit(file_name)
                    else:
                        if all_keywords_in_line(keywords, line):
                            file_name = line.split("\t")[0]
                            # print(file_name)
                            self.customSignal.search_signal.emit(file_name)

        # 启动进程：(先清空已经搜索的内容，还要停止正在搜索的内容)
        self.ui.search_result.clear()
        self.threadFlag = 0
        time.sleep(0.5)
        tempThread = Thread(target=search_and_append)
        self.threadFlag = 1
        tempThread.start()

    def handle_search_signal(self, file_name: str):
        file = os.path.join(self.current_path, file_name)
        if os.path.exists(file):
            self.add_into_searchResult(file)

    def handle_fuzzy_search(self):
        if self.ui.fuzzy_search.text() == "模糊搜索：关闭":
            self.ui.fuzzy_search.setText("模糊搜索：开启")
            self.fuzzy_search = True
        elif self.ui.fuzzy_search.text() == "模糊搜索：开启":
            self.ui.fuzzy_search.setText("模糊搜索：关闭")
            self.fuzzy_search = False

