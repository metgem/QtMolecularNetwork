#ifndef NODE_H
#define NODE_H

#include <QGraphicsItem>
#include <QApplication>
#include <QFont>
#include <QColor>

#include "style.h"

class Edge;

class Node : public QGraphicsEllipseItem
{
public:
    Node(int index, QString label=NULL);

    void invalidateShape();
    int index();
    int radius();
    void setRadius(int radius);
    QFont font();
    void setFont(QFont font);
    const QColor textColor();
    void setTextColor(const QColor color);
    void setBrush(const QBrush brush, bool autoTextColor=true);
    QString label();
    void setLabel(QString label);
    QList<qreal> pie();
    void setPie(QList<qreal> values);

    void addEdge(Edge *edge);
    QList<Edge *> edges() const;

    void updateStyle(NetworkStyle *style, NetworkStyle* old=NULL);

    enum { Type = UserType + 1 };
    int type() const { return Type; }

    virtual QVariant itemChange(GraphicsItemChange change, const QVariant &value) override;
    QPainterPath shape() const override;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override;

protected:
    void mousePressEvent(QGraphicsSceneMouseEvent *event) override;
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *event) override;

private:
    int id;
    QString label_;
    QRectF label_rect_;
    QFont font_ = QApplication::font();
    QColor text_color;
    QList<Edge *> edgeList;
    QList<qreal> pieList;
};

#endif // NODE_H
