from PySide2.QtGui import QPen, QColor, QBrush, QFont
from PySide2.QtCore import Qt, QPoint
import PySide2MolecularNetwork

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
    assert style.nodeBrush() == QBrush(Qt.red)
    assert style.nodeBrush(selected=True) == QBrush(Qt.green)
    assert style.nodeTextColor() == QColor(Qt.blue)
    assert style.nodeTextColor(selected=True) == QColor(Qt.darkYellow)
    assert style.nodePen() == QPen(Qt.darkMagenta, 10, Qt.DashLine)
    assert style.nodePen(selected=True) == QPen(Qt.magenta, 45, Qt.DotLine)
    assert style.nodeFont() == QFont('Times', 60)
    assert style.nodeFont(selected=True) == QFont('Helvetica', 42)
    assert style.edgePen() == QPen(QColor(Qt.darkRed))
    assert style.edgePen(selected=True) == QPen(QColor(Qt.cyan))
    assert style.backgroundBrush() == QBrush(Qt.darkCyan)
   
   
def compare_styles(style, ref_style):
    assert style.styleName() == ref_style.styleName()
    assert style.nodeBrush() == ref_style.nodeBrush()
    assert style.nodeBrush(selected=True) == ref_style.nodeBrush(selected=True)
    assert style.nodeTextColor() == ref_style.nodeTextColor()
    assert style.nodeTextColor(selected=True) == ref_style.nodeTextColor(selected=True)
    assert style.nodePen() == ref_style.nodePen()
    assert style.nodePen(selected=True) == ref_style.nodePen(selected=True)
    assert style.nodeFont() == ref_style.nodeFont()
    assert style.nodeFont(selected=True) == ref_style.nodeFont(selected=True)
    assert style.edgePen() == ref_style.edgePen()
    assert style.edgePen(selected=True) == ref_style.edgePen(selected=True)
    assert style.backgroundBrush() == ref_style.backgroundBrush()
    
def test_style_init(mod, style, qapp):
    """Check initialization of style."""
    
    check_style(style)
    

def test_style_default_init(mod):
    """Check initialization of default style."""
    
    style = mod.DefaultStyle()
    assert style.styleName() == "default"
    
    assert isinstance(style.nodeBrush(), QBrush)
    assert style.nodeBrush().color().isValid()
    assert isinstance(style.nodeBrush(selected=True), QBrush)
    assert style.nodeBrush(selected=True).color().isValid()
    assert id(style.nodeBrush()) != id(style.nodeBrush(selected=True))
    
    assert isinstance(style.nodeTextColor(), QColor)
    assert style.nodeTextColor().isValid()
    assert isinstance(style.nodeTextColor(selected=True), QColor)
    assert style.nodeTextColor(selected=True).isValid()
    assert id(style.nodeTextColor()) != id(style.nodeTextColor(selected=True))
    
    assert isinstance(style.nodePen(), QPen)
    assert style.nodePen().color().isValid()
    assert isinstance(style.nodePen(selected=True), QPen)
    assert style.nodePen(selected=True).color().isValid()
    assert id(style.nodePen()) != id(style.nodePen(selected=True))
    
    assert isinstance(style.nodeFont(), QFont)
    assert isinstance(style.nodeFont(selected=True), QFont)
    assert id(style.nodeFont()) != id(style.nodeFont(selected=True))
    
    
    assert isinstance(style.edgePen(), QPen)
    assert style.edgePen().color().isValid()
    assert isinstance(style.edgePen(selected=True), QPen)
    assert style.edgePen(selected=True).color().isValid()
    assert id(style.edgePen()) != id(style.edgePen(selected=True))
    
    assert isinstance(style.backgroundBrush(), QBrush)
    assert style.backgroundBrush().color().isValid()
    
    
def test_style_empty_dicts(mod):
    """Using empty dict should give the same results than no dict at all."""
    
    with pytest.not_raises(KeyError):
        style = mod.NetworkStyle("", {}, {}, {})
    
    compare_styles(style, mod.NetworkStyle())
    
@pytest.mark.parametrize('value', [None, {}])
def test_style_broken_dicts(mod, value):
    """Using invalid dicts should give the same results than no dict at all."""
    
    node = {'bgcolor': value, 'txtcolor': value, 'border': value, 'font': value}
    edge = {'color': value}
    
    with pytest.not_raises(KeyError):
        style = mod.NetworkStyle("", node, edge, {})
    
    compare_styles(style, mod.NetworkStyle())
    
    
