from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap

import pytest
import hashlib

from resources import MOLECULES

SIZES = [QSize(1, 1), QSize(20, 50), QSize(100, 100), QSize(300, 300)]

@pytest.mark.parametrize("molecule", MOLECULES)
@pytest.mark.parametrize("size", SIZES)
def test_svg_to_pixmap(mod, molecule, size):
    """Check SvgToPixmap."""

    pixmap = mod.SvgToPixmap(molecule['svg'], size)
    assert not pixmap.isNull()
    assert pixmap.size() == size

@pytest.mark.parametrize("molecule", MOLECULES)
@pytest.mark.parametrize("size", SIZES)
def test_smiles_to_pixmap(mod, molecule, size):
    """Check SmilesToPixmap."""

    pixmap = mod.SmilesToPixmap(molecule['smiles'], size)
    assert not pixmap.isNull()
    assert pixmap.size() == size
    
@pytest.mark.parametrize("molecule", MOLECULES)
@pytest.mark.parametrize("size", SIZES)
def test_inchi_to_pixmap(mod, molecule, size):
    """Check InchiToPixmap."""

    pixmap = mod.InchiToPixmap(molecule['inchi'], size)
    assert not pixmap.isNull()
    assert pixmap.size() == size
