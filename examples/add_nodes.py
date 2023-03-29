import sys
import time

from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter
from PySide6.QtCore import QPointF
from PySide6MolecularNetwork import NetworkScene

app = QApplication(sys.argv)

view = QGraphicsView()
scene = NetworkScene()
view.setScene(scene)
scene.setItemIndexMethod(QGraphicsScene.NoIndex)
view.setScene(scene)
view.setCacheMode(QGraphicsView.CacheBackground)
view.setOptimizationFlags(QGraphicsView.DontSavePainterState)
view.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
view.setRenderHint(QPainter.Antialiasing)

nitems = 0
indexes = []
labels = []
positions = []
t0 = time.time()
for i in range(-11000, 11000, 110):
    for j in range(-7000, 7000, 70):
        indexes.append(nitems)
        labels.append(str(nitems))
        positions.append(QPointF(i, j))

        nitems += 1
        
scene.createNodes(indexes, labels, positions)
    
print(f"{time.time()-t0}s")
print(f"{nitems} items")

view.show()

sys.exit(app.exec())