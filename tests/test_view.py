import pytest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView

@pytest.fixture
def view(qtbot, mod):
    v = mod.NetworkView()
    v.isVisible = lambda: True
    v.setScene(mod.NetworkScene())
    qtbot.addWidget(v)
    
    return v

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
    
    
def test_view_mouse_move(view, qtbot, mocker):
    """Check that rubber band is adjusted when mouse move"""
    
    mocker.spy(view.minimap, 'adjustRubberband')
    qtbot.mousePress(view.viewport(), Qt.LeftButton, pos=view.rect().center())
    assert view.dragMode() == QGraphicsView.ScrollHandDrag
    qtbot.mouseMove(view.viewport(), pos=view.rect().center())
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