#include "networkscene.h"
#include "node.h"
#include "edge.h"

NetworkScene::NetworkScene(QWidget *)
{

}

void NetworkScene::addNodes(QList<int> indexes, QList<QString> labels, QList<QPointF> positions)
{
    for (int i=0; i<indexes.size(); i++) {
        Node *node = new Node(indexes.at(i), labels.at(i));
        node->setPos(positions.at(i));

        addItem(node);
    }
}

void NetworkScene::addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> weights, QList<qreal> widths)
{
    for (int i=0; i<indexes.size(); i++) {
        Edge *edge = new Edge(indexes.at(i), sourceNodes.at(i), destNodes.at(i), weights.at(i), widths.at(i));

        addItem(edge);
    }
}
