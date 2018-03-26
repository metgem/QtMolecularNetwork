#include "../src/node.h"
#include "../src/edge.h"
#include "../src/networkscene.h"

#include <QApplication>
#include <QMainWindow>
#include <QGraphicsView>
#include <QGraphicsItem>

#include <ctime>
#include <iostream>

int main(int argc, char **argv)
{
    QApplication app(argc, argv);

    QGraphicsView *view = new QGraphicsView;

    NetworkScene *scene = new NetworkScene(view);
    scene->setItemIndexMethod(QGraphicsScene::NoIndex);
    view->setScene(scene);
    view->setCacheMode(QGraphicsView::CacheBackground);
    view->setOptimizationFlags(QGraphicsView::DontSavePainterState);
    view->setViewportUpdateMode(QGraphicsView::SmartViewportUpdate);
    view->setRenderHint(QPainter::Antialiasing);

    /*Node *node1 = new Node(0, QString("Node1"));
    Node *node2 = new Node(1, QString("Node2"));
    Node *node3 = new Node(2, QString("Node3"));
    scene->addItem(node1);
    scene->addItem(node2);
    scene->addItem(new Edge(0, node1, node2));
    scene->addItem(node3);
    scene->addItem(new Edge(1, node3, node3));
    node1->setPos(-50, -50);
    node2->setPos(0, -50);*/

    // Populate scene
    std::clock_t begin = std::clock();
    int nitems = 0;
    QList<int> indexes;
    QList<QString> labels;
    QList<QPointF> positions;
    for (int i = -11000; i < 11000; i += 110) {
        for (int j = -7000; j < 7000; j += 70) {
            indexes.append(nitems);
            labels.append(QString::number(nitems));
            positions.append(QPointF(i, j));

            ++nitems;
        }
    }
    scene->addNodes(indexes, labels, positions);
    std::clock_t end = std::clock();
    double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    std::cout << elapsed_secs << "s" << std::endl;
    std::cout << nitems << "items" << std::endl;

    QMainWindow mainWindow;
    mainWindow.setCentralWidget(view);

    mainWindow.show();
    return app.exec();
}
