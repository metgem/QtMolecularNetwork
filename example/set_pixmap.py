import sys
import time

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QPointF, QSize
from PyQtNetworkView import NetworkScene, Node
from PyQtNetworkView.mol_depiction import SmilesToPixmap, InchiToPixmap

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

pixmap1 = SmilesToPixmap("c1nccc2n1ccc2", QSize(300, 300))
pixmap2 = InchiToPixmap("InChI=1S/C17H19NO3/c1-18-7-6-17-10-3-5-13(20)16(17)21-15-12(19)4-2-9(14(15)17)8-11(10)18/h2-5,10-11,13,16,19-20H,6-8H2,1H3/t10-,11+,13-,16-,17-/m0/s1",
                        QSize(300, 300))

nitems = 0
t0 = time.time()
for i in range(-1100, 1100, 110):
    for j in range(-700, 700, 70):
        node = Node(nitems, str(nitems))
        node.setPos(QPointF(i, j))
        mod = nitems%4
        if mod == 0:
            node.setPixmap(pixmap1)
        elif mod == 1:
            node.setPixmap(pixmap2)
        elif mod == 2:
            node.setPixmapFromSmiles("CN=C=O")
        else:
            node.setPixmapFromInchi("InChI=1S/C10H16O/c1-6(2)10-4-8(10)7(3)9(11)5-10/h6-8H,4-5H2,1-3H3/t7-,8-,10+/m1/s1")
        scene.addItem(node)

        nitems += 1
    
print(f"{time.time()-t0}s")
print(f"{nitems} items")

view.show()

sys.exit(app.exec_())
