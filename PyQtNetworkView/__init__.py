"""
    A set of widgets based on QNetworkView and QNetworkScene for network visualization.
"""

try:
    IS_COMPILED = True
    from .NetworkView import (Node, Edge, RADIUS,
                              NetworkScene as BaseNetworkScene,
                              NetworkStyle, DefaultStyle)
    from .style import read_css, style_to_json, style_to_cytoscape
    
    import numpy as np
                              
    class NetworkScene(BaseNetworkScene):
        def setLayout(self, layout, scale=0, isolated_nodes=[]):
            if isinstance(layout, list):
                layout = np.asarray(layout)
                
            super().setLayout(layout.ravel(), scale,
                              isolated_nodes if isolated_nodes is not None else [])
            
    def style_from_css(css):
        result = read_css(css)
        
        if result is None:
            return DefaultStyle()
        
        return NetworkStyle(*result)
except ImportError:
    IS_COMPILED = False
    from .scene import Node, Edge, NetworkScene, RADIUS
    from .style import (NetworkStyle, DefaultStyle,
                        style_from_css, style_to_json, style_to_cytoscape)
    
from .view import NetworkView, MiniMapGraphicsView, disable_opengl
from .mol_depiction import SvgToPixmap, SmilesToPixmap, InchiToPixmap

from . import _version
__version__ = _version.get_versions()['version']
