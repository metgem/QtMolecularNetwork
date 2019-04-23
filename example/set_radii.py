import sys
import time

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QPointF, Qt
from PyQtNetworkView import NetworkScene

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
for i in range(-110, 110, 110):
    for j in range(-70, 70, 70):
        indexes.append(nitems)
        labels.append(str(nitems))
        positions.append(QPointF(i, j))

        nitems += 1
        
scene.addNodes(indexes, labels, positions)

model = QStandardItemModel(4, 1)
for row in range(4):
    item = QStandardItem("")
    item.setData(float(row), Qt.UserRole+1)
    model.setItem(row, 0, item)

def easing_function(value: float) -> int:
    return int(value*10)
scene.setNodesRadiiFromModel(model, 0, Qt.UserRole+1)
    
print(f"{time.time()-t0}s")
print(f"{nitems} items")

view.show()

sys.exit(app.exec_())