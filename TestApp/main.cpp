#include "../src/node.h"
#include "../src/edge.h"
#include "../src/networkscene.h"

#include <QApplication>
#include <QMainWindow>
#include <QGraphicsView>
#include <QGraphicsItem>

#include <ctime>
#include <iostream>
using namespace std;

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
    cout << "Populate Scene" << endl;
    clock_t begin = clock();
    int nitems = 0;
    QList<int> indexes;
    QList<QString> labels;
    QList<qreal> positions;
    for (int i = -11000; i < 11000; i += 110) {
        for (int j = -7000; j < 7000; j += 70) {
            indexes.append(nitems);
            labels.append(QString::number(nitems));
            positions.append(i);
            positions.append(j);

            ++nitems;
        }
    }
    scene->addNodes(indexes, labels);
    clock_t end = clock();
    double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    cout << elapsed_secs << "s" << endl;
    cout << nitems << "items" << endl;

    cout << "Set Layout" << endl;
    begin = clock();
    scene->setLayout(positions);
    end = clock();
    elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    cout << elapsed_secs << "s" << endl;

    cout << "Get all nodes" << endl;
    begin = clock();
    cout << scene->nodes().size() << endl;
    end = clock();
    elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    cout << elapsed_secs << "s" << endl;

    Node *node = scene->nodes()[0];
    QList<QColor> colors;
    colors << QColor(Qt::red) << QColor(Qt::green) << QColor(Qt::blue);
    scene->setPieColors(colors);
    QList<qreal> pies;
    pies << 5. << 10.;
    node->setPie(pies);

    QMainWindow mainWindow;
    mainWindow.setCentralWidget(view);

    mainWindow.show();
    return app.exec();
}
