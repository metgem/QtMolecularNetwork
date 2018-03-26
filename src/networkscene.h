#ifndef NETWORKVIEW_H
#define NETWORKVIEW_H

#include <QGraphicsScene>
#include <QWidget>

class Node;

class Q_DECL_EXPORT NetworkScene : public QGraphicsScene
{
    Q_OBJECT

public:
    NetworkScene(QWidget *parent = 0);
    void addNodes(QList<int> indexes, QList<QString> labels, QList<QPointF> positions);
    void addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> weights, QList<qreal> widths);

};

#endif // NETWORKVIEW_H
