from .edge import Edge
from .style import NetworkStyle
from .config import RADIUS
from .mol_depiction import SmilesToPixmap, InchiToPixmap, SvgToPixmap

from typing import Set, Union
from enum import Enum
import base64

from PyQt5.QtGui import (QPen, QColor, QFont, QBrush, QFontMetrics, QPixmap,
                         QPolygonF, QTransform, QPainterPath)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsEllipseItem, QStyle,
                             QApplication)
from PyQt5.QtCore import Qt, QRectF, QSize, QPointF


class NodePolygon(Enum):
    Custom = -1
    Circle = 0
    Square = 1
    Diamond = 2
    ThinDiamond = 3
    TriangleDown = 4
    TriangleUp = 5
    TriangleLeft = 6
    TriangleRight = 7
    Pentagon = 8
    Octagon = 9
    Hexagon = 10
    Star = 11
    Hexagram = 12
    Octagram = 13
    Decagram = 14
    Plus = 15
    X = 16
    Mask = 17


NODE_POLYGON_MAP = {
    NodePolygon.Square:        QPolygonF([QPointF(-50., 50.),    QPointF(50., 50.),
                                          QPointF(50., -50.),    QPointF(-50., -50.)]),
    NodePolygon.TriangleDown:  QPolygonF([QPointF(0., 50.),      QPointF(-50., -28.8),  QPointF(50., -28.8)]),
    NodePolygon.TriangleUp:    QPolygonF([QPointF(0., -50.),     QPointF(-50., 28.8),   QPointF(50., 28.8)]),
    NodePolygon.TriangleLeft:  QPolygonF([QPointF(-50, 0.),      QPointF(28.8, 50),     QPointF(28.8, -50)]),
    NodePolygon.TriangleRight: QPolygonF([QPointF(50, 0.),       QPointF(-28.8, 50),    QPointF(-28.8, -50)]),
    NodePolygon.Diamond:       QPolygonF([QPointF(0., 50.),      QPointF(50., 0.),
                                          QPointF(0., -50.),     QPointF(-50., 0.)]),
    NodePolygon.ThinDiamond:   QPolygonF([QPointF(0., 50.),      QPointF(25., 0.),
                                          QPointF(0., -50.),     QPointF(-25., 0.)]),
    NodePolygon.Pentagon:      QPolygonF([QPointF(-50., -16.),   QPointF(-31., 42.5),   QPointF(31., 42.5),
                                          QPointF(50., -16.),    QPointF(0., -50.)]),
    NodePolygon.Hexagon:       QPolygonF([QPointF(-43.3, 25.),   QPointF(0., 50.),      QPointF(43.30, 25.),
                                          QPointF(43.3, -25.),   QPointF(0., -50.),     QPointF(-43.30, -25.)]),
    NodePolygon.Octagon:       QPolygonF([QPointF(-50., 21.),    QPointF(-21., 50.),    QPointF(21., 50.),
                                          QPointF(50., 21.),     QPointF(50., -21.),    QPointF(21., -50.),
                                          QPointF(-21., -50.),   QPointF(-50., -21.)]),
    NodePolygon.Star:          QPolygonF([QPointF(-50., -16.),   QPointF(-15., -21.),   QPointF(0., -50.),
                                          QPointF(16., -21.),    QPointF(50., -16.),    QPointF(25., 8.),
                                          QPointF(31., 42.3),    QPointF(0., 26.),      QPointF(-31., 42.3),
                                          QPointF(-25., 8.)]),
    NodePolygon.Hexagram:      QPolygonF([QPointF(-50., 0.),     QPointF(-21., 12.),    QPointF(-25., 43.),
                                          QPointF(0., 25.),      QPointF(25., 43.),     QPointF(21., 12.),
                                          QPointF(50., 0.),      QPointF(21., -12.),    QPointF(25., -43.),
                                          QPointF(0., -25.),     QPointF(-25., -43.),   QPointF(-21., -12.)]),
    NodePolygon.Octagram:      QPolygonF([QPointF(-46., 19.),    QPointF(-17.5, 17.5),  QPointF(-19., 46.),
                                          QPointF(0., 25.),      QPointF(19., 46.),     QPointF(17.5, 17.5),
                                          QPointF(46., 19.),     QPointF(25., 0.),      QPointF(46., -19.),
                                          QPointF(17.5, -17.5),  QPointF(19., -46.),    QPointF(0., -25.),
                                          QPointF(-19., -46.),   QPointF(-17.5, -17.5), QPointF(-46., -19.),
                                          QPointF(-25., 0.)]),
    NodePolygon.Decagram:      QPolygonF([QPointF(-48., 16.),    QPointF(-20., 15.),    QPointF(-29., 40.),
                                          QPointF(-8., 24.),     QPointF(0., 50.),      QPointF(8., 24.),
                                          QPointF(29., 40.),     QPointF(20., 15.),     QPointF(48., 16.),
                                          QPointF(25., 0.),      QPointF(48., -16.),    QPointF(20., -15.),
                                          QPointF(29., -40.),    QPointF(8., -24.),     QPointF(0., -50.),
                                          QPointF(-8., -24.),    QPointF(-29., -40.),   QPointF(-20., -15.),
                                          QPointF(-48., -16.),   QPointF(-25., 0.)]),
    NodePolygon.Plus:          QPolygonF([QPointF(-50., 20.),    QPointF(-20., 20.),    QPointF(-20, 50.),
                                          QPointF(20., 50.),     QPointF(20., 20.),     QPointF(50., 20.),
                                          QPointF(50., -20.),    QPointF(20., -20.),    QPointF(20., -50.),
                                          QPointF(-20., -50.),   QPointF(-20., -20.),   QPointF(-50., -20.)]),
    NodePolygon.X:             QPolygonF([QPointF(-22., 50.),    QPointF(0., 30.),      QPointF(22., 50.),
                                          QPointF(50., 22.),     QPointF(30., 0.),      QPointF(50., -22.),
                                          QPointF(22., -50.),    QPointF(0., -30.),     QPointF(-22., -50.),
                                          QPointF(-50., -22.),   QPointF(-30., -0.),    QPointF(-50., 20.)]),
    NodePolygon.Mask:          QPolygonF([QPointF(-50.0, 6.),    QPointF(-6., 23.),    QPointF(6., 23.),
                                          QPointF(50., 6.),      QPointF(44., -23.),   QPointF(0., -29.),
                                          QPointF(-44., -23.)]),
}


