#ifndef NETWORKSCENE_H
#define NETWORKSCENE_H

#include "graphicsitem.h"

#include <QGraphicsScene>
#include <QWidget>

class Node;
class Edge;

class Q_DECL_EXPORT NetworkScene : public QGraphicsScene
{
    Q_OBJECT

public:
    NetworkScene(QWidget *parent = 0);

    void clear();

    QList<Node *> addNodes(QList<int> indexes, QList<QString> labels, QList<QPointF> positions);
    QList<Edge *> addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> weights, QList<qreal> widths);

    QList<QGraphicsItem *> nodes() const;
    QList<QGraphicsItem *> edges() const;

private:
    GraphicsItemLayer *nodesLayer;
    GraphicsItemLayer *edgesLayer;
};

#endif // NETWORKSCENE_H
