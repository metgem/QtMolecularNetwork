#ifndef NODE_H
#define NODE_H

#include <QGraphicsItem>
#include <QApplication>
#include <QFont>
#include <QColor>
#include <QSet>

#include "style.h"

class Edge;

class Q_DECL_EXPORT Node : public QGraphicsEllipseItem
{
public:
    Node(int index, const QString &label=QString());

    void invalidateShape();
    void updateLabelRect();
    int index();
    int radius();
    void setRadius(int radius);
    QFont font();
    void setFont(const QFont &font);
    const QColor textColor();
    void setTextColor(const QColor &color);
    void setBrush(const QBrush &brush, bool autoTextColor=true);
    QString label();
    void setLabel(const QString &label);
    QList<qreal> pie();
    void setPie(QList<qreal> values);

    void addEdge(Edge *edge);
    void removeEdge(Edge *edge);
    QSet<Edge *> edges() const;

    void updateStyle(NetworkStyle *style, NetworkStyle* old=nullptr);

    enum { Type = UserType + 1 };
    int type() const override { return Type; }

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
    QSet<Edge *> edges_;
    QList<qreal> pieList;
};

Q_DECLARE_METATYPE(Node *);

#endif // NODE_H
