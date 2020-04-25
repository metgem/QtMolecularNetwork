from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget
from PyQt5.QtGui import QPainter

from typing import Optional


class GraphicsItemLayer(QGraphicsItem):

    def boundingRect(self):
        return QRectF(0, 0, 0, 0)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem,
              widget: Optional[QWidget] = ...):
        pass
