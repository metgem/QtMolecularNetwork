from PySide6.QtGui import QColor, QFont, QBrush, QFontMetrics, QPixmap
from PySide6.QtCore import Qt, QSize

import pytest
import hashlib
import PySide6MolecularNetwork
from PySide6MolecularNetwork.node import NodePolygon, NODE_POLYGON_MAP
from PySide6.QtGui import QPolygonF
from PySide6.QtCore import QPointF

from resources import MOLECULES

SIZES = [QSize(0, 0), QSize(1, 1), QSize(20, 50), QSize(100, 100), QSize(300, 300)]

@pytest.mark.parametrize("index", range(10))
def test_node_init(mod, qapp, index):
    """Check initialization of Node."""

    label = hashlib.sha1(str(index).encode()).hexdigest()
    node = mod.Node(index, label)
    assert node.index() == index
    assert isinstance(node.font(), QFont)
    assert node.font() == qapp.font()
    assert isinstance(node.brush(), QBrush)
    assert isinstance(node.textColor(), QColor)
    assert node.label() == label
    assert isinstance(node.pie(), list)
    assert len(node.pie()) == 0
    assert isinstance(node.edges(), set)
    assert len(node.edges()) == 0
        
        
def test_node_set_label(mod):
    """Check that setLabel successfully change label."""

    index = 5
    node = mod.Node(index)
    assert node.label() == str(index+1)
    label = hashlib.sha1(str(index).encode()).hexdigest()
    node.setLabel(label)
    assert node.label() == label
    
    
def test_node_set_radius(mod):
    """Check that setRadius successfully change radius."""

    node = mod.Node(57)
    assert node.radius() == mod.Config.Radius
    radius = mod.Config.Radius * 2
    node.setRadius(radius)
    assert node.radius() == radius
    
    
def test_node_set_font(mod, qapp):
    """Check that setFont successfully change font."""
    
    node = mod.Node(74)
    assert node.font() == qapp.font()
    font = QFont("Helvetica", 12)
    node.setFont(font)
    assert node.font() == font
    
    
def test_node_set_text_color(mod):
    """Check that setTextColor successfully change text color."""
    
    node = mod.Node(65)
    color = QColor(Qt.red)
    node.setTextColor(color)
    assert node.textColor() == color

@pytest.mark.parametrize("id", range(0, 18))
def test_node_set_polygon(mod, qapp, id):
    """Check that setPolygon successfully change node polygon."""
    
    node = mod.Node(18)
    id = mod.NodePolygon(id)
    polygon = NODE_POLYGON_MAP[NodePolygon(id)] if id != mod.NodePolygon.Circle else QPolygonF()
        
    assert node.polygon() == mod.NodePolygon.Circle
    assert node.customPolygon().isEmpty()
    node.setPolygon(id)
    
    assert node.polygon() == id
    if polygon.isEmpty():  # Circle
        assert node.customPolygon().isEmpty()
    else:
        assert not node.customPolygon().isEmpty()
        assert node.customPolygon().size() == polygon.size()
        
@pytest.mark.parametrize("polygon", [QPolygonF([QPointF(-50., 50.), QPointF(35., 35.), QPointF(24., -24.), QPointF(-58., -58.)]),
                                     QPolygonF([QPointF(0., 25.), QPointF(-74., -35.), QPointF(42., -98.)]),
                                     QPolygonF([QPointF(1., 2.), QPointF(3., 4.)]),
                                     QPolygonF([QPointF(-5., 45.)]),
                                     QPolygonF(),
                                    ])
def test_node_set_custom_polygon(mod, qapp, polygon):
    """Check that setCustomPolygon successfully change node polygon."""
    
    node = mod.Node(34)
    assert node.customPolygon().isEmpty()
    node.setCustomPolygon(polygon)
    
    assert node.polygon() == mod.NodePolygon.Custom
    
    if polygon.isEmpty():  # Circle
        assert node.customPolygon().isEmpty()
    else:
        assert not node.customPolygon().isEmpty()
        assert node.customPolygon().size() == polygon.size()

@pytest.mark.parametrize("color", [Qt.black, Qt.white, Qt.darkGreen,
                                   Qt.blue, Qt.cyan, Qt.transparent])
@pytest.mark.parametrize("autoTextColor", [True, False])
def test_node_set_brush(mod, color, autoTextColor):
    """Check that setBrush successfully change brush."""
    
    node = mod.Node(56)
    brush = QBrush(color)
    node.setBrush(brush)
    assert node.brush() == brush
    if autoTextColor:
        if color in (Qt.black, Qt.darkGreen, Qt.blue):
            assert node.textColor().name() == "#ffffff"
        else:
            assert node.textColor().name() == "#000000"
            
@pytest.mark.parametrize("color", [Qt.black, Qt.white, Qt.darkGreen,
                                   Qt.blue, Qt.cyan, Qt.transparent])
