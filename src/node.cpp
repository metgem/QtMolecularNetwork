#include "node.h"
#include "edge.h"
#include "networkscene.h"
#include "style.h"

#include <QtWidgets>
#include <QtCore>
#include <QString>

Node::Node(int index, int radius, QString label)
    : QGraphicsEllipseItem(-radius, -radius, 2*radius, 2*radius)
{
    this->id = index;
    this->radius_ = radius;
    if (label==0)
        label = QString::number(index+1);
    this->label_ = label;

    setFlags(ItemIsSelectable | ItemIsMovable | ItemSendsScenePositionChanges);
    setCacheMode(DeviceCoordinateCache);

    setBrush(Qt::lightGray);
    setPen(QPen(Qt::black, 1));
}

int Node::index()
{
    return this->id;
}

int Node::radius()
{
    return this->radius_;
}

void Node::setRadius(int radius)
{
    this->radius_ = radius;
    this->setRect(QRectF(-radius, -radius, 2 * radius, 2 * radius));
}

QFont Node::font()
{
    return this->font_;
}

void Node::setFont(QFont font)
{
    this->font_ = font;
}

const QColor Node::textColor()
{
    return this->text_color;
}

void Node::setTextColor(const QColor color)
{
    this->text_color = color;
}

void Node::setBrush(const QBrush brush, bool autoTextColor)
{
    QGraphicsEllipseItem::setBrush(brush);

    if (autoTextColor)
    {
        QColor color = brush.color();
        // Calculate the perceptive luminance (aka luma) - human eye favors green color...
        // See https://stackoverflow.com/questions/1855884/determine-font-color-based-on-background-color
        double luma = 0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue() / 255;
        this->text_color = (luma > 0.5) ? QColor(Qt::black) : QColor(Qt::white);
    }
}

QString Node::label()
{
    return label_;
}

void Node::setLabel(QString label)
{
    this->label_ = label;
    if (isVisible())
        update();
}

void Node::setPie(QList<qreal> values)
{
    qreal sum = 0;
    for (int i=0; i<values.size(); i++) {
        sum += values[i];
    }
    if (sum>0)
    {
        for (int i=0; i<values.size(); i++) {
            values[i] /= sum;
        }
    }
    else
        values = QList<qreal>();
    this->pieList = values;
    if (isVisible())
        update();
}

void Node::addEdge(Edge *edge)
{
    edgeList << edge;
}

QList<Edge *> Node::edges() const
{
    return edgeList;
}

void Node::updateStyle(NetworkStyle *style, NetworkStyle* old)
{
    setRadius(style->nodeRadius());
    if (old == NULL || this->brush().color() == old->nodeBrush().color())
        setBrush(style->nodeBrush(), false);
    setTextColor(style->nodeTextColor());
    setPen(style->nodePen());
    setFont(style->nodeFont());
    update();
}

QVariant Node::itemChange(GraphicsItemChange change, const QVariant &value)
{
    switch (change)
    {
    case ItemScenePositionHasChanged:
        foreach(Edge* edge, edgeList)
        {
            edge->adjust();
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

QRectF Node::boundingRect() const
{
    QRectF brect = QGraphicsEllipseItem::boundingRect();
    int pwidth = this->pen().width();
    int size = 2 * (this->radius_ + pwidth);
    return QRectF(brect.x() - pwidth, brect.y() - pwidth, size, size);
}

void Node::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *)
{
    NetworkScene *scene = qobject_cast<NetworkScene *>(this->scene());
    if (scene == 0)
        return;

    // If selected, change brush to yellow and text to black
    QColor text_color;
    if (option->state & QStyle::State_Selected)
    {
        QBrush brush = scene->networkStyle()->nodeBrush("selected");
        if (brush.color().isValid())
            painter->setBrush(brush);
        else
            painter->setBrush(this->brush());
        text_color = scene->networkStyle()->nodeTextColor("selected");
        if (!text_color.isValid())
            text_color = this->text_color;
        painter->setPen(scene->networkStyle()->nodePen("selected"));
    }
    else
    {
        painter->setBrush(this->brush());
        painter->setPen(this->pen());
        text_color = this->text_color;
    }

    // Draw ellipse
    if (spanAngle() != 0 && qAbs(spanAngle() % (360 * 16)) == 0)
        painter->drawEllipse(rect());
    else
        painter->drawPie(rect(), startAngle(), spanAngle());

    qreal lod(option->levelOfDetailFromTransform(painter->worldTransform()));

    // Draw pie if any
    if (lod > 0.1 && this->pieList.size() > 0)
    {
        int radius = this->radius();
        QRectF rect(-0.85*radius, -0.85*radius, 1.7*radius, 1.7*radius);
        float start = 0;
        QList<QColor> colors = scene->pieColors();
        painter->setPen(QPen(Qt::NoPen));
        for (int i=0; i<this->pieList.size(); i++) {
            painter->setBrush(colors[i]);
            painter->drawPie(rect, start*5760, pieList[i]*5760);
            start += this->pieList[i];
        }
    }

    // Draw text
    if (lod > 0.4)
    {
        painter->setFont(this->font_);
        painter->setPen(QPen(text_color, 0));
        painter->drawText(rect(), Qt::AlignCenter, label_);
    }
}
