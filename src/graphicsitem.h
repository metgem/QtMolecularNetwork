#ifndef GRAPHICSITEM_H
#define GRAPHICSITEM_H

#include <QGraphicsItem>

class GraphicsItemLayer : public QGraphicsItem
{
public:
    QRectF boundingRect() const override
    {
        return QRectF(0,0,0,0);
    }

    void paint(QPainter *, const QStyleOptionGraphicsItem *, QWidget *) override
    {
    }
};

#endif // GRAPHICSITEM_H