@pytest.mark.parametrize("style", [Qt.NoBrush, Qt.SolidPattern,
                                   Qt.CrossPattern, Qt.DiagCrossPattern])
def test_node_set_overlay_brush(mod, color, style):
    """Check that setOverlayBrush successfully change brush."""
    
    node = mod.Node(41)
    brush = QBrush(color, style)
    assert not node.brush() == QBrush()
    node.setOverlayBrush(brush)
    assert node.overlayBrush != QBrush()
    assert node.overlayBrush() == brush
   
   
@pytest.mark.parametrize("pie", [(0.25, 0.5, 0.25), (1, 2, 3, 4),
                                 (1,), [], range(10)])
def test_node_set_pie(mod, pie):
    """Check that setPie successfully change pie list."""
    
    node = mod.Node(23)
    node.setPie(pie)
    p = node.pie()
    assert len(p) == len(pie)
    if len(pie) > 0:
        assert pytest.approx(sum(p)) == 1
    for i in range(len(pie)):
        assert pie[i] / max(pie) == pytest.approx(p[i] / max(p))
        

@pytest.mark.parametrize("molecule", MOLECULES)
def test_node_set_pixmap(mod, molecule):
    """Check that setPixmap successfully change pixmap."""
    
    node = mod.Node(32)
    assert node.pixmap().isNull()
    pixmap = QPixmap(molecule['image'])
    node.setPixmap(pixmap)
    p = node.pixmap()
    assert not p.isNull()
    assert p.size() == pixmap.size()
    assert p.cacheKey() == pixmap.cacheKey()

@pytest.mark.parametrize("molecule", MOLECULES)
@pytest.mark.parametrize("size", SIZES)
def test_node_set_pixmap_from_smiles(mod, molecule, size):
    """Check that setPixmapFromSmiles successfully change pixmap."""
    
    node = mod.Node(58)
    assert node.pixmap().isNull()
    node.setPixmapFromSmiles(molecule['smiles'], size)
    p = node.pixmap()
    assert p.isNull() == size.isNull()
    assert p.size() == size
    
@pytest.mark.parametrize("smiles", ["", "invalid"])
@pytest.mark.parametrize("size", SIZES)
def test_node_set_pixmap_from_smiles_invalid(mod, smiles, size):
    """Check that setPixmapFromSmiles does nothing if smiles is invalid."""
    
    node = mod.Node(74)
    assert node.pixmap().isNull()
    node.setPixmapFromSmiles(smiles, size)
    assert node.pixmap().isNull()

@pytest.mark.parametrize("molecule", MOLECULES)
@pytest.mark.parametrize("size", SIZES)
def test_node_set_pixmap_from_inchi(mod, molecule, size):
    """Check that setPixmapFromInchi successfully change pixmap."""
    
    node = mod.Node(45)
    assert node.pixmap().isNull()
    node.setPixmapFromInchi(molecule['inchi'], size)
    p = node.pixmap()
    assert p.isNull() == size.isNull()
    assert p.size() == size

@pytest.mark.parametrize("inchi", ["", "invalid"])
@pytest.mark.parametrize("size", SIZES)
def test_node_set_pixmap_from_inchi_invalid(mod, inchi, size):
    """Check that setPixmapFromInchi does nothing if inchi is invalid."""
    
    node = mod.Node(65)
    assert node.pixmap().isNull()
    node.setPixmapFromInchi(inchi, size)
    assert node.pixmap().isNull()
    
def test_node_shape_set_label(mod):
    """Check that shape is modified when label is changed"""
    
    node = mod.Node(226, "")
    assert node.shape().boundingRect().width() > mod.Config.Radius * 2
    fm = QFontMetrics(node.font())
    
    label = "very long label"
    node.setLabel(label)
    assert(node.label() == label)
    width = fm.horizontalAdvance(label)
    assert node.boundingRect().width() >= width
    
    label = "really really loooooooooooooong label"
    node.setLabel(label)
    assert(node.label() == label)
    assert node.boundingRect().width() >= fm.horizontalAdvance(label)
    assert node.boundingRect().width() > width
    
    label = "1"
    node.setLabel(label)
    assert node.label() == label
    assert node.boundingRect().width() < width
    
    
def test_node_shape_set_font(mod):
    label = "very long label"
    node = mod.Node(226, label)
  
    width = node.boundingRect().width()
    font = QFont("Times", 32)
    fm = QFontMetrics(font)
    node.setFont(font)
    assert node.font() == font
    assert node.boundingRect().width() >= fm.horizontalAdvance(label) > width
    
    font = QFont("Times", 4)
    fm = QFontMetrics(font)
    node.setFont(font)
    assert node.font() == font
    assert node.boundingRect().width() < width
