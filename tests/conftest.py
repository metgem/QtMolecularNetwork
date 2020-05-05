import PyQtNetworkView
import PyQtNetworkView._pure

from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtGui import QMouseEvent, QResizeEvent, QFocusEvent

from contextlib import contextmanager
import pytest

@contextmanager
def not_raises(ExpectedException):
    """Raise AssertionError if ExpectedException occurs"""
    
    try:
        yield

    except ExpectedException as error:
        raise AssertionError(f"Raised exception {error} when it should not!")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")
    
pytest.not_raises = not_raises
    

def pytest_generate_tests(metafunc):        
    if 'mod' in metafunc.fixturenames:
        metafunc.parametrize("mod",
                             [PyQtNetworkView, PyQtNetworkView._pure])       
         
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items):
    for item in items:
        # All tests need this thing, this hook allows you not to declare it if 
        # it is not used explicitly
        if 'qapp' not in item.fixturenames:
            item.fixturenames.append('qapp')
                             
    
@pytest.fixture
def qtbot(qapp, qtbot):
    # Monkey patch qtbot.mouseMove to allow sending mouseMove events without
    # window manager
    def mouseMove(widget, pos=QPoint(), delay=-1):
        event = QMouseEvent(QEvent.MouseMove, pos, Qt.NoButton, Qt.NoButton, Qt.NoModifier)
        qapp.sendEvent(widget, event)
        
    def resizeWidget(widget, size):
        event = QResizeEvent(size, widget.size())
        qapp.sendEvent(widget, event)
        
    def setFocus(widget):
        event = QFocusEvent(QEvent.FocusIn)
        qapp.sendEvent(widget, event)
        
    qtbot.mouseMove = mouseMove
    qtbot.resizeWidget = resizeWidget
    qtbot.setFocus = setFocus
    
    return qtbot
