from PySide2.QtCore import QRectF
from PySide2.QtWidgets import QGraphicsItem


class GraphicsItemLayer(QGraphicsItem):

    def boundingRect(self):
        return QRectF(0, 0, 0, 0)

    def paint(self, painter, options, widget):
        pass