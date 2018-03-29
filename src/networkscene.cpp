#include "networkscene.h"
#include "node.h"
#include "edge.h"

NetworkScene::NetworkScene(QWidget *)
{
    clear();
}

void NetworkScene::clear()
{
    QGraphicsScene::clear();

    nodesLayer = new GraphicsItemLayer;
    edgesLayer = new GraphicsItemLayer;

    addItem(nodesLayer);
    nodesLayer->setZValue(1);
    addItem(edgesLayer);
    edgesLayer->setZValue(0);
}

QList<Node *> NetworkScene::addNodes(QList<int> indexes, QList<QString> labels, QList<QPointF> positions)
{
    QList<Node *> nodes;

    for (int i=0; i<indexes.size(); i++) {
        Node *node = new Node(indexes.at(i), labels.at(i));
        node->setPos(positions.at(i));

        node->setParentItem(nodesLayer);
        nodes.append(node);
    }

    return nodes;
}

QList<Edge *> NetworkScene::addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> weights, QList<qreal> widths)
{
    QList<Edge *> edges;

    for (int i=0; i<indexes.size(); i++) {
        Edge *edge = new Edge(indexes.at(i), sourceNodes.at(i), destNodes.at(i), weights.at(i), widths.at(i));

        edge->setParentItem(edgesLayer);
        edges.append(edge);
    }

    return edges;
}

QList<QGraphicsItem *> NetworkScene::nodes() const
{
    return nodesLayer->childItems();
}

QList<QGraphicsItem *> NetworkScene::edges() const
{
    return edgesLayer->childItems();
}
