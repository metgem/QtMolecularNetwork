from PyQt5.QtGui import QColor, QPixmap
from typing import List

import itertools

from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem

from .config import RADIUS
from .node import Node
from .edge import Edge
from .graphicsitem import GraphicsItemLayer
from .style import NetworkStyle, DefaultStyle


class NetworkScene(QGraphicsScene):
    scaleChanged = pyqtSignal(float)
    layoutChanged = pyqtSignal()
    pieChartsVisibilityChanged = pyqtSignal(bool)
    pixmapVisibilityChanged = pyqtSignal(bool)
    locked = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._style = DefaultStyle()
        self._colors = []
        self._scale = 1
        self._pie_charts_visibility = True
        self._pixmap_visibility = True
        self._is_locked = False

        self.clear()

    def networkStyle(self):
        return self._style

    def setNetworkStyle(self, style: NetworkStyle = None):
        new_style = style if style is not None else DefaultStyle()
        for node in self.nodes():
            node.updateStyle(new_style, old=self._style)
        for edge in self.edges():
            edge.updateStyle(new_style, old=self._style)
        self.setBackgroundBrush(new_style.backgroundBrush())
        self._style = new_style
        
    def clear(self):
        super().clear()

        self.nodesLayer = GraphicsItemLayer()
        self.addItem(self.nodesLayer)
        self.nodesLayer.setZValue(1)

        self.edgesLayer = GraphicsItemLayer()
        self.addItem(self.edgesLayer)
        self.edgesLayer.setZValue(0)

    def render(self, painter: QPainter, target: QRectF = QRectF(), source: QRectF = QRectF(),
               mode: Qt.AspectRatioMode = Qt.KeepAspectRatio):
        
        for node in self.nodes():
            node.setCacheMode(QGraphicsItem.NoCache)
        super().render(painter, target, source, mode)
        for node in self.nodes():
            node.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        
    def addNode(self, node: Node):
        node.setParentItem(self.nodesLayer)
        
    def addEdge(self, edge: Edge):
        edge.setParentItem(self.edgesLayer)
        
    def addNodes(self, nodes: List[Node]):
        for node in nodes:
            node.setParentItem(self.nodesLayer)

    def createNodes(self, indexes, labels=None, positions=None, colors=None, radii=None):
        if not indexes:
            return []
        
        if radii is None:
            radii = []
        if colors is None:
            colors = []
        if positions is None:
            positions = []
        if labels is None:
            labels = []

        nodes = []
        for index, label, pos, color, radius in itertools.zip_longest(indexes, labels, positions, colors, radii):
            node = Node(index, label=label)
            if pos:
                node.setPos(pos)

            if self._style is not None:
                node.updateStyle(self._style)

            if isinstance(color, QColor) and color.isValid():
                # noinspection PyTypeChecker
                node.setBrush(color)

            if radius is not None and radius > 0:
                node.setRadius(radius)

            node.setParentItem(self.nodesLayer)
            nodes.append(node)

        return nodes
    
    def addEdges(self, edges: List[Edge]):
        for edge in edges:
            edge.setParentItem(self.edgesLayer)

    def createEdges(self, indexes, sourceNodes, destNodes, widths):
        if not indexes:
            return []
            
        edges = []
        for index, source, dest, width in zip(indexes, sourceNodes, destNodes, widths):
            edge = Edge(index, source, dest, width)
            if self._style is not None:
                edge.updateStyle(self._style)
            edge.setParentItem(self.edgesLayer)
            edge.adjust()
            edges.append(edge)
        return edges

    def removeAllNodes(self):
        for node in self.nodes():
            self.removeItem(node)

    def removeNodes(self, nodes):
        for node in nodes:
            self.removeItem(node)

    def removeAllEdges(self):
        for edge in self.edges():
            self.removeItem(edge)

    def removeEdges(self, edges):
        for edge in edges:
            self.removeItem(edge)

    def nodes(self):
        try:
            return sorted(self.nodesLayer.childItems(), key=lambda node: node.index())
        except RuntimeError:
            return []

    def selectedNodes(self):
        try:
            return [item for item in self.selectedItems() if self.nodesLayer.isAncestorOf(item)]
        except RuntimeError:
            return []

    def setNodesSelection(self, items):
        self.clearSelection()

        # Look if items are Nodes or indexes
        for _ in items:
            is_nodes = isinstance(_, Node)
            break

        if len(items) > 0:
            # noinspection PyUnboundLocalVariable
            if is_nodes:
                for node in items:
                    node.setSelected(True)
            else:
                nodes = self.nodes()
                nodes_len = len(nodes)
                for index in items:
                    if 0 <= index < nodes_len:
                        nodes[index].setSelected(True)

    def selectedNodesBoundingRect(self):
        bounding_rect = QRectF()
        for node in self.selectedNodes():
            bounding_rect |= node.sceneBoundingRect()
        return bounding_rect
    
    def edges(self):
        try:
            return sorted(self.edgesLayer.childItems(), key=lambda node: node.index())
        except RuntimeError:
            return []

    def selectedEdges(self):
        try:
            return [item for item in self.selectedItems() if self.edgesLayer.isAncestorOf(item)]
        except RuntimeError:
            return []

    def setEdgesSelection(self, items):
        self.clearSelection()

        # Look if items are Edges or indexes
        for _ in items:
            is_edges = isinstance(_, Edge)
            break

        if len(items) > 0:
            # noinspection PyUnboundLocalVariable
            if is_edges:
                for edge in items:
                    edge.setSelected(True)
            else:
                edges = self.edges()
                for edge in edges:
                    if edge.index() in items:
                        edge.setSelected(True)

    def setLayout(self, positions, scale=None, isolated_nodes=None):
        if scale is None or scale <= 0:
            scale = self._scale
            
        if isolated_nodes is None:
            isolated_nodes = []
            
        nodes = self.nodes()
        
        if len(positions) < len(nodes):
            return

        scale = scale if scale is not None else self._scale
        isolated_nodes = set(isolated_nodes)
        
        for node in nodes:
            i = node.index()
            if i in isolated_nodes:
                node.setFlag(QGraphicsItem.ItemHasNoContents, True)
                node.setFlag(QGraphicsItem.ItemIsSelectable, False)
                node.setFlag(QGraphicsItem.ItemIsMovable, False)
                node.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
            else:
                node.setFlag(QGraphicsItem.ItemHasNoContents, False)
                node.setFlag(QGraphicsItem.ItemIsSelectable, True)
                node.setFlag(QGraphicsItem.ItemIsMovable, self._is_locked)
                node.setFlag(QGraphicsItem.ItemIgnoresTransformations, False)
                
                node.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, False)
                pos = positions[i]
                node.setPos(*pos * scale)
                node.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

        for edge in self.edges():
            edge.adjust()

        self.layoutChanged.emit()

    def scale(self):
        return self._scale

    def setScale(self, scale=1):
        scale = 1 if scale <= 0 else scale
    
        for node in self.nodes():
            node.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, False)
            node.setPos(node.pos() * scale / self._scale)
            node.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

        for edge in self.edges():
            edge.adjust()

        self._scale = scale
        self.scaleChanged.emit(scale)

    def setLabelsFromModel(self, model, column_id, role=Qt.DisplayRole):
        for node in self.nodes():
            label = model.index(node.index(), column_id).data(role)
            node.setLabel(str(label))

    def resetLabels(self):
        for node in self.nodes():
            label = str(node.index() + 1)
            node.setLabel(label)
            
    def setNodesRadiiFromModel(self, model, column_id, role=Qt.DisplayRole, func=None):       
        if func is not None:
            for node in self.nodes():
                node.setRadius(func(model.index(node.index(), column_id).data(role)))
        else:
            for node in self.nodes():
                node.setRadius(model.index(node.index(), column_id).data(role))
                
        for edge in self.edges():
            edge.adjust()
            
    def resetNodesRadii(self):
        for node in self.nodes():
            node.setRadius(RADIUS)
            
        for edge in self.edges():
            edge.adjust()

    def pieColors(self):
        return self._colors

    def setPieColors(self, colors):
        self._colors = colors

    def setPieChartsFromModel(self, model, column_ids, role=Qt.DisplayRole):
        if len(column_ids) > len(self._colors):
            return

        for node in self.nodes():
            values = [model.index(node.index(), cid).data(role) for cid in column_ids]
            node.setPie(values)

    def resetPieCharts(self):
        for node in self.nodes():
            node.setPie(None)
            
    def pieChartsVisibility(self):
        return self._pie_charts_visibility
        
    def setPieChartsVisibility(self, visibility: bool = True):
        if visibility != self._pie_charts_visibility:
            self._pie_charts_visibility = bool(visibility)
            self.pieChartsVisibilityChanged.emit(visibility)
            
    def setPixmapsFromModel(self, model, column_id, role=Qt.DisplayRole, type="smiles"):
        for node in self.nodes():
            data = model.index(node.index(), column_id).data(role)
            if not data:
                continue
            
            if type == "smiles":
                node.setPixmapFromSmiles(data)
            elif type == "inchi":
                node.setPixmapFromInchi(data)

    def pixmapVisibility(self):
        return self._pixmap_visibility

    def setPixmapVisibility(self, visibility: bool = True):
        if visibility != self._pixmap_visibility:
            self._pixmap_visibility = bool(visibility)
            self.pixmapVisibilityChanged.emit(visibility)
            
    def resetPixmaps(self):
        for node in self.nodes():
            node.setPixmap(QPixmap())

    def hideItems(self, items):
        for item in items:
            item.hide()

    def showItems(self, items):
        for item in items:
            item.show()

    def hideSelectedItems(self):
        items = self.selectedItems()
        self.clearSelection()
        for item in items:
            item.hide()

    def showAllItems(self):
        for item in self.items():
            item.show()
            
    def hideAllItems(self):
        for item in self.items():
            item.hide()

    def nodesColors(self):
        return [node.brush().color() if node.brush().color() != self.networkStyle().nodeBrush().color()
                else QColor() for node in self.nodes()]

    def setNodesColors(self, colors):
        nodes = self.nodes()
        if len(colors) < len(nodes):
            return
        
        for node in nodes:
            color = colors[node.index()]
            if color.isValid():
                node.setBrush(color)

    def setSelectedNodesColor(self, color: QColor):
        if color.isValid():
            for node in self.selectedNodes():
                node.setBrush(color)

    def nodesRadii(self):
        return [node.radius() if node.radius() != RADIUS else 0 for node in self.nodes()]

    def setNodesRadii(self, radii):
        nodes = self.nodes()
        if len(radii) < len(nodes):
            return
        
        for node in nodes:
            radius = radii[node.index()]
            node.setRadius(radius)
            for edge in node.edges():
                edge.adjust()

    def setSelectedNodesRadius(self, radius: int):
        for node in self.selectedNodes():
            node.setRadius(radius)
            for edge in node.edges():
                edge.adjust()
            
    def lock(self, lock: bool = True):
        if lock == self._is_locked:
            return
        
        for node in self.nodes():
            node.setFlag(QGraphicsItem.ItemIsMovable, not lock)
        self._is_locked = lock
        self.locked.emit(lock)
            
    def unlock(self):
        self.lock(False)
        
    def isLocked(self) -> bool:
        return self._is_locked
