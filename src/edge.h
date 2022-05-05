#ifndef EDGE_H
#define EDGE_H

#include <QGraphicsPathItem>
#include <QPen>

#include "config.h"
#include "style.h"


class Node;

class QMN_EXPORT Edge : public QGraphicsPathItem
{
public:
    Edge(int index, Node *sourceNode, Node *destNode, qreal width=1.);

    int index();
    Node *sourceNode() const;
    Node *destNode() const;
    void setPen(const QPen &pen);
    qreal width();
    void setWidth(qreal width);
    void setSourceNode(Node *node);
    void setDestNode(Node *node);
    bool isSelfLoop();
    void adjust();

    void updateStyle(NetworkStyle *style, NetworkStyle *old=nullptr);
    QVariant itemChange(QGraphicsItem::GraphicsItemChange change, const QVariant &value) override;

    enum: int { Type = UserType + 2 };
    int type() const override { return Type; }

    QRectF boundingRect() const override;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override;

private:
    int id;
    QPointF sourcePoint;
    QPointF destPoint;
    Node *source, *dest;
};

Q_DECLARE_METATYPE(Edge *);

#endif // EDGE_H
