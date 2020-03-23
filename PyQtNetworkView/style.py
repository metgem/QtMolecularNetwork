try:
    import tinycss2
except ImportError:
    HAS_TINYCSS2 = False
else:
    HAS_TINYCSS2 = True

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QColor, QFont, QPen, QBrush

from .config import RADIUS
    
class NetworkStyle:
    name = ""
    nb = QBrush(QColor(Qt.lightGray)) # Node Brush
    nbs = QBrush(QColor())            # Node Brush Selected
    ntc = QColor(Qt.black)            # Node Text Color
    ntcs = QColor()                   # Node Text Color Selected
    np = QPen(Qt.black, 1)            # Node Pen
    nps = QPen(Qt.black, 1)           # Node Pen Selected
    nf = QFont()                      # Node Font
    nfs = QFont()                     # Node Font Selected
    ep = QPen(Qt.darkGray)            # Edge Pen
    eps = QPen(Qt.red)                # Edge Pen Selected
    sb = QBrush(QColor(Qt.white))     # Scene Brush

    def __init__(self, name=None, node=None, edge=None, scene=None):
        if name is not None:
            self.name = name
            
        if node is not None:
            try:
                d = node['bgcolor']
                try:
                    self.nb = d["normal"]
                except KeyError:
                    pass
                try:
                    self.nbs = d["selected"]
                except KeyError:
                    pass
            except KeyError:
                pass
            
            try:
                d = node['txtcolor']
                try:
                    self.ntc = d["normal"]
                except KeyError:
                    pass
                try:
                    self.ntcs = d["selected"]
                except KeyError:
                    pass
            except KeyError:
                pass
                
            try:
                d = node['border']
                try:
                    self.np = d["normal"]
                except KeyError:
                    pass
                try:
                    self.nps = d["selected"]
                except KeyError:
                    pass
            except KeyError:
                pass
                
            try:
                d = node['font']
                try:
                    self.nf = d["normal"]
                except KeyError:
                    pass
                try:
                    self.nfs = d["selected"]
                except KeyError:
                    pass
            except KeyError:
                pass
        
        if edge is not None:
            try:
                d = edge['color']
                try:
                    self.ep = d["normal"]
                except KeyError:
                    pass
                try:
                    self.eps = d["selected"]
                except KeyError:
                    pass
            except KeyError:
                pass
                
        if scene is not None:
            try:
                self.sb = scene['color']
            except KeyError:
                pass
        
    def styleName(self):
        return self.name

    def nodeBrush(self, selected=False) -> QBrush:
        return self.nbs if selected else self.nb

    def nodeTextColor(self, selected: bool=False) -> QColor:
        return self.ntcs if selected else self.ntc

    def nodePen(self, selected: bool=False) -> QPen:
        return self.nps if selected else self.np

    def nodeFont(self, selected: bool=False) -> QFont:
        return self.nfs if selected else self.nf

    def edgePen(self, selected: bool=False) -> QPen:
        return self.eps if selected else self.ep

    def backgroundBrush(self) -> QBrush:
        return self.sb


class DefaultStyle(NetworkStyle):
    name = "default"
    node = {'bgcolor': {'normal': QBrush(Qt.lightGray),
                        'selected': QBrush(Qt.yellow)},
            'txtcolor': {'normal': QColor(Qt.black),
                         'selected': QColor(Qt.black)},
            'border': {'normal': QPen(Qt.black, 1, Qt.SolidLine),
                       'selected': QPen(Qt.black, 1, Qt.SolidLine)},
            'font': {'normal': QFont('Arial', 10),
                     'selected': QFont('Arial', 10)},
            }
    edge = {'color': {'normal': QPen(QColor(Qt.darkGray)),
                      'selected': QPen(QColor(Qt.red))}}
    scene = {'color': QBrush(Qt.white)}

# Code to load theme from css
CSS_FONT_WEIGHTS_TO_QT = {100: 0, 200: 12, 300: 25, 400: 50, 500: 57, 600: 63, 700: 75, 800: 81, 900: 87, 1000: 99,
                          'bold': QFont.Bold, 'bolder': QFont.ExtraBold, 'lighter': QFont.Light}
CSS_FONT_STYLES_TO_QT = {'normal': QFont.StyleNormal, 'italic': QFont.StyleItalic, 'oblique': QFont.StyleOblique}
CSS_FONT_VARIANTS_TO_QT = {'normal': QFont.MixedCase, 'small-caps': QFont.SmallCaps,
                           'capitalize': QFont.Capitalize, 'upper': QFont.AllUppercase,
                           'lower': QFont.AllLowercase}
CSS_BORDER_STYLES_TO_QT = {'solid': Qt.SolidLine, 'dashed': Qt.DashLine, 'dotted': Qt.DotLine, 'none': Qt.NoPen}

