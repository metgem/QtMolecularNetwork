#ifndef EDGE_H
#define EDGE_H

#include <QGraphicsPathItem>

class Node;

class Edge : public QGraphicsPathItem
{
public:
    Edge(int index, Node *sourceNode, Node *destNode, qreal weight=1, qreal width=1);
    Node *sourceNode() const;
    Node *destNode() const;
    void setColor(const QColor color);
    void setWidth(qreal width);
    void setSourceNode(Node *node);
    void setDestNode(Node *node);
    void adjust();

    enum { Type = UserType + 2 };
    int type() const override { return Type; }

    virtual QVariant itemChange(GraphicsItemChange change, const QVariant &value) override;

protected:
    QRectF boundingRect() const override;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override;

private:
    int index;
    QPointF sourcePoint;
    QPointF destPoint;
    qreal weight;
    Node *source, *dest;
};

#endif // EDGE_H
