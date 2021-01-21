from PyQt5.QtGui import QPen, QColor, QStandardItemModel, QStandardItem, QPixmap, QPainter, QImage
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QPoint, QPointF, QSize

import pytest
import hashlib
import random
import numpy as np

from resources import MOLECULES
  
POSITIONS = [(56, 196), (136, 236), (60, 300), (160, 328), (232, 252),
             (240, 148), (184, 76), (280, 64), (336, 132), (304, 216)]
LINKS = [(0, 1), (1, 2), (1, 3), (1, 4), (1, 5), (4, 5), (5, 6), (5, 7), (5, 8), (5, 9)]
WIDTHS = (11.024, 9.868, 13.504, 6.664, 9.944, 10.036, 7.984, 11.028, 6.464, 8.504)
  
@pytest.fixture
def scene(mod, qapp):
    scene = mod.NetworkScene()
    nodes = scene.createNodes(range(len(POSITIONS)),
                           labels=["({},{})".format(x, y) for x, y in POSITIONS],
                           positions=[QPointF(x, y) for x, y in POSITIONS])
    sources, dests = zip(*LINKS)
    scene.createEdges(range(len(LINKS)), [nodes[x] for x in sources],
                   [nodes[x] for x in dests], WIDTHS)

    return scene

    
def test_scene_init(mod):
    """Check initialization of NetworkScene."""
    
    scene = mod.NetworkScene()
    assert isinstance(scene.networkStyle(), mod.NetworkStyle)
    assert isinstance(scene.pieColors(), list)
    assert scene.scale() == 1
    
    
def test_scene_add_node(mod):
    """Check that a node can be added to the scene."""
    
    scene = mod.NetworkScene()
    assert len(scene.nodes()) == 0
    nodes = []
    for i in range(10):
        node = mod.Node(i)
        scene.addNode(node)
        nodes.append(node)
        assert len(scene.nodes()) == i+1
        assert scene.nodes() == nodes
        
    # Try without keeping a reference
    for i in range(10, 20):
        scene.addNode(mod.Node(i))
        assert len(scene.nodes()) == i+1
        
def test_scene_add_nodes(mod):
    """Check that a node can be added by batch to the scene."""
    
    scene = mod.NetworkScene()
    assert len(scene.nodes()) == 0
    nodes = [mod.Node(i) for i in range(10)]
    scene.addNodes(nodes)
    assert len(scene.nodes()) == len(nodes)
    assert scene.nodes() == nodes
    
    # Try without keeping a reference
    scene.addNodes([mod.Node(i) for i in range(10, 20)])
    assert len(scene.nodes()) == len(nodes) + 10
        
        
def test_scene_add_edge(mod):
    """Check that an edge can be added to the scene."""
    
    scene = mod.NetworkScene()
    assert len(scene.edges()) == 0
    nodes = [mod.Node(i) for i in range(10)]
    edges = []
    for i in range(5):
        edge = mod.Edge(i, nodes[i], nodes[i+5], 1)
        scene.addEdge(edge)
        edges.append(edge)
        assert len(scene.edges()) == i+1
        assert scene.edges() == edges
        
    # Try without keeping a reference
    for i in range(5, 10):
        scene.addEdge(mod.Edge(i, mod.Node(i), mod.Node(20-i), 1))
        assert len(scene.edges()) == i+1
        
        
def test_scene_add_edges(mod):
    """Check that a node can be added by batch to the scene."""
    
    scene = mod.NetworkScene()
    assert len(scene.edges()) == 0
    edges = [mod.Edge(i, mod.Node(i), mod.Node(20-i)) for i in range(5)]
    scene.addEdges(edges)
    assert len(scene.edges()) == len(edges)
    assert scene.edges() == edges
    
    # Try without keeping a reference
    scene.addEdges([mod.Edge(i, mod.Node(i), mod.Node(20-i), 1) for i in range(5, 10)])
    assert len(scene.edges()) == len(edges) + 5
    
    
@pytest.mark.parametrize("indexes, labels, positions, colors, radii",
    [ (range(10), None, None, None, None),
      ([0, 1], ["0", "1"], None, None, None),
      ([0, 1], None, [QPoint(0, 1), QPoint(5,2)], None, None),
      ([0, 1], None, None, [QColor(Qt.red), QColor(Qt.blue)], None),
      ([0, 1], None, None, None, [5, 20]),
    ])
