#ifndef NODE_H
#define NODE_H

#include <QGraphicsItem>

class Edge;

class Node : public QGraphicsEllipseItem
{
public:
    Node(int index, QString label=0);

    int index();
    const QColor color();
    void setColor(const QColor color);
    QString label();
    void setLabel(QString label);
    void setPie(QList<qreal> values);

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
    QString label_;
    QColor color_;
    QList<Edge *> edgeList;
    QList<qreal> pieList;
};

#endif // NODE_H
