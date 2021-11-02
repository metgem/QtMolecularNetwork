#ifndef NODE_H
#define NODE_H

#include <QGraphicsItem>
#include <QApplication>
#include <QFont>
#include <QColor>
#include <QSet>
#include <QMap>
#include <QPolygonF>
#include <QVector>

#include "style.h"

class Edge;

enum NodePolygon: int {
    Circle = 0,
    Square = 1,
    Diamond = 2,
    ThinDiamond = 3,
    TriangleDown = 4,
    TriangleUp = 5,
    TriangleLeft = 6,
    TriangleRight = 7,
    Pentagon = 8,
    Octagon = 9,
    Hexagon = 10,
    Star = 11,
    Hexagram = 12,
    Octagram = 13,
    Decagram = 14,
    Plus = 15,
    X = 16,
    Mask = 17
};

static QMap<NodePolygon, QPolygonF> NODE_POLYGON_MAP{
    {NodePolygon::Square,        QPolygonF(QVector<QPointF>({QPointF(-35., 35.),    QPointF(35., 35.),
                                                           QPointF(35., -35.),    QPointF(-35., -35.)}))},
    {NodePolygon::TriangleDown,  QPolygonF(QVector<QPointF>({QPointF(0., 50.),      QPointF(-50., -28.8),  QPointF(50., -28.8)}))},
    {NodePolygon::TriangleUp,    QPolygonF(QVector<QPointF>({QPointF(0., -50.),     QPointF(-50., 28.8),   QPointF(50., 28.8)}))},
    {NodePolygon::TriangleLeft,  QPolygonF(QVector<QPointF>({QPointF(-50, 0.),      QPointF(28.8, 50),     QPointF(28.8, -50)}))},
    {NodePolygon::TriangleRight, QPolygonF(QVector<QPointF>({QPointF(50, 0.),       QPointF(-28.8, 50),    QPointF(-28.8, -50)}))},
    {NodePolygon::Diamond,       QPolygonF(QVector<QPointF>({QPointF(0., 50.),      QPointF(50., 0.),
                                                           QPointF(0., -50.),     QPointF(-50., 0.)}))},
    {NodePolygon::ThinDiamond,   QPolygonF(QVector<QPointF>({QPointF(0., 50.),      QPointF(25., 0.),
                                                           QPointF(0., -50.),     QPointF(-25., 0.)}))},
    {NodePolygon::Pentagon,      QPolygonF(QVector<QPointF>({QPointF(-50., -16.),   QPointF(-31., 42.5),   QPointF(31., 42.5),
                                                           QPointF(50., -16.),    QPointF(0., -50.)}))},
    {NodePolygon::Hexagon,       QPolygonF(QVector<QPointF>({QPointF(-43.3, 25.),   QPointF(0., 50.),      QPointF(43.30, 25.),
                                                           QPointF(43.3, -25.),   QPointF(0., -50.),     QPointF(-43.30, -25.)}))},
    {NodePolygon::Octagon,       QPolygonF(QVector<QPointF>({QPointF(-50., 21.),    QPointF(-21., 50.),    QPointF(21., 50.),
                                                           QPointF(50., 21.),     QPointF(50., -21.),    QPointF(21., -50.),
                                                           QPointF(-21., -50.),   QPointF(-50., -21.)}))},
    {NodePolygon::Star,          QPolygonF(QVector<QPointF>({QPointF(-50., -16.),   QPointF(-15., -21.),   QPointF(0., -50.),
                                                           QPointF(16., -21.),    QPointF(50., -16.),    QPointF(25., 8.),
                                                           QPointF(31., 42.3),    QPointF(0., 26.),      QPointF(-31., 42.3),
                                                           QPointF(-25., 8.)}))},
    {NodePolygon::Hexagram,      QPolygonF(QVector<QPointF>({QPointF(-50., 0.),     QPointF(-21., 12.),    QPointF(-25., 43.),
                                                           QPointF(0., 25.),      QPointF(25., 43.),     QPointF(21., 12.),
                                                           QPointF(50., 0.),      QPointF(21., -12.),    QPointF(25., -43.),
                                                           QPointF(0., -25.),     QPointF(-25., -43.),   QPointF(-21., -12.)}))},
    {NodePolygon::Octagram,      QPolygonF(QVector<QPointF>({QPointF(-46., 19.),    QPointF(-17.5, 17.5),  QPointF(-19., 46.),
                                                           QPointF(0., 25.),      QPointF(19., 46.),     QPointF(17.5, 17.5),
                                                           QPointF(46., 19.),     QPointF(25., 0.),      QPointF(46., -19.),
                                                           QPointF(17.5, -17.5),  QPointF(19., -46.),    QPointF(0., -25.),
                                                           QPointF(-19., -46.),   QPointF(-17.5, -17.5), QPointF(-46., -19.),
                                                           QPointF(-25., 0.)}))},
    {NodePolygon::Decagram,      QPolygonF(QVector<QPointF>({QPointF(-48., 16.),    QPointF(-20., 15.),    QPointF(-29., 40.),
                                                           QPointF(-8., 24.),     QPointF(0., 50.),      QPointF(8., 24.),
                                                           QPointF(29., 40.),     QPointF(20., 15.),     QPointF(48., 16.),
                                                           QPointF(25., 0.),      QPointF(48., -16.),    QPointF(20., -15.),
                                                           QPointF(29., -40.),    QPointF(8., -24.),     QPointF(0., -50.),
                                                           QPointF(-8., -24.),    QPointF(-29., -40.),   QPointF(-20., -15.),
                                                           QPointF(-48., -16.),   QPointF(-25., 0.)}))},
    {NodePolygon::Plus,          QPolygonF(QVector<QPointF>({QPointF(-50., 20.),    QPointF(-20., 20.),    QPointF(-20, 50.),
                                                           QPointF(20., 50.),     QPointF(20., 20.),     QPointF(50., 20.),
                                                           QPointF(50., -20.),    QPointF(20., -20.),    QPointF(20., -50.),
                                                           QPointF(-20., -50.),   QPointF(-20., -20.),   QPointF(-50., -20.)}))},
    {NodePolygon::X,             QPolygonF(QVector<QPointF>({QPointF(-22., 50.),    QPointF(0., 30.),      QPointF(22., 50.),
                                                           QPointF(50., 22.),     QPointF(30., 0.),      QPointF(50., -22.),
                                                           QPointF(22., -50.),    QPointF(0., -30.),     QPointF(-22., -50.),
                                                           QPointF(-50., -22.),   QPointF(-30., -0.),    QPointF(-50., 20.)}))},
    {NodePolygon::Mask,          QPolygonF(QVector<QPointF>({QPointF(-50.0, 6.),    QPointF(-6., 23.),     QPointF(6., 23.),
                                                           QPointF(50., 6.),      QPointF(44., -23.),    QPointF(0., -29.),
                                                           QPointF(-44., -23.)}))},
    };

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
    QPixmap pixmap();
    void setPixmap(const QPixmap &pixmap);
    void setPixmapFromSmiles(const QString &smiles, const QSize &size = QSize(300, 300));
    void setPixmapFromInchi(const QString &inchi, const QSize &size = QSize(300, 300));
    void setPixmapFromBase64(const QByteArray &b64);
    void setPixmapFromSvg(const QByteArray &svg, const QSize &size = QSize(300, 300));
    void scalePolygon(qreal polygon_size = 0.);
    NodePolygon polygon();
    void setPolygon(NodePolygon id);
    QPolygonF customPolygon();
    void setCustomPolygon(QPolygonF polygon, qreal polygon_size = 0.);

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
    QPixmap pixmap_;
    QPolygonF node_polygon_;
    NodePolygon stock_polygon_ = NodePolygon::Circle;;
};

Q_DECLARE_METATYPE(Node *);

#endif // NODE_H
