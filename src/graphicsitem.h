#ifndef GRAPHICSITEM_H
#define GRAPHICSITEM_H

#include <QGraphicsItem>

class GraphicsItemLayer : public QGraphicsItem
{
public:
    QRectF boundingRect() const
    {
        return QRectF(0,0,0,0);
    }

    void paint(QPainter *, const QStyleOptionGraphicsItem *, QWidget *)
    {
    }
};

#endif // GRAPHICSITEM_H