def test_style_set_style(mod, style):
    """Check that networkStyle can be changed."""
        
    scene = mod.NetworkScene()
    scene.createNodes(range(10))
    sources = scene.nodes()[:5]
    dests = scene.nodes()[5:]
    scene.createEdges(range(5), sources, dests, range(5))
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
    
    
def test_style_setters(mod, style):
    """Check that style attributes can be changed."""
    
    name = style.styleName()
    name += "_new"
    style.setStyleName(name)
    assert style.styleName() == name
    
    for selected in (False, True):
        brush = QBrush(Qt.darkBlue)
        style.setNodeBrush(brush, selected=selected)
        assert style.nodeBrush(selected=selected) == brush
    
    for selected in (False, True):
        color = QColor(Qt.darkGreen)
        style.setNodeTextColor(color, selected=selected)
        assert style.nodeTextColor(selected=selected) == color
        
    for selected in (False, True):
        pen = QPen(Qt.darkYellow, 5, Qt.SolidLine)
        style.setNodePen(pen, selected=selected)
        assert style.nodePen(selected=selected) == pen
        
    for selected in (False, True):
        font = QFont('Arial', 10)
        style.setNodeFont(font, selected=selected)
        assert style.nodeFont(selected=selected) == font
        
    for selected in (False, True):
        pen = QPen(Qt.darkYellow, 5, Qt.SolidLine)
        style.setEdgePen(pen, selected=selected)
        assert style.edgePen(selected=selected) == pen
        
    brush = QBrush(Qt.darkRed)
    style.setBackgroundBrush(brush)
    assert style.backgroundBrush() == brush

def test_style_css(mod, css):
    """Test reading style from css."""

    style = mod.style_from_css(str(css))
    
    check_style(style)
    
    
@pytest.mark.parametrize('value', ["", "invalid", None])
def test_style_css_invalid_file(mod, value):
    """If file does not exists `style_from_css` should not throw an error
    but return `DefaultStyle`."""
    
    with pytest.not_raises(FileNotFoundError):
        style = mod.style_from_css(value)
        
    compare_styles(style, mod.DefaultStyle())
    
def test_style_css_no_tinycss(mod, css, monkeypatch):
    """If tinycss2 module is not found, `style_from_css` should return `DefaultStyle`"""
            
    assert PySide2MolecularNetwork.style.HAS_TINYCSS2 == True
    monkeypatch.setattr(PySide2MolecularNetwork.style, 'HAS_TINYCSS2', False)
    compare_styles(mod.style_from_css(str(css)), mod.DefaultStyle())
    
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
            
        selected = (state == 'selected')
        css = s['css']
        
        if selector == 'node':
            assert css['background-color'] == style.nodeBrush(selected=selected).color().name()
            assert css['border-width'] == style.nodePen(selected=selected).width()
            assert css['font-size'] == style.nodeFont(selected=selected).pointSize()
            assert css['width'] == css['height'] == mod.Config.Radius * 2
            assert css['color'] == style.nodeTextColor(selected=selected).name()
            assert css['border-color'] == style.nodePen(selected=selected).color().name()
            assert css['font-family'] == style.nodeFont(selected=selected).family()
            # assert css['font-weight'] == style.nodeFont(selected=selected).weight() # TODO
            
            if state == 'normal':
                assert css['text-opacity'] == 1.0
                assert css['text-valign'] == 'center'
                assert css['text-halign'] == 'center'
                assert css['shape'] == 'ellipse'
                assert css['border-opacity'] == 1.0
                assert css['background-opacity'] == 1.0
                assert css['content'] == "data(name)"                
        elif selector == 'edge':            
            assert css['line-color'] == style.edgePen(selected=selected).color().name()
            # assert css['line-style'] == style.edgePen(selected=selected).style() #TODO
            
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
            assert value == style.edgePen(selected=True).color().name()
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
            assert value == style.edgePen(selected=True).color().name()
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
            assert value == mod.Config.Radius * 2
        elif name == 'NODE_LABEL_COLOR':
            assert value == style.nodeTextColor().name()
        elif name == 'NODE_LABEL_FONT_FACE':
            assert value == style.nodeFont().family()
        elif name == 'NODE_LABEL_FONT_SIZE':
            assert value == style.nodeFont().pointSize()
        elif name == 'NODE_PAINT':
            assert value == style.nodeBrush().color().name()
        elif name == 'NODE_SELECTED_PAINT':
            assert value == style.nodeBrush(selected=True).color().name()
        elif name == 'NODE_SHAPE':
            assert value == 'ELLIPSE'
