from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap

import pytest
import hashlib

from resources import MOLECULES

SIZES = [QSize(0, 0), QSize(1, 1), QSize(20, 50), QSize(100, 100), QSize(300, 300)]

@pytest.mark.parametrize("molecule", MOLECULES)
@pytest.mark.parametrize("size", SIZES)
def test_svg_to_pixmap(mod, molecule, size):
    """Check SvgToPixmap."""

    pixmap = mod.SvgToPixmap(molecule['svg'], size)
    assert pixmap.isNull() == size.isNull()
    assert pixmap.size() == size

@pytest.mark.parametrize("molecule", MOLECULES)
@pytest.mark.parametrize("size", SIZES)
def test_smiles_to_pixmap(mod, molecule, size):
    """Check SmilesToPixmap."""

    pixmap = mod.SmilesToPixmap(molecule['smiles'], size)
    assert pixmap.isNull() == size.isNull()
    assert pixmap.size() == size
    
@pytest.mark.parametrize("molecule", MOLECULES)
@pytest.mark.parametrize("size", SIZES)
def test_inchi_to_pixmap(mod, molecule, size):
    """Check InchiToPixmap."""

    pixmap = mod.InchiToPixmap(molecule['inchi'], size)
    assert pixmap.isNull() == size.isNull()
    assert pixmap.size() == size