def test_scene_create_nodes(mod, indexes, labels, positions, colors, radii):
    """Check that nodes can be added to the scene."""
    
    scene = mod.NetworkScene()
    
    kwargs = {}
    if labels is not None:
        kwargs['labels'] = labels
    if positions is not None:
        kwargs['positions'] = positions
    if colors is not None:
        kwargs['colors'] = colors
    if radii is not None:
        kwargs['radii'] = radii
    
    scene.createNodes(indexes, **kwargs)
    assert len(scene.nodes()) == len(indexes)
    nodes = scene.nodes()
    for i in range(len(indexes)):
        assert nodes[i].index() == indexes[i]
        if labels is not None:
            assert nodes[i].label() == labels[i]
        if positions is not None:
            assert nodes[i].pos() == positions[i]
        if colors is not None:
            assert nodes[i].brush().color() == colors[i]
        if radii is not None:
            assert nodes[i].radius() == radii[i]
            
            
def test_scene_create_nodes_empty(mod):
    """Check that createNodes with an empty list does nothing."""
    
    scene = mod.NetworkScene()
    nodes = scene.createNodes([])
    assert len(scene.items()) == 2  # Scene always contains nodes and edges container
    assert len(nodes) == 0
    
            
@pytest.mark.parametrize("width", [0, 0.24, 1, 10])
def test_scene_create_edges(mod, width):
    """Check that edges can be added to the scene."""
    
    scene = mod.NetworkScene()
    scene.createNodes(range(10))
    sources = scene.nodes()[:5]
    dests = scene.nodes()[5:]
    scene.createEdges(range(5), sources, dests, [width] * 5)
    assert len(scene.edges()) == 5
    edges = scene.edges()
    for i in range(5):
        assert edges[i].index() == i
        assert edges[i].width() == width
        assert edges[i].sourceNode() == sources[i]
        assert edges[i].destNode() == dests[i]
        
def test_scene_create_edges_empty(mod):
    """Check that createEdges with empty lists does nothing."""
    
    scene = mod.NetworkScene()
    edges = scene.createEdges([], [], [], [])
    assert len(scene.items()) == 2  # Scene always contains nodes and edges container
    assert len(edges) == 0
        
        
def test_scene_remove_all_nodes(scene):
    """Check that nodes can be removed from the scene."""
       
    assert len(scene.nodes()) == len(POSITIONS)
    scene.removeAllNodes()
    assert len(scene.nodes()) == 0
    

def test_scene_remove_all_edges(scene):
    """Check that edges can be removed from the scene."""
    
    assert len(scene.edges()) == len(LINKS)
    scene.removeAllEdges()
    assert len(scene.edges()) == 0
    

