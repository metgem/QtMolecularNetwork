#include <algorithm>

#include "networkscene.h"
#include "node.h"
#include "edge.h"
#include "style.h"
#include "config.h"

bool NodeLessThan(Node *n1, Node *n2)
{
    return n1->index() < n2->index();
}

bool EdgeLessThan(Edge *e1, Edge *e2)
{
    return e1->index() < e2->index();
}

NetworkScene::NetworkScene(QWidget *)
{
    clear();

    this->style_ = new DefaultStyle();
    this->scale_ = 1;
    this->pie_charts_visibility = true;
}

NetworkStyle *NetworkScene::networkStyle()
{
    return this->style_;
}

void NetworkScene::setNetworkStyle(NetworkStyle *style)
{
    NetworkStyle *new_style;
    if (style != nullptr)
        new_style = style;
    else
        new_style = new DefaultStyle();

    foreach(Node* node, nodes())
        node->updateStyle(new_style, this->style_);

    foreach(Edge* edge, edges())
        edge->updateStyle(new_style, this->style_);

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

void NetworkScene::addNode(Node *node)
{
    node->setParentItem(nodesLayer);
}

void NetworkScene::addEdge(Edge *edge)
{
    edge->setParentItem(edgesLayer);
}

QList<Node *> NetworkScene::addNodes(QList<int> indexes, QList<QString> labels,
                                     QList<QPointF> positions, QList<QVariant> colors, QList<QVariant> radii)
{
    QList<Node *> nodes;
    QColor color;
    int radius;

    for (int i=0; i<indexes.size(); i++) {
        Node *node;
        if (labels.size() == indexes.size())
            node = new Node(indexes[i], labels[i]);
        else
            node = new Node(indexes[i]);

        if (positions.size() == indexes.size())
            node->setPos(positions[i]);

        if (this->style_ != nullptr)
            node->updateStyle(this->style_);

        if (colors.size() == indexes.size())
        {
            color = colors[i].value<QColor>();
            if (color.isValid())
                node->setBrush(color);
        }

        if (radii.size() == indexes.size())
        {
            radius = radii[i].value<int>();
            if (radius > 0)
                node->setRadius(radius);
        }

        node->setParentItem(nodesLayer);
        nodes.append(node);
    }

    return nodes;
}

QList<Edge *> NetworkScene::addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> widths)
{
    QList<Edge *> edges;

    for (int i=0; i<indexes.size(); i++) {
        Edge *edge = new Edge(indexes[i], sourceNodes[i], destNodes[i], widths[i]);
        if (this->style_ != nullptr)
            edge->updateStyle(this->style_);
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

    std::sort(nodes.begin(), nodes.end(), NodeLessThan);

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
        if (0 <= index && index < nodes.size())
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

    std::sort(edges.begin(), edges.end(), EdgeLessThan);

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
        if (0 <= index && index < edges.size())
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

void NetworkScene::setLayout(QList<QPointF> layout, qreal scale, QList<int> isolated_nodes)
{
    if (scale <= 0)
        scale = this->scale_;

    QList<Node *> nodes = this->nodes();
    int j;

    for (int i=0; i<nodes.size(); i++) {
        Node *node = nodes[i];
        j = node->index();
        if (isolated_nodes.contains(j))
        {
            node->setFlag(QGraphicsItem::ItemHasNoContents, true);
            node->setFlag(QGraphicsItem::ItemIsSelectable, false);
            node->setFlag(QGraphicsItem::ItemIsMovable, false);
            node->setFlag(QGraphicsItem::ItemIgnoresTransformations, true);
        }
        else
        {
            node->setFlag(QGraphicsItem::ItemHasNoContents, false);
            node->setFlag(QGraphicsItem::ItemIsSelectable, true);
            node->setFlag(QGraphicsItem::ItemIsMovable, true);
            node->setFlag(QGraphicsItem::ItemIgnoresTransformations, false);
            node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges, false);
            node->setPos(layout[j] * scale);
            node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges, true);
        }
    }

    foreach(Edge* edge, edges())
    {
        edge->adjust();
    }

    emit this->layoutChanged();
}

