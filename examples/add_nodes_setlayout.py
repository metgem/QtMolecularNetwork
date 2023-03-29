import sys
import time
import numpy as np

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
positions = np.empty((40000, 2))
t0 = time.time()
for i in range(-11000, 11000, 110):
    for j in range(-7000, 7000, 70):
        indexes.append(nitems)
        labels.append(str(nitems))
        positions[(i+11000)//110*200 + (j+7000)//70] = (i, j)

        nitems += 1

scene.createNodes(indexes, labels)
scene.setLayout(positions)
    
print(f"{time.time()-t0}s")
print(f"{nitems} items")

view.show()

sys.exit(app.exec())