QT_FONT_WEIGHTS_TO_JSON = {QFont.Bold: 'bold', QFont.ExtraBold: 'bolder', QFont.Light: 'lighter'}
QT_BORDER_STYLES_TO_JSON = {v: k for k, v in CSS_BORDER_STYLES_TO_QT.items()}


def parse_rule(rule):
    name, state = None, 'normal'

    try:
        declaration = tinycss2.parse_one_declaration(rule.prelude, skip_comments=True)
        for token in declaration.value:
            if token.type == 'ident':
                name, state = declaration.name, token.value
    except (ValueError, TypeError, AttributeError):
        for token in rule.prelude:
            if token.type == 'ident':
                name = token.value

    if name is not None:
        for token in tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True):
            if token.type == 'declaration':
                for t in token.value:
                    yield name, state, token.name, t


def css_font_weight_to_qt(weight):
    try:
        weight = round(int(weight), -2)
    except ValueError:
        pass

    try:
        return CSS_FONT_WEIGHTS_TO_QT[weight]
    except KeyError:
        return


def read_css(css):
    if not HAS_TINYCSS2 or css is None:
        return

    try:
        with open(css, 'r') as f:
            sheet = tinycss2.parse_stylesheet(''.join(f.readlines()))
    except FileNotFoundError:
        return

    stylename = None
    node = {'bgcolor': {'normal': Qt.lightGray,
                        'selected': QColor()},
            'txtcolor': {'normal': Qt.black,
                         'selected': QColor()},
            'border': {'normal': {'style': Qt.SolidLine, 'width': 1, 'color': 'black'},
                       'selected': {'style': Qt.SolidLine, 'width': 1, 'color': 'black'}},
            'font': {'normal': {'family': 'Arial', 'variant': QFont.MixedCase, 'size': 10, 'unit': 'pt',
                                'style': QFont.StyleNormal, 'weight': QFont.Normal},
                     'selected': {'family': 'Arial', 'variant': QFont.MixedCase, 'size': 10, 'unit': 'pt',
                                  'style': QFont.StyleNormal, 'weight': QFont.Normal}}
            }
    edge = {'color': {'normal': Qt.darkGray, 'selected': Qt.red}}
    scene = {'color': Qt.white}

    for rule in sheet:
        if rule.type == 'comment' and stylename is None:
            try:
                stylename = rule.value.split('name: ')[1].strip()
            except IndexError:
                stylename = ""
        elif rule.type == 'qualified-rule':
            for name, state, prop, token in parse_rule(rule):
                if name == 'node':
                    if token.type == 'ident':
                        if prop == 'background-color':
                            node['bgcolor'][state] = token.value
                        elif prop == 'color':
                            node['txtcolor'][state] = token.value
                        elif prop == 'font-family':
                            node['font'][state]['family'] = token.value
                        elif prop == 'font-weight':
                            weight = css_font_weight_to_qt(token.value)
                            if weight is not None:
                                node['font'][state]['weight'] = weight
                        elif prop == 'font-style':
                            style = CSS_FONT_STYLES_TO_QT.get(token.value)
                            if style is not None:
                                node['font'][state]['style'] = style
                        elif prop == 'font-variant':
                            variant = CSS_FONT_VARIANTS_TO_QT.get(token.value)
                            node['font'][state]['variant'] = variant
                        elif prop == 'font':
                            style = CSS_FONT_STYLES_TO_QT.get(token.value)
                            if style is not None:
                                node['font'][state]['style'] = style
                            else:
                                variant = CSS_FONT_VARIANTS_TO_QT.get(token.value)
                                if variant is not None:
                                    node['font'][state]['variant'] = variant
                                else:
                                    weight = css_font_weight_to_qt(token.value)
                                    if weight is not None:
                                        node['font'][state]['weight'] = weight
                                    else:
                                        node['font'][state]['family'] = token.value
                        elif prop == 'border-style':
                            style = CSS_BORDER_STYLES_TO_QT.get(token.value)
                            node['border'][state]['style'] = style
                        elif prop == 'border-color':
                            node['border'][state]['color'] = token.value
                        elif prop == 'border':
                            style = CSS_BORDER_STYLES_TO_QT.get(token.value)
                            if style is not None:
                                node['border'][state]['style'] = style
                            else:
                                node['border'][state]['color'] = token.value
                    elif token.type == 'dimension':
                        if prop in ('font', 'font-size'):
                            node['font'][state]['size'] = token.value
                            node['font'][state]['unit'] = token.unit
                        elif prop in ('border', 'border-width'):
                            node['border'][state]['width'] = token.value
                    elif token.type == 'hash':
                        if prop == 'background-color':
                            node['bgcolor'][state] = token.serialize()
                        elif prop == 'color':
                            node['txtcolor'][state] = token.serialize()
                        elif prop in ('border', 'border-color'):
                            node['border'][state]['color'] = token.serialize()
                elif name == 'edge':
                    if token.type == 'ident':
                        if prop == 'background-color':
                            edge['color'][state] = token.value
                    elif token.type == 'hash':
                        if prop == 'background-color':
                            edge['color'][state] = token.serialize()
                elif name == 'scene':
                    if token.type == 'ident':
                        if prop == 'background-color':
                            scene['color'] = token.value
                    elif token.type == 'hash':
                        if prop == 'background-color':
                            scene['color'] = token.serialize()

    for state in ('normal', 'selected'):
        node['bgcolor'][state] = QBrush(QColor(node['bgcolor'][state]))
        node['txtcolor'][state] = QColor(node['txtcolor'][state])
        node['border'][state] = QPen(QBrush(QColor(node['border'][state]['color'])),
                                     node['border'][state]['width'],
                                     node['border'][state]['style'])
        f = QFont(node['font'][state]['family'])
        if node['font'][state]['unit'] == 'px':
            f.setPixelSize(node['font'][state]['size'])
        else:
            f.setPointSize(node['font'][state]['size'])
        f.setCapitalization(node['font'][state]['variant'])
        f.setWeight(node['font'][state]['weight'])
        f.setStyle(node['font'][state]['style'])
        node['font'][state] = f
        edge['color'][state] = QPen(QColor(edge['color'][state]))
    scene['color'] = QColor(scene['color'])

    return stylename, node, edge, scene

    
