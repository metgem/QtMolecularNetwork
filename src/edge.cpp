#include "edge.h"
#include "node.h"
#include "networkscene.h"
#include "style.h"

#include <QtGui>
#include <QtCore>
#include <QStyleOption>

Edge::Edge(int index, Node *sourceNode, Node *destNode, qreal width)
{
    this->id = index;
    this->source = sourceNode;
    this->dest = destNode;

    if (sourceNode)
        source->addEdge(this);
    if (destNode && source != dest)
        dest->addEdge(this);

    setPen(QPen(Qt::darkGray));
    setWidth(width);

    setAcceptedMouseButtons(Qt::LeftButton);
    setFlag(ItemIsSelectable);
    setZValue(-1);
}

int Edge::index()
{
    return this->id;
}

Node *Edge::sourceNode() const
{
    return source;
}

void Edge::setSourceNode(Node *node)
{
    this->source->removeEdge(this);
    this->source = node;
    this->source->addEdge(this);
    adjust();
}

Node *Edge::destNode() const
{
    return dest;
}

void Edge::setDestNode(Node *node)
{
    this->dest->removeEdge(this);
    this->dest = node;
    this->dest->addEdge(this);
    adjust();
}

void Edge::setPen(const QPen &pen)
{
    QPen new_pen = QPen(pen);
    new_pen.setWidthF(this->pen().widthF());
    QGraphicsPathItem::setPen(new_pen);
}

qreal Edge::width()
{
    return this->pen().widthF();
}

void Edge::setWidth(qreal width)
{
    QPen pen(this->pen());
    if ((source != dest) && width >= 0)
    {
        pen.setWidthF(width);
    }
    else
    {
        pen.setWidth(1);
    }
    QGraphicsPathItem::setPen(pen);
}

bool Edge::isSelfLoop()
{
    return (source == dest) && source;
}

void Edge::adjust()
{
    if (!source || !dest)
        return;

    QLineF line(mapFromItem(source, 0., 0.), mapFromItem(dest, 0., 0.));
    qreal length = line.length();

    prepareGeometryChange();

    qreal min_len = source->radius() + dest->radius() + source->pen().widthF() + dest->pen().widthF();

    if (length > min_len) {
        QPointF offset((line.dx() * (source->radius() + source->pen().widthF() + 1)) / length,
                           (line.dy() * (source->radius() + source->pen().width() + 1)) / length);
        sourcePoint = line.p1() + offset;
        offset = QPointF((line.dx() * (dest->radius() + dest->pen().widthF() + 1)) / length,
                         (line.dy() * (dest->radius() + dest->pen().widthF() + 1)) / length);
        destPoint = line.p2() - offset;
    } else {
        sourcePoint = destPoint = line.p1();
    }

    QPainterPath path;

    if (source == dest)
    {
        int radius  = source->radius();
        path.moveTo(sourcePoint.x() - radius - 2 * source->pen().widthF(),
                    sourcePoint.y());
        path.cubicTo(QPointF(sourcePoint.x() - 4 * radius, sourcePoint.y()),
                     QPointF(sourcePoint.x(),              sourcePoint.y() - 4 * radius),
                     QPointF(sourcePoint.x(),              sourcePoint.y() - radius - 2 * source->pen().widthF()));
    }
    else
    {
        path.moveTo(sourcePoint);
        path.lineTo(destPoint);
    }
    setPath(path);
}

void Edge::updateStyle(NetworkStyle *style, NetworkStyle *old)
{
    Q_UNUSED(old);
    setPen(style->edgePen());
    update();
}

QVariant Edge::itemChange(QGraphicsItem::GraphicsItemChange change, const QVariant &value)
{
    if (change == QGraphicsItem::ItemSelectedChange)
    {
        setZValue(isSelected() ? 0 : -1); // Bring item to front
        setCacheMode(cacheMode()); // Force redraw
    }
    return QGraphicsPathItem::itemChange(change, value);
}

QRectF Edge::boundingRect() const
{
    if (!source || !dest)
        return QRectF();

    QRectF brect = QGraphicsPathItem::boundingRect();

    if (source == dest)
    {
        qreal w(pen().widthF());
        qreal radius = (qreal) source->radius();
        qreal width = source->pen().widthF();
        qreal delta = int(2 * radius - 2 * width - w);
        qreal size = int(2 * (radius + width + 1 + w));
        return QRectF(brect.x() + delta, brect.y() + delta, size, size);
    }

    return brect;
}

void Edge::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *)
{
    if (!source || !dest)
        return;

    qreal lod(option->levelOfDetailFromTransform(painter->worldTransform()));

    if (lod<0.1)
    {
        return;
    }

    NetworkScene *scene = qobject_cast<NetworkScene *>(this->scene());
    if (scene == nullptr)
        return;

    QLineF line(sourcePoint, destPoint);
    if ((source != dest) && qFuzzyCompare(line.length(), qreal(0.)))
        return;

    if (option->state & QStyle::State_Selected)
    {
        QPen pen = scene->networkStyle()->edgePen(true);
        pen.setWidthF(this->pen().widthF());
        painter->setPen(pen);
    }
    else
        painter->setPen(this->pen());

    painter->drawPath(path());
}
