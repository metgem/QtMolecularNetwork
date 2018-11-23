from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt

import pytest

@pytest.mark.parametrize("width", [None, 0, 0.24, 1, 10])
def test_edge_init(mod, width):
    """Check initialization of Edge."""

    node1 = mod.Node(0, "")
    node2 = mod.Node(1, "")
    if width is not None:
        edge = mod.Edge(5, node1, node2, width)
    else:
        edge = mod.Edge(5, node1, node2)
        
    assert edge.index() == 5
    assert edge.sourceNode() == node1
    assert edge.destNode() == node2
        
    if width is not None:
        assert edge.width() == width
    else:
        assert edge.width() == 1
        
    assert isinstance(edge.pen(), QPen)
          
          
def test_edge_add(mod):
    """Check node/edge link."""
    
    node1 = mod.Node(54)
    node2 = mod.Node(72)
    node3 = mod.Node(96)
    node4 = mod.Node(456)
    
    edge1 = mod.Edge(0, node1, node2)
    assert node1.edges() == {edge1}
    assert node2.edges() == {edge1}
    assert node3.edges() == set()
    assert edge1.sourceNode() == node1
    assert edge1.destNode() == node2
    
    edge2 = mod.Edge(1, node1, node3)
    assert node1.edges() == {edge1, edge2}
    assert node2.edges() == {edge1}
    assert node3.edges() == {edge2}
    assert edge2.sourceNode() == node1
    assert edge2.destNode() == node3

    edge3 = mod.Edge(2, node2, node3)
    assert node1.edges() == {edge1, edge2}
    assert node2.edges() == {edge1, edge3}
    assert node3.edges() == {edge2, edge3}
    assert edge3.sourceNode() == node2
    assert edge3.destNode() == node3
    
    edge4 = mod.Edge(3, node4, node4)
    assert node4.edges() == {edge4}
    assert edge4.sourceNode() == edge4.destNode() == node4

    
def test_edge_set_node(mod):
    """Check that setSourceNode/setDestNode successfully change source/destination node."""
    
    node1 = mod.Node(65)
    node2 = mod.Node(41)
    node3 = mod.Node(58)
    node4 = mod.Node(58)
    
    edge = mod.Edge(0, node1, node2)
    assert edge.sourceNode() == node1
    assert edge.destNode() == node2
    assert node1.edges() == node2.edges() == {edge}
    assert node3.edges() == node4.edges() == set()
    
    edge.setSourceNode(node3)
    assert edge.sourceNode() == node3
    assert edge.destNode() == node2
    assert node1.edges() == set()
    assert node2.edges() == {edge}
    assert node3.edges() == {edge}
    assert node4.edges() == set()
    
    edge.setDestNode(node4)
    assert edge.sourceNode() == node3
    assert edge.destNode() == node4
    assert node1.edges() == set()
    assert node2.edges() == set()
    assert node3.edges() == {edge}
    assert node4.edges() == {edge}
    

def test_edge_set_pen(mod):
    """Check that pen can be changed."""
    
    node1 = mod.Node(96)
    node2 = mod.Node(75)
    edge = mod.Edge(0, node1, node2)
    
    assert isinstance(edge.pen(), QPen)
    
    width = edge.width()
    pen = QPen(Qt.red)
    pen.setWidth(150)
    edge.setPen(pen)
    assert edge.pen().color().name() == '#ff0000'
    assert edge.width() == width
    
    
@pytest.mark.parametrize("width", [0, 0.24, 1, 10])
def test_edge_set_width(mod, width):
    """Check that edge width can be changed."""
    
    node1 = mod.Node(84)
    node2 = mod.Node(63)
    edge = mod.Edge(0, node1, node2)
    
    edge.setWidth(width)
    
    assert edge.width() == width
