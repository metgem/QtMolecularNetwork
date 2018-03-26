#include "node.h"
#include "edge.h"
#include "config.h"

#include <QtWidgets>
#include <QtCore>

Node::Node(int index, QString label)
    : QGraphicsEllipseItem(-RADIUS, -RADIUS, 2*RADIUS, 2*RADIUS)
{
    this->index = index;
    this->label = label;

    setFlags(ItemIsSelectable | ItemIsMovable | ItemSendsGeometryChanges);

    setCacheMode(DeviceCoordinateCache);

    setColor(Qt::lightGray);
}

void Node::setColor(const QColor color)
{
    this->color = color;
}

void Node::setLabel(QString label)
{
    this->label = label;
    setCacheMode(cacheMode()); // Force redraw
}

void Node::addEdge(Edge *edge)
{
    edgeList << edge;
    edge->adjust();
}

QList<Edge *> Node::edges() const
{
    return edgeList;
}

QVariant Node::itemChange(GraphicsItemChange change, const QVariant &value)
{
    switch (change)
    {
    case ItemPositionHasChanged:
        for (int i = 0; i < edgeList.size(); ++i) {
            edgeList.at(i)->adjust();
        }
        break;
    case ItemSelectedChange:
        setZValue(!isSelected());  // Bring item to front
        setCacheMode(cacheMode()); // Force Redraw
        break;
    }

    return QGraphicsItem::itemChange(change, value);
}

void Node::mousePressEvent(QGraphicsSceneMouseEvent *event)
{
    update();
    QGraphicsItem::mousePressEvent(event);
}

void Node::mouseReleaseEvent(QGraphicsSceneMouseEvent *event)
{
    update();
    QGraphicsItem::mouseReleaseEvent(event);
}

void Node::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *)
{
    // If selected, change brush to yellow
    if (option->state & QStyle::State_Selected)
        painter->setBrush(Qt::yellow);
    else
        painter->setBrush(color);

    // Draw ellipse
    if (spanAngle() != 0 && qAbs(spanAngle() % (360 * 16)) == 0)
        painter->drawEllipse(rect());
    else
        painter->drawPie(rect(), startAngle(), spanAngle());

    qreal lod(option->levelOfDetailFromTransform(painter->worldTransform()));

    // Draw pie if any
    if (lod > 0.1 && pieList.size() > 0)
    {
        QRectF rect(-0.85*RADIUS, -0.85*RADIUS, 1.7*RADIUS, 1.7*RADIUS);
        float start(0);

        painter->setPen(QPen(Qt::NoPen));
        for (int i = 0; i < pieList.size(); ++i) {
            float v(pieList.at(i));
            painter->drawPie(rect, start*5760, v*5760);
            start += v;
        }
    }

    // Draw text
    if (lod > 0.4)
    {
        QFont font;
        font = painter->font();
        font.setPixelSize(FONT_SIZE);
        painter->setFont(font);
        painter->setPen(QPen(Qt::black, 0));
        painter->drawText(rect(), Qt::AlignCenter, label);
    }
}