class Node(QGraphicsEllipseItem):
    Type = QGraphicsItem.UserType + 1

    def __init__(self, index, label=None):
        super().__init__(-RADIUS, -RADIUS, 2 * RADIUS, 2 * RADIUS)

        self._edges = set()
        self._pie = []

        self._font = QApplication.font()
        self._text_color = QColor()
        self._pixmap = QPixmap()
        self._stock_polygon = NodePolygon.Circle
        self._node_polygon = QPolygonF()
        self._overlay_brush: QBrush = QBrush()

        self.id = index
        if label is None:
            self.setLabel(str(index+1))
        else:
            self.setLabel(label)

        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsScenePositionChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

        self.setBrush(Qt.lightGray)
        self.setPen(QPen(Qt.black, 1))
        self.setZValue(10)

    def invalidateShape(self):
        # TODO: Can't find a good way to update shape
        self.prepareGeometryChange()
        rect = self.rect()
        self.setRect(QRectF())
        self.setRect(rect)
        
    def updateLabelRect(self):
        fm = QFontMetrics(self.font())
        width = fm.width(self.label())
        height = fm.height()
        # noinspection PyAttributeOutsideInit
        self._label_rect = QRectF(-width/2, -height/2, width, height)

        self.invalidateShape()

    def index(self) -> int:
        return self.id

    def radius(self) -> int:
        return int(self.rect().width() / 2)

    def setRadius(self, radius: int):
        self.prepareGeometryChange()
        self.setRect(QRectF(-radius, -radius, 2 * radius, 2 * radius))
        self.scalePolygon()

    def font(self) -> QFont:
        return self._font

    def setFont(self, font: QFont):
        self._font = font
        self.updateLabelRect()

    def textColor(self) -> QColor:
        return self._text_color

    def setTextColor(self, color: QColor):
        self._text_color = color

    # noinspection PyMethodOverriding
    def setBrush(self, brush: QBrush, autoTextColor: bool = True):
        super().setBrush(brush)

        if autoTextColor:
            # Calculate the perceptive luminance (aka luma) - human eye favors green color...
            # See https://stackoverflow.com/questions/1855884/determine-font-color-based-on-background-color
            color = QBrush(brush).color()
            if color.alpha() < 128:
                self._text_color = QColor(Qt.black)
            else:
                luma = (0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()) / 255
                self._text_color = QColor(Qt.black) if luma > 0.5 else QColor(Qt.white)

    def overlayBrush(self) -> QBrush:
        return self._overlay_brush

    def setOverlayBrush(self, brush: QBrush):
        self._overlay_brush = brush

    def label(self) -> str:
        return self._label

    def setLabel(self, label: str):
        # noinspection PyAttributeOutsideInit
        self._label = label
        self.updateLabelRect()

    def pie(self) -> list:
        return self._pie

    def setPie(self, values: list):
        if values is not None:
            sum_ = sum(values)
            values = [v / sum_ for v in values] if sum_ > 0 else []
            self._pie = values
        else:
            self._pie = []
        self.update()

    def pixmap(self):
        return self._pixmap

    def setPixmap(self, pixmap: QPixmap):
        self._pixmap = pixmap

    def setPixmapFromSmiles(self, smiles: str, size: QSize = QSize(300, 300)):
        self._pixmap = SmilesToPixmap(smiles, size)

    def setPixmapFromInchi(self, smiles: str, size: QSize = QSize(300, 300)):
        self._pixmap = InchiToPixmap(smiles, size)
        
    def setPixmapFromBase64(self, b64: bytes) -> None:
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(b64))
        self._pixmap = pixmap
        
    def setPixmapFromSvg(self, svg: bytes, size: QSize = QSize(300, 300)):
        self._pixmap = SvgToPixmap(svg, size)

    def scalePolygon(self):
        rect_size = max(self.rect().width(), self.rect().height())
        polygon_size = max(self._node_polygon.boundingRect().width(), self._node_polygon.boundingRect().height())
        scale = rect_size / polygon_size if polygon_size > 0. else 1.
        self._node_polygon = QTransform().scale(scale, scale).map(self._node_polygon)

    def polygon(self) -> NodePolygon:
        return self._stock_polygon

    def setPolygon(self, id: Union[NodePolygon, int]):
        if isinstance(id, int):
            id = NodePolygon(id)
        self.setCustomPolygon(NODE_POLYGON_MAP.get(id, QPolygonF()))
        self._stock_polygon = id

    def customPolygon(self) -> QPolygonF:
        return self._node_polygon

    def setCustomPolygon(self, polygon: QPolygonF):
        self.prepareGeometryChange()
        self._stock_polygon = NodePolygon.Custom
        self._node_polygon = polygon
        self.scalePolygon()
        self.invalidateShape()

    def addEdge(self, edge: Edge):
        self._edges.add(edge)
        
    def removeEdge(self, edge: Edge):
        self._edges.remove(edge)

    def edges(self) -> Set[Edge]:
        return self._edges

    def updateStyle(self, style: NetworkStyle, old: NetworkStyle = None):
        if old is None or self.brush().color() == old.nodeBrush().color():
            self.setBrush(style.nodeBrush(), autoTextColor=False)
            self.setTextColor(style.nodeTextColor())
        self.setPen(style.nodePen())
        self.setFont(style.nodeFont())
        self.invalidateShape()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            for edge in self._edges:
                edge.adjust()
        elif change == QGraphicsItem.ItemSelectedChange:
            self.setZValue(20 if value else 10)  # Bring item to front
            self.setCacheMode(self.cacheMode())  # Force redraw
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super().mouseReleaseEvent(event)

    def shape(self):
        if self._stock_polygon == NodePolygon.Circle:
            path = super().shape()
        else:
            path = QPainterPath()
            path.addPolygon(self._node_polygon)

        label_path = QPainterPath()
        label_path.addRect(self._label_rect)
        return path.united(label_path)

    # noinspection PyMethodOverriding
    def paint(self, painter, option, widget):
        scene = self.scene()
        if scene is None:
            return

        style = scene.networkStyle()

        # If selected, change brush to yellow
        if option.state & QStyle.State_Selected:
            brush = style.nodeBrush(True)
            text_color = style.nodeTextColor(True)
            if brush is None or not brush.color().isValid():
                brush = self.brush()
                text_color = self.textColor()
            painter.setBrush(brush)
            painter.setPen(style.nodePen(True))
        else:
            painter.setBrush(self.brush())
            painter.setPen(self.pen())
            text_color = self.textColor()
            
        # Get level of detail
        lod = option.levelOfDetailFromTransform(painter.worldTransform())
        rect = self.rect()
        
        if lod < 0.1:
            painter.fillRect(rect, painter.brush())
            return

        if self._stock_polygon == NodePolygon.Circle:
            # Draw ellipse
            if self.spanAngle() != 0 and abs(self.spanAngle()) % (360 * 16) == 0:
                painter.drawEllipse(rect)
                if self._overlay_brush.style() != Qt.NoBrush:
                    painter.setBrush(self._overlay_brush)
                    painter.drawEllipse(rect)
            else:
                painter.drawPie(rect, self.startAngle(), self.spanAngle())
                if self._overlay_brush.style() != Qt.NoBrush:
                    painter.setBrush(self._overlay_brush)
                    painter.drawPie(rect, self.startAngle(), self.spanAngle())

        else:
            # Draw polygon
            painter.drawPolygon(self._node_polygon)

            if self._overlay_brush.style() != Qt.NoBrush:
                painter.setBrush(self._overlay_brush)
                painter.drawPolygon(self._node_polygon)

        # Draw pies if any
        if scene.pieChartsVisibility() and len(self._pie) > 0:
            if self._stock_polygon == NodePolygon.Circle:
                rect = QTransform().scale(.85, .85).mapRect(rect)
            else:
                if self._stock_polygon == NodePolygon.Square:
                    rect = QTransform().scale(1.2, 1.2).mapRect(rect)

                # Set clip path for pies
                painter_path = QPainterPath()
                painter_path.addPolygon(QTransform().scale(.8, .8).map(self._node_polygon))
                painter.setClipPath(painter_path)

            start = 0.
            colors = self.scene().pieColors()
            painter.setPen(QPen(Qt.NoPen))
            for v, color in zip(self._pie, colors):
                painter.setBrush(color)
                painter.drawPie(rect, int(start * 5760), int(v * 5760))
                start += v

        # Draw text
        if lod > 0.4:
            bounding_rect = self.boundingRect()
            painter.setClipping(False)
            painter.setFont(self.font())
            painter.setPen(QPen(text_color, 0))
            painter.drawText(bounding_rect, Qt.AlignCenter, self._label)
            if scene.pixmapVisibility() and not self._pixmap.isNull():
                painter.drawPixmap(bounding_rect.toRect(), self._pixmap, self._pixmap.rect())
