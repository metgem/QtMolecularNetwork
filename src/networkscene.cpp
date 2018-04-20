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

    this->scale_ = 1;

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
        Node *node;
        if (labels.size() == indexes.size())
            node = new Node(indexes[i], labels[i]);
        else
            node = new Node(indexes[i]);

        if (positions.size() == indexes.size())
            node->setPos(positions[i]);

        node->setParentItem(nodesLayer);
        nodes.append(node);
    }

    return nodes;
}

QList<Edge *> NetworkScene::addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> weights, QList<qreal> widths)
{
    QList<Edge *> edges;

    for (int i=0; i<indexes.size(); i++) {
        Edge *edge = new Edge(indexes[i], sourceNodes[i], destNodes[i], weights[i], widths[i]);

        edge->setParentItem(edgesLayer);
        edges.append(edge);
    }

    return edges;
}

QList<Node *> NetworkScene::nodes() const
{
    QList<Node *> nodes;
    foreach(QGraphicsItem *item, nodesLayer->childItems())
    {
        nodes.append(qgraphicsitem_cast<Node *>(item));
    }
    return nodes;
}

QList<Node *> NetworkScene::selectedNodes() const
{
    QList<Node *> nodes;
    foreach(QGraphicsItem *item, selectedItems())
    {
        if (nodesLayer->isAncestorOf(item))
            nodes.append(qgraphicsitem_cast<Node *>(item));
    }
    return nodes;
}

void NetworkScene::setNodesSelection(QList<int> indexes)
{
    clearSelection();
    QList<Node *> nodes = this->nodes();
    foreach (int index, indexes)
    {
        nodes[index]->setSelected(true);
    }
}

void NetworkScene::setNodesSelection(QList<Node *> nodes)
{
    clearSelection();
    foreach (Node *node, nodes)
    {
        node->setSelected(true);
    }
}

QList<Edge *> NetworkScene::edges() const
{
    QList<Edge *> edges;
    foreach(QGraphicsItem *item, edgesLayer->childItems())
    {
        edges.append(qgraphicsitem_cast<Edge *>(item));
    }
    return edges;
}

QList<Edge *> NetworkScene::selectedEdges() const
{
    QList<Edge *> edges;
    foreach(QGraphicsItem *item, selectedItems())
    {
        if (edgesLayer->isAncestorOf(item))
            edges.append(qgraphicsitem_cast<Edge *>(item));
    }
    return edges;
}

void NetworkScene::setEdgesSelection(QList<int> indexes)
{
    clearSelection();
    QList<Edge *> edges = this->edges();
    foreach (int index, indexes)
    {
        edges[index]->setSelected(true);
    }
}

void NetworkScene::setEdgesSelection(QList<Edge *> edges)
{
    clearSelection();
    foreach (Edge *edge, edges)
    {
        edge->setSelected(true);
    }
}

void NetworkScene::setLayout(QList<QPointF> layout, qreal scale)
{
    if (!scale)
        scale = this->scale_;

    QList<Node *> nodes = this->nodes();

    for (int i=0; i<nodes.size(); i++) {
        Node *node = nodes[i];
        node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges, false);
        nodes[i]->setPos(layout[i] * scale);
        node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges);
    }

    foreach(Edge* edge, edges())
    {
        edge->adjust();
    }

    emit this->layoutChanged();
}

void NetworkScene::setLayout(QList<qreal> layout, qreal scale)
{
    if (!scale)
        scale = this->scale_;

    QList<Node *> nodes(this->nodes());
    for (int i=0; i<nodes.size(); i++) {
        Node *node = nodes[i];
        node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges, false);
        node->setPos(layout[i*2] * scale, layout[i*2+1] * scale);
        node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges);
    }

    foreach(Edge* edge, edges())
    {
        edge->adjust();
    }

    emit this->layoutChanged();
}

qreal NetworkScene::scale()
{
    return this->scale_;
}

void NetworkScene::setScale(qreal scale)
{
    foreach (Node* node, this->nodes()) {
        node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges, false);
        node->setPos(node->pos() * scale / this->scale_);
        node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges);
    }

    foreach(Edge* edge, edges())
    {
        edge->adjust();
    }

    this->scale_ = scale;
    emit this->scaleChanged(scale);
}

void NetworkScene::setLabelsFromModel(QAbstractTableModel* model, int column_id, int role)
{
    foreach (Node* node, this->nodes()) {
        QVariant label = model->index(node->index(), column_id).data(role);
        node->setLabel(label.toString());
    }
    this->invalidate();
}

QList<QColor> NetworkScene::pieColors()
{
    return this->colors_;
}

void NetworkScene::setPieColors(QList<QColor> colors)
{
    this->colors_ = colors;
}

void NetworkScene::setPieChartsFromModel(QAbstractTableModel *model, QList<int> column_ids, int role)
{
    foreach (Node* node, this->nodes()) {
        QList<qreal> values;
        for (int i=0; i<column_ids.size(); i++) {
            values.append(model->index(node->index(), column_ids[i]).data(role).toReal());
        }
        node->setPie(values);
    }
    this->invalidate();
}

void NetworkScene::resetPieCharts()
{
    foreach (Node* node, this->nodes()) {
        node->setPie(QList<qreal>());
    }
    this->invalidate();
}

void NetworkScene::hideItems(QList<QGraphicsItem *> items)
{
    foreach(QGraphicsItem *item, items)
    {
        item->hide();
    }
}

void NetworkScene::showItems(QList<QGraphicsItem *> items)
{
    foreach(QGraphicsItem *item, items)
    {
        item->show();
    }
}

void NetworkScene::hideSelectedItems()
{
    QList<QGraphicsItem *> items = selectedItems();
    clearSelection();
    foreach(QGraphicsItem *item, items)
    {
        item->hide();
    }
}

void NetworkScene::showAllItems()
{
    foreach(QGraphicsItem *item, items())
    {
        item->show();
    }
}

Node *NetworkScene::nodeAt(const QPointF &position, const QTransform &deviceTransform) const
{
    QGraphicsItem *item = itemAt(position, deviceTransform);
    if (nodesLayer->isAncestorOf(item))
        return qgraphicsitem_cast<Node *>(item);
    return 0;

}

Node *NetworkScene::nodeAt(qreal x, qreal y, const QTransform &deviceTransform) const
{
    QGraphicsItem *item = itemAt(x, y, deviceTransform);
    if (nodesLayer->isAncestorOf(item))
        return qgraphicsitem_cast<Node *>(item);
    return 0;
}

Edge *NetworkScene::edgeAt(const QPointF &position, const QTransform &deviceTransform) const
{
    QGraphicsItem *item = itemAt(position, deviceTransform);
    if (edgesLayer->isAncestorOf(item))
        return qgraphicsitem_cast<Edge *>(item);
    return 0;
}

Edge *NetworkScene::edgeAt(qreal x, qreal y, const QTransform &deviceTransform) const
{
    QGraphicsItem *item = itemAt(x, y, deviceTransform);
    if (edgesLayer->isAncestorOf(item))
        return qgraphicsitem_cast<Edge *>(item);
    return 0;
}