def style_from_css(css):
    result = read_css(css)
    
    if result is None:
        return DefaultStyle()
    
    return NetworkStyle(*result)
    

def style_to_json(style: NetworkStyle):
    style_dict = {"format_version": 1.0,
                  "generated_by": "{} {}".format(QCoreApplication.applicationName(), QCoreApplication.applicationVersion()),
                  "target_cytoscapejs_version": "~2.1",
                  "title": style.styleName(),
                  "style": [{
                      "selector": "node",
                      "css": {
                          "text-opacity": 1.0,
                          "background-color": style.nodeBrush().color().name(),
                          "text-valign": "center",
                          "text-halign": "center",
                          "border-width": style.nodePen().width(),
                          "font-size": style.nodeFont().pointSize(),
                          "width": RADIUS * 2,
                          "shape": "ellipse",
                          "color": style.nodeTextColor().name(),
                          "border-opacity": 1.0,
                          "height": RADIUS * 2,
                          "background-opacity": 1.0,
                          "border-color": style.nodePen().color().name(),
                          "font-family": style.nodeFont().family(),
                          "font-weight": QT_FONT_WEIGHTS_TO_JSON.get(style.nodeFont().weight(), 'normal'),
                          "content": "data(name)"
                      }
                  }, {
                      "selector": "node:selected",
                      "css": {
                          "background-color": style.nodeBrush('selected').color().name(),
                          "border-width": style.nodePen('selected').width(),
                          "font-size": style.nodeFont('selected').pointSize(),
                          "width": RADIUS * 2,
                          "color": style.nodeTextColor('selected').name(),
                          "height": RADIUS * 2,
                          "border-color": style.nodePen('selected').color().name(),
                          "font-family": style.nodeFont('selected').family(),
                          "font-weight": QT_FONT_WEIGHTS_TO_JSON.get(style.nodeFont('selected').weight(), 'normal')
                      }
                  }, {
                      "selector": "edge",
                      "css": {
                          "line-color": style.edgePen().color().name(),
                          "opacity": 1.0,
                          "line-style": QT_BORDER_STYLES_TO_JSON.get(style.edgePen().style(), 'solid'),
                          "text-opacity": 1.0,
                          "content": "data(interaction)"
                      }
                  }, {
                      "selector": "edge:selected",
                      "css": {
                          "line-color": style.edgePen('selected').color().name(),
                          "line-style": QT_BORDER_STYLES_TO_JSON.get(style.edgePen('selected').style(), 'solid'),
                      }
                  }]
                  }
    return style_dict