def test_scene_remove_nodes(scene):
    """Check that specific nodes can be removed from the scene."""
       
    nodes = scene.nodes()
    num_nodes = len(POSITIONS)
    assert len(nodes) == num_nodes
    for i in range(num_nodes // 2):
        scene.removeNodes([nodes[i], nodes[i + num_nodes // 2]])
        assert len(scene.nodes()) == num_nodes - (i+1)*2
        assert nodes[i] not in scene.nodes()
        assert nodes[i + num_nodes // 2] not in scene.nodes()
    assert len(scene.nodes()) == 0
    

def test_scene_remove_edges(scene):
    """Check that specific edges can be removed from the scene."""
       
    edges = scene.edges()
    num_edges = len(LINKS)
    assert len(edges) == num_edges
    for i in range(num_edges):
        scene.removeEdges([edges[i]])
        assert len(scene.edges()) == num_edges - i - 1
        assert edges[i] not in scene.edges()
    assert len(scene.edges()) == 0
    

@pytest.mark.parametrize("scale", [0, 1, 0.245, 1000])
def test_scene_set_scale(scene, scale, qtbot):
    """Check that scale can be changed."""
    
    effective_scale = 1 if scale <= 0 else scale
    
    for node in scene.nodes():
        x, y = POSITIONS[node.index()]
        assert node.pos().x() == x
        assert node.pos().y() == y
            
    with qtbot.waitSignal(scene.scaleChanged, check_params_cb=lambda s: s == effective_scale):
        scene.setScale(scale)
    
    for node in scene.nodes():
        x, y = POSITIONS[node.index()]
        assert node.pos().x() == pytest.approx(x * effective_scale)
        assert node.pos().y() == pytest.approx(y * effective_scale)
        
    with qtbot.waitSignal(scene.scaleChanged, check_params_cb=lambda s: s == 1):
        scene.setScale(1)
    
    for node in scene.nodes():
        x, y = POSITIONS[node.index()]
        assert node.pos().x() == pytest.approx(x)
        assert node.pos().y() == pytest.approx(y)
        
        
@pytest.mark.parametrize("role", [Qt.DisplayRole, Qt.UserRole+1])
def test_scene_set_labels_from_model(scene, role):
    """Check that setLabelsFromModel change labels on all nodes."""
    
    model = QStandardItemModel()
    
    for i in range(len(scene.nodes())):
        item = QStandardItem()
        label = hashlib.sha1(str(i).encode()).hexdigest()
        item.setData(label, role)
        model.setItem(i, 0, item)
        item = QStandardItem()
        label = hashlib.md5(str(i).encode()).hexdigest()
        item.setData(label, role)
        model.setItem(i, 1, item)
    
    scene.setLabelsFromModel(model, 0, role)
    
    for node in scene.nodes():
        label = hashlib.sha1(str(node.index()).encode()).hexdigest()
        assert node.label() == label
        
    scene.setLabelsFromModel(model, 1, role)
    
    for node in scene.nodes():
        label = hashlib.md5(str(node.index()).encode()).hexdigest()
        assert node.label() == label
        
    scene.resetLabels()
    
    for node in scene.nodes():
        assert node.label() == str(node.index()+1)
        
        
@pytest.mark.parametrize("role", [Qt.DisplayRole, Qt.UserRole+1])
@pytest.mark.parametrize("func", [None, lambda x: x, lambda x: 2*x, lambda x: x//3], ids=["None", "identity", "2*x", "x/3"])
def test_scene_set_nodes_radii_from_model(scene, role, func):
    """Check that setNodesRadiiFromModel change radius for all nodes."""
    
    model = QStandardItemModel()
    
    default = scene.nodes()[0].radius()
    
    values = []
    for i in range(len(scene.nodes())):
        item = QStandardItem()
        radius0 = random.randint(0, 100)
        item.setData(radius0, role)
        model.setItem(i, 0, item)
        item = QStandardItem()
        radius1 = random.randint(0, 100)
        item.setData(radius1, role)
        model.setItem(i, 1, item)
        values.append((radius0, radius1))
    
    for col in range(1):       
        if func is not None:
            scene.setNodesRadiiFromModel(model, col, role, func)
            for node in scene.nodes():
                assert node.radius() == func(values[node.index()][col])
        else:
            scene.setNodesRadiiFromModel(model, col, role)
            for node in scene.nodes():
                assert node.radius() == values[node.index()][col]
        
    scene.resetNodesRadii()
    
    for node in scene.nodes():
        assert node.radius() == default
        

def test_scene_set_pie_colors(scene):
    """Check that setPieColors change colors."""
    
    colors = [QColor(i) for i in range(2, 12)]
    
    scene.setPieColors(colors)
    assert scene.pieColors() == colors
    

@pytest.mark.parametrize("colors", [[QColor(i) for i in range(2, 7)],
                                    [QColor(i) for i in range(2, 6)]])
@pytest.mark.parametrize("role", [Qt.DisplayRole, Qt.UserRole+1])
def test_scene_set_pie_charts_from_model(scene, colors, role):
    """Check that setPieChartsFromModel change pie charts on all nodes."""
    
    model = QStandardItemModel()
    scene.setPieColors(colors)
    
    for i in range(len(scene.nodes())):
        for j in range(10):
            item = QStandardItem()
            item.setData(i+j, role)
            model.setItem(i, j, item)
            
    for node in scene.nodes():
        assert len(node.pie()) == 0
        
    scene.setPieChartsFromModel(model, range(0, 5), role)
    
    if len(colors) < 5:
        for node in scene.nodes():
            assert len(node.pie()) == 0
    else:
        for node in scene.nodes():
            values = [node.index()+j for j in range(5)]
            values = [v/sum(values) for v in values]
            assert node.pie() == values
        
        scene.setPieChartsFromModel(model, range(5, 10), role)
    
        for node in scene.nodes():
            values = [node.index()+j for j in range(5, 10)]
            values = [v/sum(values) for v in values]
            assert node.pie() == values
            
        scene.resetPieCharts()
        
        for node in scene.nodes():
            assert len(node.pie()) == 0
            

def test_scene_set_pie_charts_visibility(qtbot, scene):
    """Check that setPieChartsVisibility effectively changed pie charts visibility."""
    
    assert scene.pieChartsVisibility() == True
    with qtbot.waitSignal(scene.pieChartsVisibilityChanged):
        scene.setPieChartsVisibility(False)
        assert scene.pieChartsVisibility() == False
        
    with qtbot.assertNotEmitted(scene.pieChartsVisibilityChanged):
        scene.setPieChartsVisibility(False)
        assert scene.pieChartsVisibility() == False
        
    with qtbot.waitSignal(scene.pieChartsVisibilityChanged):
        scene.setPieChartsVisibility(True)
        assert scene.pieChartsVisibility() == True
        
@pytest.mark.parametrize("molecule", MOLECULES)
@pytest.mark.parametrize("role", [Qt.DisplayRole, Qt.UserRole+1])
@pytest.mark.parametrize("type", ["smiles", "inchi"])
def test_scene_set_pixmaps_from_model(scene, molecule, role, type):
    """Check that setPixmapsFromModel change pixmaps on all nodes."""
    
    model = QStandardItemModel()
    
    for i in range(len(scene.nodes())):
        for j in range(2):
            item = QStandardItem()
            data = molecule[type]
            item.setData(data, role)
            model.setItem(i, j, item)
            
    for node in scene.nodes():
        assert node.pixmap().isNull()
        
        
    for column in range(0, 1):
        scene.setPixmapsFromModel(model, column, role, scene.PixmapsSmiles if type=="smiles" else scene.PixmapsInchi)
        
        for node in scene.nodes():
            pixmap = QPixmap(molecule['image'])
            p = node.pixmap()
            assert not p.isNull()
            assert p.size() == pixmap.size()
        
        scene.resetPixmaps()
    
        for node in scene.nodes():
            assert node.pixmap().isNull()
            
@pytest.mark.parametrize("molecule", MOLECULES)
@pytest.mark.parametrize("role", [Qt.DisplayRole, Qt.UserRole+1])
@pytest.mark.parametrize("type", ["smiles", "inchi"])
def test_scene_set_pixmaps_from_model_auto(scene, molecule, role, type):
    """Check that setPixmapsFromModel change pixmaps on all nodes."""
           
    model = QStandardItemModel()
    
    for i in range(len(scene.nodes())):
        for j in range(2):
            item = QStandardItem()
            data = molecule[type]
            item.setData(data, role)
            model.setItem(i, j, item)
            
    for node in scene.nodes():
        assert node.pixmap().isNull()
        
    for column in range(0, 1):
        scene.setPixmapsFromModel(model, column, role, scene.PixmapsAuto)
        
        for node in scene.nodes():
            pixmap = QPixmap(molecule['image'])
            p = node.pixmap()
            assert not p.isNull()
            assert p.size() == pixmap.size()
        
        scene.resetPixmaps()
    
        for node in scene.nodes():
            assert node.pixmap().isNull()
        
@pytest.mark.parametrize("molecule", MOLECULES)
def test_scene_reset_pixmaps(scene, molecule):
    """Check that reset pixmaps sucessfully reset pixmaps for all nodes in scene"""
    
    for node in scene.nodes():
        assert node.pixmap().isNull()
        
    for node in scene.nodes():
        node.setPixmap(QPixmap(molecule['image']))
        
    for node in scene.nodes():
        assert not node.pixmap().isNull()
        
    scene.resetPixmaps()
    
    for node in scene.nodes():
        assert node.pixmap().isNull()
        
def test_scene_set_pixmap_visibility(qtbot, scene):
    """Check that setPixmapVisibility effectively changed pixmap visibility."""
    
    assert scene.pixmapVisibility() == True
    with qtbot.waitSignal(scene.pixmapVisibilityChanged):
        scene.setPixmapVisibility(False)
        assert scene.pixmapVisibility() == False
        
    with qtbot.assertNotEmitted(scene.pixmapVisibilityChanged):
        scene.setPixmapVisibility(False)
        assert scene.pixmapVisibility() == False
        
    with qtbot.waitSignal(scene.pixmapVisibilityChanged):
        scene.setPixmapVisibility(True)
        assert scene.pixmapVisibility() == True

            
def test_scene_show_hide_items(scene):
    """Check that nodes/edges can be hidden/shown."""
    
    nodes = scene.nodes()
    edges = scene.edges()
    
    for node in nodes:
        assert node.isVisible() == True
        
    for edge in edges:
        assert edge.isVisible() == True
       
    for i in range(len(nodes)//2):
        scene.hideItems([nodes[i], nodes[i+5]])
        assert nodes[i].isVisible() == False
        assert nodes[i+5].isVisible() == False
    
    for i in range(len(edges)//2):
        scene.hideItems([edges[i], edges[i+2]])
        assert edges[i].isVisible() == False
        assert edges[i+2].isVisible() == False
    
    scene.showItems(nodes + edges)
    
    for node in nodes:
        assert node.isVisible() == True
        
    for edge in edges:
        assert edge.isVisible() == True
        
    scene.hideAllItems()
    
    for node in nodes:
        assert node.isVisible() == False
        
    for edge in edges:
        assert edge.isVisible() == False
        
    scene.showAllItems()
    
    for node in nodes:
        assert node.isVisible() == True
        
    for edge in edges:
        assert edge.isVisible() == True
        
        
def test_scene_hide_selected_items(scene):
    """Check that hideSelectedItems hide only selected items"""
    
    scene.clearSelection()
    assert len(scene.selectedItems()) == 0
    
    for node in scene.nodes():
        assert node.isVisible()
    for edge in scene.edges():
        assert edge.isVisible()
    
    selected_items = set()
    not_selected_items = set()
    for i, node in enumerate(scene.nodes()):
        if i % 2 == 0:
            node.setSelected(True)
            selected_items.add(node)
        else:
            not_selected_items.add(node)
    for i, edge in enumerate(scene.edges()):
        if i % 3 == 0:
            edge.setSelected(True)
            selected_items.add(edge)
        else:
            not_selected_items.add(edge)
    assert selected_items == set(scene.selectedItems())
        
    scene.hideSelectedItems()
    assert len(scene.selectedItems()) == 0

    for item in selected_items:
        assert not item.isVisible()
    for item in not_selected_items:
        assert item.isVisible()
        
def test_scene_set_selection(scene):
    """Check that nodes/edges can be selected programmatically."""
    
    nodes = scene.nodes()
    edges = scene.edges()
    
    for node in nodes:
        assert node.isSelected() == False
        
    for edge in edges:
        assert edge.isSelected() == False
       
    for i in range(len(nodes)//2):
        scene.setNodesSelection([nodes[i], nodes[i+5]])
        assert nodes[i].isSelected() == True
        assert nodes[i+5].isSelected() == True
    
    for i in range(len(edges)//2):
        scene.setEdgesSelection([edges[i], edges[i+2]])
        assert edges[i].isVisible() == True
        assert edges[i+2].isVisible() == True
        
    scene.setNodesSelection([])
    for node in nodes:
        assert node.isSelected() == False
        
    scene.setEdgesSelection([])
    for edge in edges:
        assert edge.isSelected() == False
        
    for i in range(len(nodes)//2):
        scene.setNodesSelection([i, i+5])
        assert nodes[i].isSelected() == True
        assert nodes[i+5].isSelected() == True
    
    for i in range(len(edges)//2):
        scene.setEdgesSelection([i, i+2])
        assert edges[i].isVisible() == True
        assert edges[i+2].isVisible() == True
        
        
@pytest.mark.parametrize("color", [QColor(), QColor(Qt.blue)])
def test_scene_set_selected_nodes_color(scene, color):
    """Check that setSelectedNodesColor modify only the color of selected nodes
    and do nothing if color is not valid"""
    
    for node in scene.nodes():
        assert node.brush().color() != color
        
    selected_nodes = set()
    not_selected_nodes = set()
    for i, node in enumerate(scene.nodes()):
        if i % 2 == 0:
            node.setSelected(True)
            selected_nodes.add(node)
        else:
            not_selected_nodes.add(node)
            
    scene.setSelectedNodesColor(color)
    
    if color.isValid():
        for item in selected_nodes:
            assert item.brush().color() == color
    else:
        for item in selected_nodes:
            assert item.brush().color() != color
    for item in not_selected_nodes:
        assert item.brush().color() != color
        
        
@pytest.mark.parametrize("radius", [0, 25, 35, 100])
def test_scene_set_selected_nodes_radius(scene, radius):
    """Check that setSelectedNodesRadius modify only the radius of selected nodes"""
    
    for node in scene.nodes():
        assert node.radius() != radius
    
    selected_nodes = set()
    not_selected_nodes = set()
    for i, node in enumerate(scene.nodes()):
        if i % 2 == 0:
            node.setSelected(True)
            selected_nodes.add(node)
        else:
            not_selected_nodes.add(node)
            
    scene.setSelectedNodesRadius(radius)
    
    for item in selected_nodes:
        assert item.radius() == radius
    for item in not_selected_nodes:
        assert item.radius() != radius
    
        
@pytest.mark.parametrize("colors", [[QColor(i) for i in range(2, 12)],
                                    [QColor(i) for i in range(2, 10)],
                                    [QColor() for i in range(10)]])
def test_scene_set_nodes_colors(scene, colors):
    """Check that setNodesColors change colors for all nodes."""
    
    default = scene.nodes()[0].brush().color()
    
    scene.setNodesColors(colors)
    if len(colors) >= len(scene.nodes()):
        for i, node in enumerate(scene.nodes()):
            if colors[i].isValid():
                assert node.brush().color() == colors[i]
            else:
                assert node.brush().color() == default
        assert scene.nodesColors() == colors
    else:
        for node in scene.nodes():
            assert node.brush().color() == default
            
@pytest.mark.parametrize("radii", [[i for i in range(2, 12)],
                                   [i for i in range(2, 10)],
                                   [0 for i in range(10)]])
def test_scene_set_nodes_radii(scene, radii):
    """Check that setNodesRadii change radii for all nodes."""
    
    default = scene.nodes()[0].radius()
       
    scene.setNodesRadii(radii)
    if len(radii) >= len(scene.nodes()):
        for i, node in enumerate(scene.nodes()):
            assert node.radius() == radii[i]
        assert scene.nodesRadii() == radii
    else:
        for node in scene.nodes():
            assert node.radius() == default
            
            
def test_scene_nodes(scene):
    """Check that nodes are sorted by index."""
    
    nodes = scene.nodes()
    for i, node in enumerate(nodes):
        assert node.index() == i
        
        
def test_scene_edges(scene):
    """Check that nodes are sorted by index."""
    
    edges = scene.edges()
    for i, edge in enumerate(edges):
        assert edge.index() == i
            
            
def test_scene_selected_nodes(scene):
    """Check that selectedNodes returns only selected nodes."""
    
    nodes = scene.nodes()
    selected_nodes = set()
    for i in range(0, len(nodes), 2):
        nodes[i].setSelected(True)
        selected_nodes.add(nodes[i])
    
    r = scene.selectedNodes()
    assert set(r) == selected_nodes
    
    
def test_scene_selected_edges(scene):
    """Check that selectedEdges returns only selected edges."""
    
    edges = scene.edges()
    selected_edges = set()
    for i in range(0, len(edges), 2):
        edges[i].setSelected(True)
        selected_edges.add(edges[i])
    
    r = scene.selectedEdges()
    assert set(r) == selected_edges


def test_scene_paint_no_scene(mod, qtbot):
    """Check that painting scene does not throw an error."""
    
    v = mod.NetworkView()
    qtbot.addWidget(v)
    v.show()
    qtbot.waitForWindowShown(v)
    
 
@pytest.mark.parametrize('select, span_angle',
                         [
                             [False, 0],
                             [True, 0],
                             [False, 15],
                             [False, 0]
                         ])
def test_scene_paint(mod, scene, qtbot, select, span_angle):
    """Check that painting scene does not throw an error."""
    
    v = mod.NetworkView()
    qtbot.addWidget(v)
    v.setScene(scene)
    n = scene.nodes()[0]
    n.setSelected(select)
    n.setSpanAngle(span_angle)
    
    e = scene.edges()[0]
    e.setSelected(True)
    
    v.show()
    qtbot.waitForWindowShown(v)
    
    
@pytest.mark.parametrize('pies, set_nodes_colors',
                         [
                            [None, False], [[0., .2], False], [[.5, .6], True]
                         ])
def test_scene_paint_pies(mod, scene, qtbot, pies, set_nodes_colors):
    """Check that painting scene with nodes pies does not throw an error."""
    
    v = mod.NetworkView()
    qtbot.addWidget(v)
    v.setScene(scene)
    n = scene.nodes()[0]
    if set_nodes_colors: # Setting pies without settings scene nodes colors should be fine
        scene.setPieColors([QColor() for p in pies])
    if pies is not None:
        n.setPie(pies)

    v.show()
    qtbot.waitForWindowShown(v)
    
    
@pytest.mark.parametrize("molecule", MOLECULES)
def test_scene_paint_pixmap(mod, scene, qtbot, molecule):
    """Check that painting scene with nodes pies does not throw an error."""
    
    v = mod.NetworkView()
    qtbot.addWidget(v)
    v.setScene(scene)
    n = scene.nodes()[0]
    n.setPixmap(QPixmap(molecule['image']))
            
    v.show()
    qtbot.waitForWindowShown(v)


def test_scene_selected_nodes_bounding_rect(scene):
    """Check that selectedNodesBoundingRect increase as new nodes are selected."""
    
    bounding_rect = scene.selectedNodesBoundingRect()
    assert bounding_rect.isNull()
    for node in scene.nodes():
        node.setSelected(True)
        new_bounding_rect = scene.selectedNodesBoundingRect()
        if not bounding_rect.isNull():
            assert new_bounding_rect.contains(bounding_rect)
        bounding_rect = new_bounding_rect
        
    for node in scene.nodes():
        new_bounding_rect = scene.selectedNodesBoundingRect()
        assert new_bounding_rect == bounding_rect
        bounding_rect = new_bounding_rect
        
        
def test_scene_items_bounding_rect(mod):
    """Check that selectedNodesBoundingRect increase as new nodes are selected."""
    
    scene = mod.NetworkScene()
    bounding_rect = scene.itemsBoundingRect()
    assert bounding_rect.isNull()
    
    for i in range(10):
        node = mod.Node(i)
        scene.addNode(node)
        node.setPos(i*2, i*i)
        new_bounding_rect = scene.itemsBoundingRect()
        if not bounding_rect.isNull():
            assert new_bounding_rect.contains(bounding_rect)
        bounding_rect = new_bounding_rect
        
    nodes = scene.nodes()
    for node in nodes:
        scene.removeItem(node)
        new_bounding_rect = scene.itemsBoundingRect()
        print(bounding_rect, new_bounding_rect)
        if not new_bounding_rect.isNull():
            assert bounding_rect.contains(new_bounding_rect)
        bounding_rect = new_bounding_rect


def test_scene_lock(scene, qtbot):
    """Check that nodes in a locked scene can't be moved."""
    
    assert not scene.isLocked()
    for node in scene.nodes():
        assert node.flags() & QGraphicsItem.ItemIsMovable
        
    with qtbot.waitSignal(scene.locked, check_params_cb=lambda lock: lock):
        scene.lock(True)
    assert scene.isLocked()
    for node in scene.nodes():
        assert node.flags() | QGraphicsItem.ItemIsMovable
        
    with qtbot.waitSignal(scene.locked, check_params_cb=lambda lock: not lock):
        scene.lock(False)
    assert not scene.isLocked()
    for node in scene.nodes():
        assert node.flags() & QGraphicsItem.ItemIsMovable
        
    with qtbot.waitSignal(scene.locked, check_params_cb=lambda lock: lock):
        scene.lock()
    assert scene.isLocked()
    for node in scene.nodes():
        assert node.flags() | QGraphicsItem.ItemIsMovable
        
    with qtbot.assertNotEmitted(scene.locked):
        scene.lock()
    assert scene.isLocked()
    for node in scene.nodes():
        assert node.flags() | QGraphicsItem.ItemIsMovable
        
        
@pytest.mark.parametrize("scale", [-1, 0, 1, 0.245, 1000])
@pytest.mark.parametrize("k", [0, 1, 5, 10])
def test_scene_set_layout(scene, qtbot, scale, k):
    """Check that setLayout change nodes positions."""
    
    for node in scene.nodes():
        x, y = POSITIONS[node.index()]
        assert node.pos().x() == x
        assert node.pos().y() == y
    
    positions = np.asarray([(random.randrange(0, 100), random.randrange(0, 100)) for _ in scene.nodes()])
    isolated_nodes = random.choices([node.index() for node in scene.nodes()], k=k)
    
    with qtbot.waitSignal(scene.layoutChanged):
        scene.setLayout(positions, scale, isolated_nodes)
    
    effective_scale = scale if scale > 0 else scene.scale()
    
    for node in scene.nodes():
        if node.index() in isolated_nodes:
            x, y = POSITIONS[node.index()]
            assert node.pos().x() == pytest.approx(x)
            assert node.pos().y() == pytest.approx(y)
        else:
            x, y = positions[node.index()]
            assert node.pos().x() == pytest.approx(x * effective_scale)
            assert node.pos().y() == pytest.approx(y * effective_scale)
     
     
@pytest.mark.parametrize("positions", [[], [(0, 0), (1, 1), (2,2)], None],
                         ids= ["emptyList", "lessThanNodes", "biggerThanNodes"])
def test_scene_set_layout_list(scene, qtbot, positions):
    """calling setLayout with a list instead of numpy array should work.
    If list is smaller than the list of nodes in the scene, nothing should be done."""
       
    if positions is None:
        positions = [(random.randrange(0, 100), random.randrange(0, 100)) for _ in range(len(scene.nodes())*2)]
        
    nodes = scene.nodes()
        
    if len(positions) < len(nodes):
        with qtbot.assertNotEmitted(scene.layoutChanged):
            scene.setLayout(positions)
        positions = POSITIONS.copy()
    else:
        with qtbot.waitSignal(scene.layoutChanged):
            scene.setLayout(positions)
    
    for node in scene.nodes():
        x, y = positions[node.index()]
        assert node.pos().x() == pytest.approx(x)
        assert node.pos().y() == pytest.approx(y)
    
        
@pytest.mark.parametrize("scale", [-1, 0, 1, 0.245, 1000])
def test_scene_set_layout_no_flags_change(scene, qtbot, scale):
    """Check that setLayout don't change ItemIsMovable flag of nodes."""
    
    flags = {}
    for node in scene.nodes():
        flags[node.index()] = node.flags() | QGraphicsItem.ItemIsMovable
    
    positions = np.asarray([(random.randrange(0, 100), random.randrange(0, 100)) for _ in scene.nodes()])
    
    with qtbot.waitSignal(scene.layoutChanged):
        scene.setLayout(positions, scale)
    for node in scene.nodes():
        assert node.flags() | QGraphicsItem.ItemIsMovable == flags[node.index()]
    
    scene.lock(not scene.lock())
    with qtbot.waitSignal(scene.layoutChanged):
        scene.setLayout(positions, scale)
    for node in scene.nodes():
        assert node.flags() | QGraphicsItem.ItemIsMovable == flags[node.index()]
    
    scene.lock(not scene.lock())
    with qtbot.waitSignal(scene.layoutChanged):
        scene.setLayout(positions, scale)
    for node in scene.nodes():
        assert node.flags() | QGraphicsItem.ItemIsMovable == flags[node.index()]
        
        
def test_scene_render(scene):
    """Check that scene render set DeviceCoordinateCache nodes flag back."""
            
    image = QImage(QSize(20, 20), QImage.Format_ARGB32)
    painter = QPainter(image)
    scene.render(painter)
    painter.end()
    
    for node in scene.nodes():
        assert node.flags() | QGraphicsItem.DeviceCoordinateCache
    
