import pytest

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsView, QWidget, QOpenGLWidget
import PyQtNetworkView

def test_view_init(view, mod):
    """Check initialization of NetworkView"""
    
    assert isinstance(view.scene(), mod.NetworkScene)
    assert isinstance(view.minimap, mod.MiniMapGraphicsView)
    assert view.minimap.parent() == view
    assert view.minimap.scene() == view.scene()
    

def test_view_left_mouse_press(view, qtbot):
    """Check mousePress and mouseRelease events with left button"""

    qtbot.mousePress(view.viewport(), Qt.LeftButton)
    assert view.dragMode() == QGraphicsView.ScrollHandDrag
    
    qtbot.mouseRelease(view.viewport(), Qt.LeftButton)
    assert view.dragMode() == QGraphicsView.NoDrag
    
    
def test_view_right_mouse_press(view, qtbot):
    """Check mousePress and mouseRelease events with right button"""
    
    qtbot.mousePress(view.viewport(), Qt.RightButton)
    assert view.dragMode() == QGraphicsView.RubberBandDrag
    assert view.rubberBandSelectionMode() == Qt.IntersectsItemBoundingRect
    
    qtbot.mouseRelease(view.viewport(), Qt.RightButton)
    assert view.dragMode() == QGraphicsView.NoDrag
    
    
@pytest.mark.parametrize("has_scene", [True, False], ids=["scene", "noscene"])
def test_view_mouse_move(view, qtbot, mocker, has_scene):
    """Check that rubber band is adjusted when mouse move"""
    
    if not has_scene:
        mocker.patch("PyQt5.QtWidgets.QGraphicsView.scene", return_value=None)
        assert view.scene() is None
    
    mocker.spy(view.minimap, 'adjustRubberband')
    qtbot.mousePress(view.viewport(), Qt.LeftButton, pos=view.rect().center())
    assert view.dragMode() == QGraphicsView.ScrollHandDrag
    qtbot.mouseMove(view.viewport(), pos=view.rect().center())
    assert view.minimap.adjustRubberband.call_count == 1
    
    
def test_view_mouse_wheel(view, qtbot, mocker):
    """Check that scaleView is called on mouse wheel event"""
    
    mocker.spy(view, 'scaleView')
    qtbot.mouseWheel(view.viewport())
    assert view.scaleView.call_count == 1
    
    
@pytest.mark.parametrize("x, y", [(0, 0), (5, 25), (8, 5)])
def test_view_translate(view, mocker, x, y):
    """Check that rubber band is adjusted when translate is called"""
    
    mocker.spy(view.minimap, 'adjustRubberband')
    view.translate(x, y)
    assert view.minimap.adjustRubberband.call_count == 1
    
    
def test_view_resize(view, qtbot, mocker):
    """Check that rubber band is adjusted when NetworkView is resized"""
    
    mocker.spy(view.minimap, 'adjustRubberband')
    qtbot.resizeWidget(view.viewport(), view.size()*2)
    assert view.minimap.adjustRubberband.call_count == 1
    
    
def test_view_focus_in(view, qtbot):
    """Check that focusedIn signal is sent when NetworkView gets focus"""
    
    with qtbot.waitSignal(view.focusedIn):
        qtbot.setFocus(view)
        
        
@pytest.mark.parametrize("scale", [0, 1, 0.245, 1000])
def test_view_set_scale(view, mocker, scale):
    """Check that changing scale results in calling zoomToFit and adjusting scene rect."""
    
    mocker.spy(view.minimap, 'zoomToFit')
    mocker.spy(view.scene(), 'setSceneRect')
    
    view.scene().setScale(scale)
    assert view.minimap.zoomToFit.call_count == 1
    assert view.scene().setSceneRect.call_count == 1
    
    
def test_view_set_layout(view, mocker):
    """Check that changing layout results in calling zoomToFit and adjusting scene rect."""
    
    mocker.spy(view, 'zoomToFit')
    mocker.spy(view.minimap, 'zoomToFit')
    mocker.spy(view.scene(), 'setSceneRect')
    
    view.scene().setLayout([])
    assert view.zoomToFit.call_count == 1
    assert view.minimap.zoomToFit.call_count == 1
    assert view.scene().setSceneRect.call_count == 1
        
        
@pytest.mark.parametrize("contains_scene", [True, False], ids=["contains", "notcontains"])
def test_view_minimap_adjust_rubber_band(view, mocker, qtbot, contains_scene):
    """Check that adjustRubberband hides band if entire scene is visible in main view."""
    
    with qtbot.waitExposed(view):
        view.show()
    
    mocker.patch("PyQt5.QtCore.QRectF.contains", return_value=contains_scene)
    view.minimap.adjustRubberband()
    
    assert not view.minimap.band.isVisible() == contains_scene
    
    