def style_to_cytoscape(style: NetworkStyle):
    return  {'title': QCoreApplication.applicationName() + "-" + style.styleName(),
                  'defaults':
                      [{'visualProperty': 'COMPOUND_NODE_SHAPE', 'value': 'ROUND_RECTANGLE'},
                       {'visualProperty': 'EDGE_LABEL', 'value': ''},
                       {'visualProperty': 'EDGE_LINE_TYPE', 'value': style.edgePen().style()},
                       {'visualProperty': 'EDGE_PAINT', 'value': style.edgePen().color().name()},
                       {'visualProperty': 'EDGE_SELECTED', 'value': False},
                       {'visualProperty': 'EDGE_SELECTED_PAINT', 'value': style.edgePen('selected').color().name()},
                       {'visualProperty': 'EDGE_VISIBLE', 'value': True},
                       {'visualProperty': 'EDGE_WIDTH', 'value': 12.0},
                       {'visualProperty': 'EDGE_SOURCE_ARROW_UNSELECTED_PAINT', 'value': style.edgePen().color().name()},
                       {'visualProperty': 'EDGE_TARGET_ARROW_UNSELECTED_PAINT', 'value': style.edgePen().color().name()},
                       {'visualProperty': 'EDGE_STROKE_UNSELECTED_PAINT', 'value': style.edgePen().color().name()},
                       {'visualProperty': 'EDGE_SOURCE_ARROW_SELECTED_PAINT', 'value': style.edgePen('selected').color().name()},
                       {'visualProperty': 'EDGE_TARGET_ARROW_SELECTED_PAINT', 'value': style.edgePen('selected').color().name()},
                       {'visualProperty': 'EDGE_STROKE_SELECTED_PAINT', 'value': style.edgePen('selected').color().name()},
                       {'visualProperty': 'NETWORK_BACKGROUND_PAINT', 'value': style.backgroundBrush().color().name()},
                       {'visualProperty': 'NETWORK_CENTER_X_LOCATION', 'value': 0.0},
                       {'visualProperty': 'NETWORK_CENTER_Y_LOCATION', 'value': 0.0},
                       {'visualProperty': 'NETWORK_CENTER_Z_LOCATION', 'value': 0.0},
                       {'visualProperty': 'NETWORK_DEPTH', 'value': 0.0},
                       {'visualProperty': 'NETWORK_EDGE_SELECTION', 'value': True},
                       {'visualProperty': 'NETWORK_HEIGHT', 'value': 400.0},
                       {'visualProperty': 'NETWORK_NODE_SELECTION', 'value': True},
                       {'visualProperty': 'NETWORK_SCALE_FACTOR', 'value': 1.0},
                       {'visualProperty': 'NETWORK_SIZE', 'value': 550.0},
                       {'visualProperty': 'NETWORK_TITLE', 'value': ''},
                       {'visualProperty': 'NETWORK_WIDTH', 'value': 550.0},
                       {'visualProperty': 'NODE_BORDER_PAINT', 'value': style.nodePen().color().name()},
                       {'visualProperty': 'NODE_BORDER_STROKE', 'value': style.nodePen().style()},
                       {'visualProperty': 'NODE_BORDER_TRANSPARENCY', 'value': 255},
                       {'visualProperty': 'NODE_BORDER_WIDTH', 'value': style.nodePen().width()},
                       {'visualProperty': 'NODE_DEPTH', 'value': 0.0},
                       {'visualProperty': 'NODE_FILL_COLOR', 'value': style.nodeBrush().color().name()},
                       {'visualProperty': 'NODE_HEIGHT', 'value': RADIUS*2},
                       {'visualProperty': 'NODE_LABEL', 'value': ''},
                       {'visualProperty': 'NODE_LABEL_COLOR', 'value': style.nodeTextColor().name()},
                       {'visualProperty': 'NODE_LABEL_FONT_FACE', 'value': style.nodeFont().family()},
                       {'visualProperty': 'NODE_LABEL_FONT_SIZE', 'value': style.nodeFont().pointSize()},
                       {'visualProperty': 'NODE_LABEL_TRANSPARENCY', 'value': 255},
                       {'visualProperty': 'NODE_NESTED_NETWORK_IMAGE_VISIBLE', 'value': True},
                       {'visualProperty': 'NODE_PAINT', 'value': style.nodeBrush().color().name()},
                       {'visualProperty': 'NODE_SELECTED', 'value': False},
                       {'visualProperty': 'NODE_SELECTED_PAINT', 'value': style.nodeBrush('selected').color().name()},
                       {'visualProperty': 'NODE_SHAPE', 'value': 'ELLIPSE'},
                       {'visualProperty': 'NODE_SIZE', 'value': RADIUS*2},
                       {'visualProperty': 'NODE_TOOLTIP', 'value': ''},
                       {'visualProperty': 'NODE_TRANSPARENCY', 'value': 255},
                       {'visualProperty': 'NODE_VISIBLE', 'value': True},
                       {'visualProperty': 'NODE_WIDTH', 'value': RADIUS*2},
                       {'visualProperty': 'NODE_X_LOCATION', 'value': 0.0},
                       {'visualProperty': 'NODE_Y_LOCATION', 'value': 0.0},
                       {'visualProperty': 'NODE_Z_LOCATION', 'value': 0.0}],
                  'mappings': [{'mappingType': 'passthrough',
                                'mappingColumn': 'interaction',
                                'mappingColumnType': 'String',
                                'visualProperty': 'EDGE_LABEL'},
                               {'mappingType': 'passthrough',
                                'mappingColumn': 'name',
                                'mappingColumnType': 'String',
                                'visualProperty': 'NODE_LABEL'}]}

