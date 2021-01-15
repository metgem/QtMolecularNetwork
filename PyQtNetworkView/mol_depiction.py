from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtSvg import QSvgRenderer

from rdkit.Chem import Mol, MolFromSmiles, rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.inchi import INCHI_AVAILABLE
if INCHI_AVAILABLE:
    from rdkit.Chem.inchi import MolFromInchi


def SvgToPixmap(svg_data: str, size: QSize):
    if size.isNull():
        return QPixmap()
    
    svg_renderer = QSvgRenderer()
    svg_renderer.load(svg_data.encode('utf-8'))
    pixmap = QPixmap(size)
    painter = QPainter()

    pixmap.fill(Qt.transparent)
    painter.begin(pixmap)
    svg_renderer.render(painter)
    painter.end()

    return pixmap


def MolToPixmap(mol: Mol, size: QSize):
    if size.isNull() or mol is None:
        return QPixmap()
    
    if not mol.GetNumConformers():
        rdDepictor.Compute2DCoords(mol)

    svg_drawer = rdMolDraw2D.MolDraw2DSVG(size.width(), size.height())
    svg_drawer.drawOptions().clearBackground = False
    svg_drawer.DrawMolecule(mol)
    svg_drawer.FinishDrawing()
    drawing_text = svg_drawer.GetDrawingText()
    return SvgToPixmap(drawing_text, size)


def SmilesToPixmap(smiles: str, size: QSize):
    if size.isNull() or not smiles:
        return QPixmap()
    
    return MolToPixmap(MolFromSmiles(smiles), size)


def InchiToPixmap(inchi: str, size: QSize):
    if size.isNull() or not inchi:
        return QPixmap()
    
    return MolToPixmap(MolFromInchi(inchi), size)
