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
    this->pixmap_visibility = true;
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

void NetworkScene::render(QPainter *painter, const QRectF &target, const QRectF &source, Qt::AspectRatioMode aspectRatioMode)
{
    foreach(Node* node, nodes())
    {
        node->setCacheMode(QGraphicsItem::NoCache);
    }
    QGraphicsScene::render(painter, target, source, aspectRatioMode);
    foreach(Node* node, nodes())
    {
        node->setCacheMode(QGraphicsItem::DeviceCoordinateCache);
    }
}

void NetworkScene::addNode(Node *node)
{
    node->setParentItem(nodesLayer);
}

void NetworkScene::addEdge(Edge *edge)
{
    edge->setParentItem(edgesLayer);
}

void NetworkScene::addNodes(QList<Node *> nodes)
{
    foreach(Node* node, nodes)
    {
        node->setParentItem(nodesLayer);
    }
}

void NetworkScene::addEdges(QList<Edge *> edges)
{
    foreach(Edge* edge, edges)
    {
        edge->setParentItem(edgesLayer);
    }
}

QList<Node *> NetworkScene::createNodes(QList<int> indexes, QList<QString> labels,
                                     QList<QPointF> positions, QList<QVariant> colors, QList<QVariant> radii)
{
    if (indexes.isEmpty())
        return QList<Node *>();

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

QList<Edge *> NetworkScene::createEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> widths)
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
    foreach(Edge * edge, edges())
    {
        if (indexes.contains(edge->index()))
            edge->setSelected(true);
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

    if (layout.size() < nodes.size())
        return;

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
            node->setFlag(QGraphicsItem::ItemIsMovable, is_locked);
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

    if (layout.size() < 2*nodes.size())
        return;

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
            node->setFlag(QGraphicsItem::ItemIsMovable, is_locked);
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

void NetworkScene::setPixmapsFromModel(QAbstractItemModel *model, int column_id, int role, int type)
{
    foreach (Node* node, this->nodes()) {
        QVariant data = model->index(node->index(), column_id).data(role);
        if (!data.isValid())
            continue;
        QString text = data.toString();

        if (type == NetworkScene::PixmapsBase64 || (type == NetworkScene::PixmapsAuto && text.startsWith(QString("b64="))))
        {
            if (text.startsWith(QString("b64=")))
                node->setPixmapFromBase64(text.mid(4).toUtf8());
            else
                node->setPixmapFromBase64(text.toUtf8());
        }
        else if (type == NetworkScene::PixmapsSvg || (type == NetworkScene::PixmapsAuto && (text.startsWith(QString("<?xml")) || text.startsWith("<svg"))))
            node->setPixmapFromSvg(text.toUtf8());
        else if (type == NetworkScene::PixmapsInchi || (type == NetworkScene::PixmapsAuto && text.startsWith(QString("InChI="))))
            node->setPixmapFromInchi(text);
        else if (type == NetworkScene::PixmapsSmiles || type == NetworkScene::PixmapsAuto)
            node->setPixmapFromSmiles(text);
    }
}

bool NetworkScene::pixmapVisibility()
{
    return this->pixmap_visibility;
}

void NetworkScene::setPixmapVisibility(bool visibility)
{
    if (visibility != this->pixmap_visibility)
    {
        this->pixmap_visibility = visibility;
        emit this->pixmapVisibilityChanged(visibility);
    }
}

void NetworkScene::resetPixmaps()
{
    foreach (Node* node, this->nodes()) {
        node->setPixmap(QPixmap());
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

    if (radii.size() < nodes.size())
        return;

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

void NetworkScene::lock(bool lock)
{
    foreach (Node *node, nodes())
    {
        node->setFlag(QGraphicsItem::ItemIsMovable, !lock);
    }
    is_locked = lock;
    emit this->locked(lock);
}

void NetworkScene::unlock(){
    this->lock(false);
}

bool NetworkScene::isLocked()
{
    return is_locked;
}
