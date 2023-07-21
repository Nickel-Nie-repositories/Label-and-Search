# 参考： https://www.cnblogs.com/zhiyiYo/p/15676079.html
import sys

from PySide2.QtCore import QRect, QRectF, QSize, Qt, QPointF, Signal
from PySide2.QtGui import QPainter, QPixmap, QWheelEvent, QMouseEvent, QTransform
from PySide2.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                               QGraphicsScene, QGraphicsView, QGraphicsSimpleTextItem,
                               QGraphicsRectItem)


class ImageViewer(QGraphicsView):
    """ 图片查看器 """

    finish_Draw_rect = Signal(float, float, float, float)
    finish_Draw_Point = Signal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.zoomInTimes = 0
        self.maxZoomInTimes = 23

        # 创建场景
        self.graphicsScene = QGraphicsScene()

        # 图片
        self.pixmap = QPixmap(r'D:\PythonProject\Label_and_Search/test.png')
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.displayedImageSize = QSize(0, 0)

        # ///////////////////<在这个基础上实现 打点 和 画矩形 >/////////////////////
        self.mouseState = "拖拽"
        self.lastPos = QPointF(0, 0)
        self.graphicsList = []
        self.graphicsCoordList = []

        # 初始化小部件
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        # self.resize(1200, 900)

        # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 以鼠标所在位置为锚点进行缩放
        self.setTransformationAnchor(self.AnchorUnderMouse)

        # 平滑缩放
        self.pixmapItem.setTransformationMode(Qt.SmoothTransformation)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform)

        # 设置场景
        self.graphicsScene.addItem(self.pixmapItem)
        self.setScene(self.graphicsScene)

    def wheelEvent(self, e: QWheelEvent):
        """ 滚动鼠标滚轮缩放图片 """
        if e.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()
        self.mouseState = "拖拽"
        self.setCursor(Qt.ArrowCursor)
        self.__setDragEnabled(self.__isEnableDrag())

    def resizeEvent(self, e):
        """ 缩放图片 """
        super().resizeEvent(e)

        if self.zoomInTimes > 0:
            return

        # 调整图片大小
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size() * ratio
        if ratio < 1:
            self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
        else:
            self.resetTransform()

    def setImage(self, imagePath: str):
        """ 设置显示的图片 """
        self.resetTransform()

        # 刷新图片
        self.pixmap = QPixmap(imagePath)
        self.pixmapItem.setPixmap(self.pixmap)
        # 清除上面画的框线：
        self.clear_graphics()
        # 调整图片大小
        self.setSceneRect(QRectF(self.pixmap.rect()))
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size() * ratio
        if ratio < 1:
            self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)

    def resetTransform(self):
        """ 重置变换 """
        super().resetTransform()
        self.zoomInTimes = 0
        self.__setDragEnabled(False)

    def __isEnableDrag(self):
        """ 根据图片的尺寸决定是否启动拖拽功能 """
        v = self.verticalScrollBar().maximum() > 0
        h = self.horizontalScrollBar().maximum() > 0
        return v or h

    def __setDragEnabled(self, isEnabled: bool):
        """ 设置拖拽是否启动 """
        self.setDragMode(
            self.ScrollHandDrag if isEnabled else self.NoDrag)

    def __getScaleRatio(self):
        """ 获取显示的图像和原始图像的缩放比例 """
        if self.pixmap.isNull():
            return 1

        pw = self.pixmap.width()
        ph = self.pixmap.height()
        rw = min(1, self.width() / pw)
        rh = min(1, self.height() / ph)
        return min(rw, rh)

    def fitInView(self, item: QGraphicsItem, mode=Qt.KeepAspectRatio):
        """ 缩放场景使其适应窗口大小 """
        super().fitInView(item, mode)
        self.displayedImageSize = self.__getScaleRatio() * self.pixmap.size()
        self.zoomInTimes = 0

    def zoomIn(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
        """ 放大图像 """
        if self.zoomInTimes == self.maxZoomInTimes:
            return

        self.setTransformationAnchor(viewAnchor)

        self.zoomInTimes += 1
        self.scale(1.1, 1.1)
        self.__setDragEnabled(self.__isEnableDrag())

        # 还原 anchor
        self.setTransformationAnchor(self.AnchorUnderMouse)

    def zoomOut(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
        """ 缩小图像 """
        if self.zoomInTimes == 0 and not self.__isEnableDrag():
            return

        self.setTransformationAnchor(viewAnchor)

        self.zoomInTimes -= 1

        # 原始图像的大小
        pw = self.pixmap.width()
        ph = self.pixmap.height()

        # 实际显示的图像宽度
        w = self.displayedImageSize.width() * 1.1 ** self.zoomInTimes
        h = self.displayedImageSize.height() * 1.1 ** self.zoomInTimes

        # 这里大概是说，缩小，多以图像的原本大小为界，但是如果原图很大，我们希望窥之全貌，于是以窗口大小为界。
        if pw > self.width() or ph > self.height():
            # 在窗口尺寸小于原始图像时禁止继续缩小图像比窗口还小
            if w <= self.width() and h <= self.height():
                self.fitInView(self.pixmapItem)
            else:
                self.scale(1 / 1.1, 1 / 1.1)
        else:
            # 在窗口尺寸大于图像时不允许缩小的比原始图像小
            if w <= pw:
                self.resetTransform()
            else:
                self.scale(1 / 1.1, 1 / 1.1)

        self.__setDragEnabled(self.__isEnableDrag())

        # 还原 anchor
        self.setTransformationAnchor(self.AnchorUnderMouse)

    # 定义选中绘制点工具的处理：
    def StartDrawPoint(self):
        self.mouseState = "点/待按下"
        self.__setDragEnabled(False)
        self.setCursor(Qt.CrossCursor)

    # 定义选中绘制矩形工具的处理：
    def StartDrawRect(self):
        self.mouseState = "矩形/待按下"
        self.__setDragEnabled(False)
        self.setCursor(Qt.CrossCursor)
        self.setDragMode(self.RubberBandDrag)

    # 重载鼠标按下事件：
    def mousePressEvent(self, event: QMouseEvent):
        if self.mouseState == "点/待按下" and event.button() == Qt.LeftButton:
            pos = event.pos()
            pos = self.mapToScene(pos)
            correctedPos = pos - QPointF(3.75, 7.5)
            self.Draw_Point(correctedPos)
            self.finish_Draw_Point.emit(correctedPos.x(), correctedPos.y())
            # 恢复状态：
            self.mouseState = "拖拽"
            self.setCursor(Qt.ArrowCursor)
            self.__setDragEnabled(self.__isEnableDrag())
        elif self.mouseState == "矩形/待按下" and event.button() == Qt.LeftButton:
            super(ImageViewer, self).mousePressEvent(event)
            pos = event.pos()
            pos = self.mapToScene(pos)
            # 记录一下pos：
            self.lastPos = pos
            self.mouseState = "矩形/待松开"
        else:
            super(ImageViewer, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.mouseState == "矩形/待松开" and event.button() == Qt.LeftButton:
            pos = event.pos()
            pos = self.mapToScene(pos)
            # 绘制矩形：
            self.Draw_Rect(self.lastPos, pos)
            # 同时需要向上层发送一个信号，以让他们可以记录进label。
            self.finish_Draw_rect.emit(self.lastPos.x(), self.lastPos.y(), pos.x(), pos.y())
            # 恢复状态：
            self.mouseState = "拖拽"
            self.setCursor(Qt.ArrowCursor)
            self.__setDragEnabled(self.__isEnableDrag())
        else:
            super(ImageViewer, self).mouseReleaseEvent(event)

    def Draw_Rect(self, pos1, pos2):
        tempItem = QGraphicsRectItem(QRectF(pos1, pos2))
        self.graphicsScene.addItem(tempItem)
        self.graphicsList.append(tempItem)
        coordinate_text = "(%.6f,%.6f,%.6f,%.6f)" % (pos1.x(), pos1.y(), pos2.x(), pos2.y())
        self.graphicsCoordList.append(coordinate_text)

    def Draw_Point(self, pos):
        tempItem = QGraphicsSimpleTextItem()
        tempItem.setText("+")
        tempItem.setPos(pos)
        self.graphicsScene.addItem(tempItem)
        self.graphicsList.append(tempItem)
        coordinate_text = "(%.6f,%.6f)" % (pos.x(), pos.y())
        self.graphicsCoordList.append(coordinate_text)

    def pop_graphics(self, text: str):
        if self.graphicsCoordList[-1] == text:
            self.graphicsScene.removeItem(self.graphicsList.pop())
            self.graphicsCoordList.pop()

    def clear_graphics(self):
        for i in range(len(self.graphicsCoordList)):
            self.graphicsScene.removeItem(self.graphicsList.pop())
            self.graphicsCoordList.pop()

    def redraw(self, coordinate_text: str):
        float_list = coordinate_text[1:-1].split(",")
        float_list = [float(i) for i in float_list]
        if len(float_list) == 4:
            self.Draw_Rect(QPointF(float_list[0], float_list[1]), QPointF(float_list[2], float_list[3]))
        if len(float_list) == 2:
            self.Draw_Point(QPointF(float_list[0], float_list[1]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ImageViewer()
    w.show()
    sys.exit(app.exec_())
