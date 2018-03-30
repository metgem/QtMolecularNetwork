#ifndef NODE_H
#define NODE_H

#include <QGraphicsItem>

class Edge;

class Node : public QGraphicsEllipseItem
{
public:
    Node(int index, QString label);

    int index();
    void setColor(const QColor color);
    void setLabel(QString label);
    void addEdge(Edge *edge);
    QList<Edge *> edges() const;

    enum { Type = UserType + 1 };
    int type() const { return Type; }

    virtual QVariant itemChange(GraphicsItemChange change, const QVariant &value) override;

    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override;

protected:
    void mousePressEvent(QGraphicsSceneMouseEvent *event) override;
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *event) override;

private:
    int id;
    QString label;
    QColor color;
    QList<Edge *> edgeList;
    QList<float> pieList;
};

#endif // NODE_H
