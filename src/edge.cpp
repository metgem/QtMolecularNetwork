#include "edge.h"
#include "config.h"
#include "node.h"

#include <QtGui>
#include <QtCore>
#include <QStyleOption>

Edge::Edge(int index, Node *sourceNode, Node *destNode, qreal weight, qreal width)
{
    this->index = index;
    this->weight = weight;
    this->source = sourceNode;
    this->dest = destNode;

    source->addEdge(this);
    if (source != dest)
        dest->addEdge(this);

    setAcceptedMouseButtons(Qt::LeftButton);
    setColor(Qt::darkGray);
    setWidth(width);
    adjust();

    setFlag(ItemIsSelectable);
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

void Edge::setColor(const QColor color)
{
    QPen pen;
    pen.setColor(color);
    setPen(pen);
}

void Edge::setWidth(qreal width)
{
    QPen pen;
    if ((source != dest) && width)
    {;
        pen.setWidth(width);
    }
    else
    {
        pen.setWidth(1);
    }
}

void Edge::adjust()
{
    if (!source || !dest)
        return;

    QLineF line(mapFromItem(source, 0, 0), mapFromItem(dest, 0, 0));
    qreal length = line.length();

    prepareGeometryChange();

    if (length > qreal(2*RADIUS+NODE_BORDER_WIDTH)) {
        QPointF edgeOffset((line.dx() * (RADIUS + NODE_BORDER_WIDTH + 1)) / length,
                           (line.dy() * (RADIUS + NODE_BORDER_WIDTH + 1)) / length);
        sourcePoint = line.p1() + edgeOffset;
        destPoint = line.p2() - edgeOffset;
    } else {
        sourcePoint = destPoint = line.p1();
    }

    QPainterPath path;

    if (source == dest)
    {
        path.moveTo(sourcePoint.x()-RADIUS-NODE_BORDER_WIDTH*2,
                    sourcePoint.y());
        path.cubicTo(QPointF(sourcePoint.x()-4*RADIUS, sourcePoint.y()),
                     QPointF(sourcePoint.x(),          sourcePoint.y()-4*RADIUS),
                     QPointF(sourcePoint.x(),          sourcePoint.y()-RADIUS-NODE_BORDER_WIDTH*2));
    }
    else
    {
        path.moveTo(sourcePoint);
        path.lineTo(destPoint);
    }
    setPath(path);
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

    QRectF brect(QGraphicsPathItem::boundingRect());

    if (source == dest)
    {
        qreal w(pen().width());
        return QRectF(brect.x()+2*RADIUS-NODE_BORDER_WIDTH*2-w,
                       brect.y()+2*RADIUS-NODE_BORDER_WIDTH*2-w,
                       2*(RADIUS+NODE_BORDER_WIDTH+1+w),
                       2*(RADIUS+NODE_BORDER_WIDTH+1+w));
    }

    return brect;
}

void Edge::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *)
{
    if (!source || !dest)
        return;

    QLineF line(sourcePoint, destPoint);
    if ((source != dest) && qFuzzyCompare(line.length(), qreal(0.)))
        return;

    QPen pen(this->pen());

    if (option->state & QStyle::State_Selected)
    {
        pen.setColor(Qt::red);
    }

    painter->setPen(pen);
    painter->drawPath(path());
}
