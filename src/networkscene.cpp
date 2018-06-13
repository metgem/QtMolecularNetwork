#include <algorithm>

#include "networkscene.h"
#include "node.h"
#include "edge.h"
#include "style.h"

bool NodeLessThan(Node *n1, Node *n2)
{
    return n1->index() < n2->index();
}

NetworkScene::NetworkScene(QWidget *)
{
    clear();

    this->style_ = new DefaultStyle();
    this->scale_ = 1;
}

NetworkStyle *NetworkScene::networkStyle()
{
    return this->style_;
}

void NetworkScene::setNetworkStyle(NetworkStyle *style)
{
    NetworkStyle *new_style;
    if (style != 0)
        new_style = style;
    else
        new_style = new DefaultStyle();

    foreach(Node* node, nodes())
        node->updateStyle(this->style_, new_style);

    foreach(Edge* edge, edges())
        edge->updateStyle(this->style_, new_style);

    setBackgroundBrush(new_style->backgroundBrush());

    this->style_ = new_style;
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

QList<Node *> NetworkScene::addNodes(QList<int> indexes, QList<QString> labels, QList<QPointF> positions, QList<QVariant> colors)
{
    QList<Node *> nodes;
    QColor color;

    for (int i=0; i<indexes.size(); i++) {
        Node *node;
        if (labels.size() == indexes.size())
            node = new Node(indexes[i], this->style_->nodeRadius(), labels[i]);
        else
            node = new Node(indexes[i], this->style_->nodeRadius());

        if (positions.size() == indexes.size())
            node->setPos(positions[i]);

        if (colors.size() == indexes.size())
        {
            color = colors[i].value<QColor>();
            if (color.isValid())
                node->setBrush(color);
        }
        else if (style_ != 0)
            node->setBrush(style_->nodeBrush());

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
        edge->adjust();
        edges.append(edge);
    }

    return edges;
}

void NetworkScene::removeAllNodes()
{
    foreach(Node* node, nodes())
    {
        removeItem(qgraphicsitem_cast<QGraphicsItem *>(node));
    }
}

void NetworkScene::removeNodes(QList<Node *> nodes)
{
    foreach(Node* node, nodes)
    {
        removeItem(qgraphicsitem_cast<QGraphicsItem *>(node));
    }
}

void NetworkScene::removeAllEdges()
{
    foreach(Edge* edge, edges())
    {
        removeItem(qgraphicsitem_cast<QGraphicsItem *>(edge));
    }
}

void NetworkScene::removeEdges(QList<Edge *> edges)
{
    foreach(Edge* edge, edges)
    {
        removeItem(qgraphicsitem_cast<QGraphicsItem *>(edge));
    }
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

QRectF NetworkScene::selectedNodesBoundingRect()
{
    QRectF boundingRect;
    foreach (Node* node, selectedNodes())
        boundingRect |= node->sceneBoundingRect();
    return boundingRect;
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
    int j;

    for (int i=0; i<nodes.size(); i++) {
        Node *node = nodes[i];
        j = node->index();
        node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges, false);
        node->setPos(layout[j] * scale);
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
    int j;

    for (int i=0; i<nodes.size(); i++) {
        Node *node = nodes[i];
        j = node->index();
        node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges, false);
        node->setPos(layout[j*2] * scale, layout[j*2+1] * scale);
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
}

void NetworkScene::resetLabels()
{
    foreach (Node* node, this->nodes()) {
        QString label = QString::number(node->index() + 1);
        node->setLabel(label);
    }
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
    if (column_ids.size() != this->colors_.size())
        return;

    foreach (Node* node, this->nodes()) {
        QList<qreal> values;
        for (int i=0; i<column_ids.size(); i++) {
            values.append(model->index(node->index(), column_ids[i]).data(role).toReal());
        }
        node->setPie(values);
    }
}

void NetworkScene::resetPieCharts()
{
    foreach (Node* node, this->nodes()) {
        node->setPie(QList<qreal>());
    }
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

QList<QColor> NetworkScene::nodesColors()
{
    QList<QColor> colors;
    QColor color;
    QList<Node *> nodes = this->nodes();

    std::sort(nodes.begin(), nodes.end(), NodeLessThan);

    foreach(Node *node, nodes)
    {
        color = node->brush().color();
        if (color != style_->nodeBrush().color())
            colors.append(color);
        else
            colors.append(QColor());
    }

    return colors;
}

void NetworkScene::setNodesColors(QList<QVariant> colors)
{
    QColor color;
    QList<Node *> nodes = this->nodes();

    for (int i=0; i<nodes.size(); i++) {
        color = colors[nodes[i]->index()].value<QColor>();
        if (color.isValid())
            nodes[i]->setBrush(color);
    }
}

void NetworkScene::setSelectedNodesColor(QColor color)
{
    foreach(Node *node, selectedNodes())
    {
        if (color.isValid())
            node->setBrush(color);
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
