from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit
from ui import *


app = QApplication([])
mainWindow = MainWindow()
mainWindow.ui.show()
app.exec_()

# 测试动态载入函数并调用：

# 源码文件路径：
# from mytools.import_function import import_function
# from mytools.dynamic_import import dynamic_import

# source_path = r"D:\PythonProject\Label_and_Search\Labelers\OCR_keyword_label.py"


# 我们希望从这个文件中找到一个函数并调用它。

# names, funcs = import_function(source_path)
# F = dynamic_import(source_path)
# 之后你就可以调用这个函数了！
# print(funcs[0](r'D:\PythonProject\Label_and_Search\test.png'))