void NetworkScene::setLayout(QList<qreal> layout, qreal scale, QList<int> isolated_nodes)
{
    if (scale <= 0)
        scale = this->scale_;

    QList<Node *> nodes(this->nodes());
    int j;

    for (int i=0; i<nodes.size(); i++) {
        Node *node = nodes[i];
        j = node->index();
        if (isolated_nodes.contains(j))
        {
            node->setFlag(QGraphicsItem::ItemHasNoContents, true);
            node->setFlag(QGraphicsItem::ItemIgnoresTransformations, true);
            node->setFlag(QGraphicsItem::ItemIsSelectable, false);
            node->setFlag(QGraphicsItem::ItemIsMovable, false);
        }
        else
        {
            node->setFlag(QGraphicsItem::ItemHasNoContents, false);
            node->setFlag(QGraphicsItem::ItemIgnoresTransformations, false);
            node->setFlag(QGraphicsItem::ItemIsSelectable, true);
            node->setFlag(QGraphicsItem::ItemIsMovable, true);
            node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges, false);
            node->setPos(layout[j*2] * scale, layout[j*2+1] * scale);
            node->setFlag(QGraphicsItem::ItemSendsScenePositionChanges);
        }
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
    if (scale <= 0)
        scale = 1;

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

void NetworkScene::setLabelsFromModel(QAbstractItemModel *model, int column_id, int role)
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

void NetworkScene::setNodesRadiiFromModel(QAbstractItemModel *model, int column_id, int role, const std::function<int (qreal)> &func)
{
    if (func)
    {
        foreach (Node* node, this->nodes()) {
            node->setRadius(func(model->index(node->index(), column_id).data(role).toReal()));
        }
    }
    else
    {
        foreach (Node* node, this->nodes()) {
            node->setRadius(model->index(node->index(), column_id).data(role).toInt());
        }
    }

    foreach (Edge* edge, this->edges()) {
        edge->adjust();
    }
}

void NetworkScene::resetNodesRadii()
{
    foreach (Node* node, this->nodes()) {
        node->setRadius(RADIUS);
    }

    foreach (Edge* edge, this->edges()) {
        edge->adjust();
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

void NetworkScene::setPieChartsFromModel(QAbstractItemModel *model, QList<int> column_ids, int role)
{
    if (column_ids.size() > this->colors_.size())
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

bool NetworkScene::pieChartsVisibility()
{
    return this->pie_charts_visibility;
}

void NetworkScene::setPieChartsVisibility(bool visibility)
{
    if (visibility != this->pie_charts_visibility)
    {
        this->pie_charts_visibility = visibility;
        emit this->pieChartsVisibilityChanged(visibility);
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

void NetworkScene::hideAllItems()
{
    foreach(QGraphicsItem *item, items())
    {
        item->hide();
    }
}

QList<QColor> NetworkScene::nodesColors()
{
    QList<QColor> colors;
    QColor color;

    foreach(Node *node, this->nodes())
    {
        color = node->brush().color();
        if (color != this->style_->nodeBrush().color())
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

    if (colors.size() < nodes.size())
        return;

    for (int i=0; i<nodes.size(); i++) {
        color = colors[nodes[i]->index()].value<QColor>();
        if (color.isValid())
            nodes[i]->setBrush(color);
    }
}

void NetworkScene::setSelectedNodesColor(QColor color)
{
    if (color.isValid())
    {
        foreach(Node *node, selectedNodes())
        {
            node->setBrush(color);
        }
    }
}

QList<int> NetworkScene::nodesRadii()
{
    QList<int> radii;
    int radius;

    foreach(Node *node, this->nodes())
    {
        radius = node->radius();
        if (radius != RADIUS)
            radii.append(radius);
        else
            radii.append(0);
    }

    return radii;
}

void NetworkScene::setNodesRadii(QList<int> radii)
{
    int radius;
    QList<Node *> nodes = this->nodes();

    for (int i=0; i<nodes.size(); i++) {
        radius = radii[nodes[i]->index()];
        nodes[i]->setRadius(radius);
        foreach(Edge* edge, nodes[i]->edges())
            edge->adjust();
    }
}

void NetworkScene::setSelectedNodesRadius(int radius)
{
    foreach(Node *node, selectedNodes())
    {
        node->setRadius(radius);
        foreach(Edge* edge, node->edges())
            edge->adjust();
    }
}


Node *NetworkScene::nodeAt(const QPointF &position, const QTransform &deviceTransform) const
{
    QGraphicsItem *item = itemAt(position, deviceTransform);
    if (nodesLayer->isAncestorOf(item))
        return qgraphicsitem_cast<Node *>(item);
    return nullptr;

}

Node *NetworkScene::nodeAt(qreal x, qreal y, const QTransform &deviceTransform) const
{
    QGraphicsItem *item = itemAt(x, y, deviceTransform);
    if (nodesLayer->isAncestorOf(item))
        return qgraphicsitem_cast<Node *>(item);
    return nullptr;
}

Edge *NetworkScene::edgeAt(const QPointF &position, const QTransform &deviceTransform) const
{
    QGraphicsItem *item = itemAt(position, deviceTransform);
    if (edgesLayer->isAncestorOf(item))
        return qgraphicsitem_cast<Edge *>(item);
    return nullptr;
}

Edge *NetworkScene::edgeAt(qreal x, qreal y, const QTransform &deviceTransform) const
{
    QGraphicsItem *item = itemAt(x, y, deviceTransform);
    if (edgesLayer->isAncestorOf(item))
        return qgraphicsitem_cast<Edge *>(item);
    return nullptr;
}

QRectF NetworkScene::itemsBoundingRect() const
{
    QRectF boundingRect;
    foreach (QGraphicsItem *item, items())
    {
        if (!(item->flags() & QGraphicsItem::ItemHasNoContents))
            boundingRect |= item->sceneBoundingRect();
    }
    return boundingRect;
}
