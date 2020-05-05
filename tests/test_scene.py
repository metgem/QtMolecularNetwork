from PyQt5.QtGui import QPen, QColor, QStandardItemModel, QStandardItem, QPixmap, QPainter
from PyQt5.QtCore import Qt, QPoint


import pytest
import hashlib

from resources import MOLECULES
  
@pytest.fixture
def scene(mod, qapp):
    scene = mod.NetworkScene()
    scene.addNodes(range(10), positions=[QPoint(i, i+1) for i in range(10)])
    sources = scene.nodes()[:5]
    dests = scene.nodes()[5:]
    scene.addEdges(range(5), sources, dests, range(5))

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
    
    
@pytest.mark.parametrize("indexes, labels, positions, colors, radii",
    [ (range(10), None, None, None, None),
      ([0, 1], ["0", "1"], None, None, None),
      ([0, 1], None, [QPoint(0, 1), QPoint(5,2)], None, None),
      ([0, 1], None, None, [QColor(Qt.red), QColor(Qt.blue)], None),
      ([0, 1], None, None, None, [5, 20]),
    ])
def test_scene_add_nodes(mod, indexes, labels, positions, colors, radii):
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
    
    scene.addNodes(indexes, **kwargs)
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
            
            
@pytest.mark.parametrize("width", [0, 0.24, 1, 10])
def test_scene_add_edges(mod, width):
    """Check that edges can be added to the scene."""
    
    scene = mod.NetworkScene()
    scene.addNodes(range(10))
    sources = scene.nodes()[:5]
    dests = scene.nodes()[5:]
    scene.addEdges(range(5), sources, dests, [width] * 5)
    assert len(scene.edges()) == 5
    edges = scene.edges()
    for i in range(5):
        assert edges[i].index() == i
        assert edges[i].width() == width
        assert edges[i].sourceNode() == sources[i]
        assert edges[i].destNode() == dests[i]
        
        
def test_scene_remove_all_nodes(scene):
    """Check that nodes can be removed from the scene."""
       
    assert len(scene.nodes()) == 10
    scene.removeAllNodes()
    assert len(scene.nodes()) == 0
    

def test_scene_remove_all_edges(scene):
    """Check that edges can be removed from the scene."""
    
    assert len(scene.edges()) == 5
    scene.removeAllEdges()
    assert len(scene.edges()) == 0
    

def test_scene_remove_nodes(scene):
    """Check that specific nodes can be removed from the scene."""
       
    nodes = scene.nodes()
    assert len(nodes) == 10
    for i in range(5):
        scene.removeNodes([nodes[i], nodes[i+5]])
        assert len(scene.nodes()) == 10 - (i+1)*2
        assert nodes[i] not in scene.nodes()
        assert nodes[i+5] not in scene.nodes()
    assert len(scene.nodes()) == 0
    

def test_scene_remove_edges(scene):
    """Check that specific edges can be removed from the scene."""
       
    edges = scene.edges()
    assert len(edges) == 5
    for i in range(5):
        scene.removeEdges([edges[i]])
        assert len(scene.edges()) == 5 - i - 1
        assert edges[i] not in scene.edges()
    assert len(scene.edges()) == 0
    

@pytest.mark.parametrize("scale", [0, 1, 0.245, 1000])
def test_scene_set_scale(scene, scale):
    """Check that scale can be changed."""
    
    for node in scene.nodes():
        assert node.pos().x() == node.index()
        assert node.pos().y() == node.index() + 1
        
    scene.setScale(scale)
    
    scale = 1 if scale <= 0 else scale
    
    for node in scene.nodes():
        assert node.pos().x() == pytest.approx(node.index() * scale)
        assert node.pos().y() == pytest.approx((node.index() + 1) * scale)
        
    scene.setScale(1)
    
    for node in scene.nodes():
        assert node.pos().x() == pytest.approx(node.index())
        assert node.pos().y() == pytest.approx(node.index() + 1)
        
        
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
        

def test_scene_set_pie_colors(scene):
    """Check that setPieColors change colors."""
    
    colors = [QColor(i) for i in range(2, 12)]
    
    scene.setPieColors(colors)
    assert scene.pieColors() == colors
    

@pytest.mark.parametrize("colors", [[QColor(i) for i in range(2, 7)],
                                    [QColor(i) for i in range(2, 6)]])
@pytest.mark.parametrize("role", [Qt.DisplayRole, Qt.UserRole+1])
def test_scene_set_pie_charts_from_model(scene, colors, role):
    """Check that setLabelsFromModel change pie charts on all nodes."""
    
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
