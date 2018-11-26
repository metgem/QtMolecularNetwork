from PyQt5.QtGui import QPen, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QPoint

import pytest

@pytest.fixture
def style(mod):
    node = {'bgcolor': {'normal': QBrush(Qt.red),
                        'selected': QBrush(Qt.green)},
            'txtcolor': {'normal': QColor(Qt.blue),
                        'selected': QColor(Qt.darkYellow)},
            'border': {'normal': QPen(Qt.darkMagenta, 10, Qt.DashLine),
                       'selected': QPen(Qt.magenta, 45, Qt.DotLine)},
            'font': {'normal': QFont('Times', 60),
                     'selected': QFont('Helvetica', 42)},
            }
    edge = {'color': {'normal': QPen(QColor(Qt.darkRed)),
                    'selected': QPen(QColor(Qt.cyan))}}
    scene = {'color': QBrush(Qt.darkCyan)}
        
    return mod.NetworkStyle("test", node, edge, scene)
    
    
@pytest.fixture
def css(tmpdir):
    p = tmpdir.mkdir("css").join("style.css")
    content = \
"""/* name: test */

node
{
    background-color: #ff0000;
    color: #0000ff;
    border: dashed #800080 10px;
    font: Times 60pt;
}

node:selected
{
    background-color: #00ff00;
    color: #808000;
    border: dotted #ff00ff 45px;
    font: Helvetica 42pt;
}

edge
{
    background-color: #800000;
}

edge:selected
{
    background-color: #00ffff;
}

scene
{
    background-color: #008080;
}
"""
    p.write(content)
    
    return p
    
    
def check_style(style):
    assert style.styleName() == "test"
    assert style.nodeBrush("normal") == QBrush(Qt.red)
    assert style.nodeBrush("selected") == QBrush(Qt.green)
    assert style.nodeTextColor("normal") == QColor(Qt.blue)
    assert style.nodeTextColor("selected") == QColor(Qt.darkYellow)
    assert style.nodePen("normal") == QPen(Qt.darkMagenta, 10, Qt.DashLine)
    assert style.nodePen("selected") == QPen(Qt.magenta, 45, Qt.DotLine)
    assert style.nodeFont("normal") == QFont('Times', 60)
    assert style.nodeFont("selected") == QFont('Helvetica', 42)
    assert style.edgePen("normal") == QPen(QColor(Qt.darkRed))
    assert style.edgePen("selected") == QPen(QColor(Qt.cyan))
    assert style.backgroundBrush() == QBrush(Qt.darkCyan)
   
   
def test_style_init(mod, style, qapp):
    """Check initialization of style."""
    
    check_style(style)
    

def test_style_default_init(mod):
    """Check initialization of default style."""
    
    style = mod.DefaultStyle()
    assert style.styleName() == "default"
    assert isinstance(style.nodeBrush("normal"), QBrush)
    assert isinstance(style.nodeBrush("selected"), QBrush)
    assert id(style.nodeBrush("normal")) != id(style.nodeBrush("selected"))
    assert isinstance(style.nodeTextColor("normal"), QColor)
    assert isinstance(style.nodeTextColor("selected"), QColor)
    assert id(style.nodeTextColor("normal")) != id(style.nodeTextColor("selected"))
    assert isinstance(style.nodePen("normal"), QPen)
    assert isinstance(style.nodePen("selected"), QPen)
    assert id(style.nodePen("normal")) != id(style.nodePen("selected"))
    assert isinstance(style.nodeFont("normal"), QFont)
    assert isinstance(style.nodeFont("selected"), QFont)
    assert id(style.nodeFont("normal")) != id(style.nodeFont("selected"))
    assert isinstance(style.edgePen("normal"), QPen)
    assert isinstance(style.edgePen("selected"), QPen)
    assert id(style.edgePen("normal")) != id(style.edgePen("selected"))
    assert isinstance(style.backgroundBrush(), QBrush)

    
def test_style_set_style(mod, style):
    """Check that networkStyle can be changed."""
        
    scene = mod.NetworkScene()
    scene.addNodes(range(10))
    sources = scene.nodes()[:5]
    dests = scene.nodes()[5:]
    scene.addEdges(range(5), sources, dests, range(5))
    assert scene.networkStyle() != style
    scene.setNetworkStyle(style)
    assert scene.networkStyle() == style
    for node in scene.nodes():
        assert node.brush() == style.nodeBrush()
        assert node.textColor() == style.nodeTextColor()
        assert node.pen() == style.nodePen()
        assert node.font() == style.nodeFont()
        
    for edge in scene.edges():
        assert edge.pen().color() == style.edgePen().color()
        
    assert scene.backgroundBrush() == style.backgroundBrush()
    