def test_view_minimap_left_mouse_press(view, qtbot, mocker):
    """Check that centerOn is called on left click only if band is visible and click is not inside band geometry."""

    mocker.spy(view.minimap, 'centerOn')
    mocker.patch("PyQt5.QtWidgets.QRubberBand.isVisible", return_value=False)

    qtbot.mousePress(view.minimap.viewport(), Qt.LeftButton)
    assert view.minimap.centerOn.call_count == 0
    qtbot.mouseRelease(view.minimap.viewport(), Qt.LeftButton)
    assert view.minimap.centerOn.call_count == 0
    
    mocker.patch("PyQt5.QtWidgets.QRubberBand.isVisible", return_value=True)
    
    qtbot.mousePress(view.minimap.viewport(), Qt.LeftButton)
    assert view.minimap.centerOn.call_count == 1
    qtbot.mouseRelease(view.minimap.viewport(), Qt.LeftButton)
    assert view.minimap.centerOn.call_count == 1
    
    mocker.patch("PyQt5.QtWidgets.QRubberBand.geometry", return_value=view.minimap.rect())
    qtbot.mousePress(view.minimap.viewport(), Qt.LeftButton)
    assert view.minimap.centerOn.call_count == 1
    qtbot.mouseRelease(view.minimap.viewport(), Qt.LeftButton)
    assert view.minimap.centerOn.call_count == 1

    
    
def test_view_minimap_right_mouse_press(view, qtbot, mocker):
    """Check that right mouse clik on minimap does nothing."""

    mocker.spy(view.minimap, 'centerOn')
    mocker.patch("PyQt5.QtWidgets.QRubberBand.isVisible", return_value=False)

    qtbot.mousePress(view.minimap.viewport(), Qt.RightButton)
    assert view.minimap.centerOn.call_count == 0
    qtbot.mouseRelease(view.minimap.viewport(), Qt.RightButton)
    assert view.minimap.centerOn.call_count == 0
    
    mocker.patch("PyQt5.QtWidgets.QRubberBand.isVisible", return_value=True)
    
    qtbot.mousePress(view.minimap.viewport(), Qt.RightButton)
    assert view.minimap.centerOn.call_count == 0
    qtbot.mouseRelease(view.minimap.viewport(), Qt.RightButton)
    assert view.minimap.centerOn.call_count == 0
    
    view.minimap.band.geometry = lambda: view.minimap.rect()
    qtbot.mousePress(view.minimap.viewport(), Qt.RightButton)
    assert view.minimap.centerOn.call_count == 0
    qtbot.mouseRelease(view.minimap.viewport(), Qt.RightButton)
    assert view.minimap.centerOn.call_count == 0
    
    
def test_view_minimap_mouse_move(view, qtbot, mocker):
    """Check that centerOn is called when band is dragged."""
    
    mocker.spy(view.minimap, 'centerOn')
    mocker.patch("PyQt5.QtWidgets.QRubberBand.isVisible", return_value=True)
    mocker.patch("PyQt5.QtWidgets.QRubberBand.geometry", return_value=view.minimap.rect())
    qtbot.mousePress(view.minimap.viewport(), Qt.LeftButton, pos=view.minimap.rect().center())
    assert view.minimap.centerOn.call_count == 0
    assert view.minimap._drag_start_pos is not None
    qtbot.mouseMove(view.minimap.viewport())
    assert view.minimap.centerOn.call_count == 1
    
    
def test_view_update_visible_items(view, mod, mocker):
    """Check that update method is called for every visible items."""
       
    node1 = mod.Node(85)
    view.scene().addNode(node1)
    node1.setVisible(False)
    
    node2 = mod.Node(85)
    view.scene().addNode(node2)
    
    for item in view.scene().nodes():
        mocker.spy(item, 'update')
    
    view.updateVisibleItems()
    
    for item in view.scene().nodes():
        if item.isVisible():
            assert item.update.call_count == 1
        else:
            assert item.update.call_count == 0
            
            
@pytest.mark.parametrize("scale", [0, 0.5, 20, 50, 100])
def test_view_scale_view(view, mocker, scale):
    """Check that scaleView call scale with appropriate scale factor."""
    
    mocker.spy(view, 'scale')
    mocker.spy(view.minimap, 'adjustRubberband')
    view.scaleView(scale)
    view.scale.assert_called_once_with(scale, scale)
    assert view.minimap.adjustRubberband.call_count == 1
    
    
def test_view_zoom_to_fit(view, mocker):
    """Check that zoomToFit does nothing if there is node scene set."""
    
    mocker.patch("PyQt5.QtWidgets.QGraphicsView.scene", return_value=None)
    mocker.spy(view, "fitInView")
    mocker.spy(view.minimap, "adjustRubberband")
    
    view.zoomToFit()
    assert view.fitInView.call_count == 0
    assert view.minimap.adjustRubberband.call_count == 0
    

def test_remote_session():
    """Check that `isRemoteSession` returns False when not in remote session."""
    assert PyQtNetworkView.view.isRemoteSession() == False
    
    
def test_disable_opengl(monkeypatch):
    """Check that `disable_opengl` set the `USE_OPENGL` flag to False."""
    
    monkeypatch.setattr(PyQtNetworkView.view, 'USE_OPENGL', True)
    assert PyQtNetworkView.view.USE_OPENGL == True
    PyQtNetworkView.view.disable_opengl()
    assert PyQtNetworkView.view.USE_OPENGL == False
    
    
@pytest.mark.parametrize('use_opengl', [True, False])
def test_opengl_disabled(mod, monkeypatch, use_opengl):
    """Check that if `USE_OPENGL` flag is False, usage of OpenGL is effectively disabled."""
    
    monkeypatch.setattr(PyQtNetworkView.view, 'USE_OPENGL', use_opengl)
    view = mod.NetworkView()
    if use_opengl:
        assert isinstance(view.viewport(), QOpenGLWidget)
    else:
        assert isinstance(view.viewport(), QWidget)
