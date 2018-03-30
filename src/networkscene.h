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

    QList<Node *> addNodes(QList<int> indexes, QList<QString> labels, QList<QPointF> positions = QList<QPointF>());
    QList<Edge *> addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> weights, QList<qreal> widths);

    QList<Node *> nodes() const;
    QList<Node *> selectedNodes() const;
    void setNodesSelection(QList<int> indexes);
    void setNodesSelection(QList<Node *> nodes);

    QList<Edge *> edges() const;
    QList<Edge *> selectedEdges() const;
    void setEdgesSelection(QList<int> indexes);
    void setEdgesSelection(QList<Edge *> edges);

    void setLayout(QList<qreal> layout);
    void setLayout(QList<QPointF> layout);

private:
    GraphicsItemLayer *nodesLayer;
    GraphicsItemLayer *edgesLayer;
};

#endif // NETWORKSCENE_H
