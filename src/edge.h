#ifndef EDGE_H
#define EDGE_H

#include <QGraphicsPathItem>
#include <QPen>

#include "style.h"

class Node;

class Edge : public QGraphicsPathItem
{
public:
    Edge(int index, Node *sourceNode, Node *destNode, qreal weight=1, qreal width=1);

    int index();
    Node *sourceNode() const;
    Node *destNode() const;
    void setPen(QPen pen);
    qreal width();
    void setWidth(qreal width);
    void setSourceNode(Node *node);
    void setDestNode(Node *node);
    void adjust();

    void updateStyle(NetworkStyle *style, NetworkStyle *old=NULL);

    enum { Type = UserType + 2 };
    int type() const { return Type; }

    virtual QVariant itemChange(GraphicsItemChange change, const QVariant &value) override;

    QRectF boundingRect() const override;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override;

private:
    int id;
    QPointF sourcePoint;
    QPointF destPoint;
    qreal weight;
    Node *source, *dest;
};

#endif // EDGE_H