def test_style_css(mod, css):
    """Test reading style from css."""

    style = mod.style_from_css(str(css))
    
    check_style(style)
    
    
def test_style_to_json(mod, style):
    json = mod.style_to_json(style)
    
    assert json['title'] == "test"
    selectors = {s['selector'] for s in json['style']}
    assert selectors == {'node', 'node:selected', 'edge', 'edge:selected'}
    for s in json['style']:
        if ':' in s['selector']:
            selector, state = s['selector'].split(':')
        else:
            selector, state = s['selector'], 'normal'
            
        css = s['css']
        
        if selector == 'node':
            assert css['background-color'] == style.nodeBrush(state).color().name()
            assert css['border-width'] == style.nodePen(state).width()
            assert css['font-size'] == style.nodeFont(state).pointSize()
            assert css['width'] == css['height'] == mod.RADIUS * 2
            assert css['color'] == style.nodeTextColor(state).name()
            assert css['border-color'] == style.nodePen(state).color().name()
            assert css['font-family'] == style.nodeFont(state).family()
            # assert css['font-weight'] == style.nodeFont(state).weight() # TODO
            
            if state == 'normal':
                assert css['text-opacity'] == 1.0
                assert css['text-valign'] == 'center'
                assert css['text-halign'] == 'center'
                assert css['shape'] == 'ellipse'
                assert css['border-opacity'] == 1.0
                assert css['background-opacity'] == 1.0
                assert css['content'] == "data(name)"                
        elif selector == 'edge':            
            assert css['line-color'] == style.edgePen(state).color().name()
            # assert css['line-style'] == style.edgePen(state).style() #TODO
            
            if state == 'normal':
                assert css['opacity'] == 1.0
                assert css['text-opacity'] == 1.0
                assert css['content'] == 'data(interaction)'
                
                
def test_style_to_cytoscape(mod, style):
    c = mod.style_to_cytoscape(style)
    
    assert c['title'].endswith("-" + style.styleName())
    for prop in c['defaults']:
        name, value = prop['visualProperty'], prop['value']
        
        if name == 'COMPOUND_NODE_SHAPE':
            assert value == 'ROUND_RECTANGLE'
        elif name == 'EDGE_LABEL':
            assert value == ''
        # elif name == 'EDGE_LINE_TYPE':
            # assert value == style.edgePen().style()
        elif name == 'EDGE_PAINT':
            assert value == style.edgePen().color().name()
        elif name == 'EDGE_SELECTED_PAINT':
            assert value == style.edgePen('selected').color().name()
        elif name == 'EDGE_VISIBLE':
            assert value == True
        elif name == 'EDGE_SELECTED':
            assert value == False
        elif name in ('EDGE_SOURCE_ARROW_UNSELECTED_PAINT',
                      'EDGE_TARGET_ARROW_UNSELECTED_PAINT',
                      'EDGE_STROKE_UNSELECTED_PAINT'):
            assert value == style.edgePen().color().name()
        elif name in ('EDGE_SOURCE_ARROW_SELECTED_PAINT',
                      'EDGE_TARGET_ARROW_SELECTED_PAINT',
                      'EDGE_STROKE_SELECTED_PAINT'):
            assert value == style.edgePen('selected').color().name()
        elif name == 'NETWORK_BACKGROUND_PAINT':
            assert value == style.backgroundBrush().color().name()
        elif name == 'NODE_BORDER_PAINT':
            assert value == style.nodePen().color().name()
        # elif name == 'NODE_BORDER_STROKE':
            # assert value == style.nodePen().style()
        elif name == 'NODE_BORDER_WIDTH':
            assert value == style.nodePen().width()
        elif name == 'NODE_FILL_COLOR':
            assert value == style.nodeBrush().color().name()
        elif name in ('NODE_HEIGHT', 'NODE_WIDTH', 'NODE_SIZE'):
            assert value == mod.RADIUS * 2
        elif name == 'NODE_LABEL_COLOR':
            assert value == style.nodeTextColor().name()
        elif name == 'NODE_LABEL_FONT_FACE':
            assert value == style.nodeFont().family()
        elif name == 'NODE_LABEL_FONT_SIZE':
            assert value == style.nodeFont().pointSize()
        elif name == 'NODE_PAINT':
            assert value == style.nodeBrush().color().name()
        elif name == 'NODE_SELECTED_PAINT':
            assert value == style.nodeBrush('selected').color().name()
        elif name == 'NODE_SHAPE':
            assert value == 'ELLIPSE'
