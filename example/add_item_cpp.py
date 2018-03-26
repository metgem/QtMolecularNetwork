import sys
import time

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPointF
from PyNetworkView import NetworkScene, Node

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
t0 = time.time()
for i in range(-11000, 11000, 110):
    for j in range(-7000, 7000, 70):
        node = Node(nitems, str(nitems))
        node.setPos(QPointF(i,j))

        scene.addItem(node)
        
        nitems += 1
    
print(f"{time.time()-t0}s")
print(f"{nitems} items")

view.show()

sys.exit(app.exec_())