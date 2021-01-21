#include "node.h"
#include "edge.h"
#include "networkscene.h"
#include "style.h"
#include "config.h"
#include "mol_depiction.h"

#include <QtWidgets>
#include <QtCore>
#include <QString>
#include <QPixmap>
#include <QtSvg/QSvgRenderer>

Node::Node(int index, const QString &label)
    : QGraphicsEllipseItem(-RADIUS, -RADIUS, 2*RADIUS, 2*RADIUS)
{
    this->id = index;
    if (label.isNull())
        setLabel(QString::number(index+1));
    else
        setLabel(label);

    setFlags(ItemIsSelectable | ItemIsMovable | ItemSendsScenePositionChanges);
    setCacheMode(DeviceCoordinateCache);

    setBrush(Qt::lightGray);
    setPen(QPen(Qt::black, 1));
    setZValue(10);
}

void Node::invalidateShape()
{
    //TODO: Can't find a good way to update shape
    prepareGeometryChange();
    QRectF rect = this->rect();
    setRect(QRectF());
    setRect(rect);
}

void Node::updateLabelRect()
{
    QFontMetrics fm = QFontMetrics(this->font());
    int width = fm.width(this->label());
    int height = fm.height();
    this->label_rect_ = QRectF(-width/2, -height/2, width, height);

    this->invalidateShape();
}

int Node::index()
{
    return this->id;
}

int Node::radius()
{
    return int(this->rect().width() / 2);
}

void Node::setRadius(int radius)
{
    prepareGeometryChange();
    this->setRect(QRectF(-radius, -radius, 2 * radius, 2 * radius));
}

QFont Node::font()
{
    return this->font_;
}

void Node::setFont(const QFont &font)
{
    this->font_ = font;
    updateLabelRect();
}

const QColor Node::textColor()
{
    return this->text_color;
}

void Node::setTextColor(const QColor &color)
{
    this->text_color = color;
}

void Node::setBrush(const QBrush &brush, bool autoTextColor)
{
    QGraphicsEllipseItem::setBrush(brush);

    if (autoTextColor)
    {
        QColor color = brush.color();
        // Calculate the perceptive luminance (aka luma) - human eye favors green color...
        // See https://stackoverflow.com/questions/1855884/determine-font-color-based-on-background-color
        if (color.alpha() < 128)
        {
            this->text_color = QColor(Qt::black);
        }
        else
        {
            double luma = (0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()) / 255;
            this->text_color = (luma > 0.5) ? QColor(Qt::black) : QColor(Qt::white);
        }
    }
}

QString Node::label()
{
    return label_;
}

void Node::setLabel(const QString &label)
{
    this->label_ = label;
    updateLabelRect();
}

QList<qreal> Node::pie()
{
    return this->pieList;
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
    this->update();
}

QPixmap Node::pixmap()
{
    return this->pixmap_;
}

void Node::setPixmap(const QPixmap &pixmap)
{
    this->pixmap_ = pixmap;
}

void Node::setPixmapFromSmiles(const QString &smiles, const QSize &size)
{
    QPixmap pixmap(SmilesToPixmap(smiles, size));
    this->pixmap_ = pixmap;
}

void Node::setPixmapFromInchi(const QString &inchi, const QSize &size)
{
    QPixmap pixmap(InchiToPixmap(inchi, size));
    this->pixmap_ = pixmap;
}

void Node::setPixmapFromBase64(const QByteArray &b64)
{
    QPixmap pixmap;
    pixmap.loadFromData(QByteArray::fromBase64(b64));
    this->pixmap_ = pixmap;
}

void Node::addEdge(Edge *edge)
{
    this->edges_.insert(edge);
}

void Node::removeEdge(Edge *edge)
{
    this->edges_.remove(edge);
}

QSet<Edge *> Node::edges() const
{
    return this->edges_;
}

void Node::updateStyle(NetworkStyle *style, NetworkStyle *old)
{
    if (old == nullptr || this->brush().color() == old->nodeBrush().color())
    {
        setBrush(style->nodeBrush(), false);
        setTextColor(style->nodeTextColor());
    }
    setPen(style->nodePen());
    setFont(style->nodeFont());
    invalidateShape();
}

QVariant Node::itemChange(GraphicsItemChange change, const QVariant &value)
{
    switch (change)
    {
    case ItemScenePositionHasChanged:
        foreach(Edge* edge, this->edges_)
        {
            edge->adjust();
        }
        break;
    case ItemSelectedChange:
        setZValue(value.toBool() ? 20 : 10);  // Bring item to front
        setCacheMode(cacheMode()); // Force Redraw
        break;
    default:
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

QPainterPath Node::shape() const
{
    QPainterPath path = QGraphicsEllipseItem::shape();
    path.addRect(this->label_rect_);
    return path;
}

void Node::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    Q_UNUSED(widget);

    NetworkScene *scene = qobject_cast<NetworkScene *>(this->scene());
    if (scene == nullptr)
        return;

    NetworkStyle *style(scene->networkStyle());

    // If selected, change brush to yellow and text to black
    QColor text_color;
    if (option->state & QStyle::State_Selected)
    {
        QBrush brush = style->nodeBrush(true);
        text_color = style->nodeTextColor(true);
        if (!brush.color().isValid())
        {
            brush = this->brush();
            text_color = this->textColor();
        }
        painter->setBrush(brush);
        painter->setPen(style->nodePen(true));
    }
    else
    {
        painter->setBrush(this->brush());
        painter->setPen(this->pen());
        text_color = this->text_color;
    }

    qreal lod(option->levelOfDetailFromTransform(painter->worldTransform()));

    if (lod<0.1)
    {
        painter->fillRect(rect(), painter->brush());
        return;
    }

    // Draw ellipse
    if (spanAngle() != 0 && qAbs(spanAngle() % (360 * 16)) == 0)
        painter->drawEllipse(rect());
    else
        painter->drawPie(rect(), startAngle(), spanAngle());

    // Draw pie if any
    if (scene->pieChartsVisibility() && lod > 0.1 && this->pieList.size() > 0)
    {
        int radius = this->radius();
        QRectF rect(-0.85*radius, -0.85*radius, 1.7*radius, 1.7*radius);
        float start = 0;
        QList<QColor> colors = scene->pieColors();
        painter->setPen(QPen(Qt::NoPen));
        for (int i=0; i<std::min(this->pieList.size(), colors.size()); i++) {
            painter->setBrush(colors[i]);
            painter->drawPie(rect, int(start*5760), int(pieList[i]*5760));
            start += this->pieList[i];
        }
    }

    // Draw text
    if (lod > 0.4)
    {
        QRectF bounding_rect = boundingRect();
        painter->setFont(this->font_);
        painter->setPen(QPen(text_color, 0));
        painter->drawText(bounding_rect, Qt::AlignCenter, label_);
        if (scene->pixmapVisibility() && !this->pixmap_.isNull())
        {
            painter->drawPixmap(bounding_rect.toRect(), this->pixmap_, this->pixmap_.rect());
        }
    }
}
