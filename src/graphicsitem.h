#ifndef GRAPHICSITEM_H
#define GRAPHICSITEM_H

#include <QGraphicsItem>
#include "config.h"

class QMN_EXPORT GraphicsItemLayer : public QGraphicsItem
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