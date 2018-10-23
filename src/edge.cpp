#include "edge.h"
#include "node.h"
#include "networkscene.h"
#include "style.h"

#include <QtGui>
#include <QtCore>
#include <QStyleOption>

Edge::Edge(int index, Node *sourceNode, Node *destNode, qreal weight, qreal width)
{
    this->id = index;
    this->weight = weight;
    this->source = sourceNode;
    this->dest = destNode;

    source->addEdge(this);
    if (source != dest)
        dest->addEdge(this);

    setPen(QPen(Qt::darkGray));
    setWidth(width);

    setAcceptedMouseButtons(Qt::LeftButton);
    setFlag(ItemIsSelectable);
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
    this->source = node;
    adjust();
}

Node *Edge::destNode() const
{
    return dest;
}

void Edge::setDestNode(Node *node)
{
    this->dest = node;
    adjust();
}

void Edge::setPen(QPen pen)
{
    pen.setWidth(this->pen().width());
    QGraphicsPathItem::setPen(pen);
}

qreal Edge::width()
{
    return this->pen().width();
}

void Edge::setWidth(qreal width)
{
    QPen pen(this->pen());
    if ((source != dest) && width)
    {
        pen.setWidth(width);
    }
    else
    {
        pen.setWidth(1);
    }
    QGraphicsPathItem::setPen(pen);
}

void Edge::adjust()
{
    if (!source || !dest)
        return;

    QLineF line(mapFromItem(source, 0, 0), mapFromItem(dest, 0, 0));
    qreal length = line.length();

    prepareGeometryChange();

    int min_len = source->radius() + dest->radius() + source->pen().width() + dest->pen().width();

    if (length > qreal(min_len)) {
        QPointF offset((line.dx() * (source->radius() + source->pen().width() + 1)) / length,
                           (line.dy() * (source->radius() + source->pen().width() + 1)) / length);
        sourcePoint = line.p1() + offset;
        offset = QPointF((line.dx() * (dest->radius() + dest->pen().width())) / length,
                         (line.dy() * (dest->radius() + dest->pen().width())) / length);
        destPoint = line.p2() - offset;
    } else {
        sourcePoint = destPoint = line.p1();
    }

    QPainterPath path;

    if (source == dest)
    {
        int radius  = source->radius();
        path.moveTo(sourcePoint.x() - radius - 2 * source->pen().width(),
                    sourcePoint.y());
        path.cubicTo(QPointF(sourcePoint.x() - 4 * radius, sourcePoint.y()),
                     QPointF(sourcePoint.x(),              sourcePoint.y() - 4 * radius),
                     QPointF(sourcePoint.x(),              sourcePoint.y() - radius - 2 * source->pen().width()));
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

QVariant Edge::itemChange(GraphicsItemChange change, const QVariant &value)
{
    if (change == ItemSelectedChange)
    {
        setZValue(!isSelected());  // Bring item to front
        setCacheMode(cacheMode()); // Force redraw
    }

    return QGraphicsItem::itemChange(change, value);
}

QRectF Edge::boundingRect() const
{
    if (!source || !dest)
        return QRectF();

    QRectF brect = QGraphicsPathItem::boundingRect();

    if (source == dest)
    {
        qreal w(pen().width());
        int radius = source->radius();
        int width = source->pen().width();
        int delta = 2 * radius - 2 * width - w;
        int size = 2 * (radius + width + 1 + w);
        return QRectF(brect.x()+delta, brect.y() + delta, size, size);
    }

    return brect;
}

void Edge::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *)
{
    if (!source || !dest)
        return;

    NetworkScene *scene = qobject_cast<NetworkScene *>(this->scene());
    if (scene == 0)
        return;

    QLineF line(sourcePoint, destPoint);
    if ((source != dest) && qFuzzyCompare(line.length(), qreal(0.)))
        return;

    if (option->state & QStyle::State_Selected)
    {
        QPen pen = scene->networkStyle()->edgePen("selected");
        pen.setWidth(this->pen().width());
        painter->setPen(pen);
    }
    else
        painter->setPen(this->pen());

    painter->drawPath(path());
}
