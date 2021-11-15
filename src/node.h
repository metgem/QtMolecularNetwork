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
    Custom = -1,
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
    Mask = 17,
    Heart = 18,
    Spade = 19,
    Club = 20
};

static QMap<NodePolygon, QPolygonF> NODE_POLYGON_MAP{
    {NodePolygon::Square,        QPolygonF(QVector<QPointF>({QPointF(-35., 35.),    QPointF(35., 35.),
                                                             QPointF(35., -35.),    QPointF(-35., -35.)}))},
    {NodePolygon::TriangleDown,  QPolygonF(QVector<QPointF>({QPointF(0., 50.),      QPointF(-50., -28.8),    QPointF(50., -28.8)}))},
    {NodePolygon::TriangleUp,    QPolygonF(QVector<QPointF>({QPointF(0., -50.),     QPointF(-50., 28.8),     QPointF(50., 28.8)}))},
    {NodePolygon::TriangleLeft,  QPolygonF(QVector<QPointF>({QPointF(-50, 0.),      QPointF(28.8, 50),       QPointF(28.8, -50)}))},
    {NodePolygon::TriangleRight, QPolygonF(QVector<QPointF>({QPointF(50, 0.),       QPointF(-28.8, 50),      QPointF(-28.8, -50)}))},
    {NodePolygon::Diamond,       QPolygonF(QVector<QPointF>({QPointF(0., 50.),      QPointF(50., 0.),
                                                             QPointF(0., -50.),     QPointF(-50., 0.)}))},
    {NodePolygon::ThinDiamond,   QPolygonF(QVector<QPointF>({QPointF(0., 50.),      QPointF(25., 0.),
                                                             QPointF(0., -50.),     QPointF(-25., 0.)}))},
    {NodePolygon::Pentagon,      QPolygonF(QVector<QPointF>({QPointF(-50., -16.),   QPointF(-31., 42.5),     QPointF(31., 42.5),
                                                             QPointF(50., -16.),    QPointF(0., -50.)}))},
    {NodePolygon::Hexagon,       QPolygonF(QVector<QPointF>({QPointF(-43.3, 25.),   QPointF(0., 50.),        QPointF(43.30, 25.),
                                                             QPointF(43.3, -25.),   QPointF(0., -50.),       QPointF(-43.30, -25.)}))},
    {NodePolygon::Octagon,       QPolygonF(QVector<QPointF>({QPointF(-50., 21.),    QPointF(-21., 50.),      QPointF(21., 50.),
                                                             QPointF(50., 21.),     QPointF(50., -21.),      QPointF(21., -50.),
                                                             QPointF(-21., -50.),   QPointF(-50., -21.)}))},
    {NodePolygon::Star,          QPolygonF(QVector<QPointF>({QPointF(-50., -16.),   QPointF(-15., -21.),     QPointF(0., -50.),
                                                             QPointF(16., -21.),    QPointF(50., -16.),      QPointF(25., 8.),
                                                             QPointF(31., 42.3),    QPointF(0., 26.),        QPointF(-31., 42.3),
                                                             QPointF(-25., 8.)}))},
    {NodePolygon::Hexagram,      QPolygonF(QVector<QPointF>({QPointF(-50., 0.),     QPointF(-21., 12.),      QPointF(-25., 43.),
                                                             QPointF(0., 25.),      QPointF(25., 43.),       QPointF(21., 12.),
                                                             QPointF(50., 0.),      QPointF(21., -12.),      QPointF(25., -43.),
                                                             QPointF(0., -25.),     QPointF(-25., -43.),     QPointF(-21., -12.)}))},
    {NodePolygon::Octagram,      QPolygonF(QVector<QPointF>({QPointF(-46., 19.),    QPointF(-17.5, 17.5),    QPointF(-19., 46.),
                                                             QPointF(0., 25.),      QPointF(19., 46.),       QPointF(17.5, 17.5),
                                                             QPointF(46., 19.),     QPointF(25., 0.),        QPointF(46., -19.),
                                                             QPointF(17.5, -17.5),  QPointF(19., -46.),      QPointF(0., -25.),
                                                             QPointF(-19., -46.),   QPointF(-17.5, -17.5),   QPointF(-46., -19.),
                                                             QPointF(-25., 0.)}))},
    {NodePolygon::Decagram,      QPolygonF(QVector<QPointF>({QPointF(-48., 16.),    QPointF(-20., 15.),      QPointF(-29., 40.),
                                                             QPointF(-8., 24.),     QPointF(0., 50.),        QPointF(8., 24.),
                                                             QPointF(29., 40.),     QPointF(20., 15.),       QPointF(48., 16.),
                                                             QPointF(25., 0.),      QPointF(48., -16.),      QPointF(20., -15.),
                                                             QPointF(29., -40.),    QPointF(8., -24.),       QPointF(0., -50.),
                                                             QPointF(-8., -24.),    QPointF(-29., -40.),     QPointF(-20., -15.),
                                                             QPointF(-48., -16.),   QPointF(-25., 0.)}))},
    {NodePolygon::Plus,          QPolygonF(QVector<QPointF>({QPointF(-50., 20.),    QPointF(-20., 20.),      QPointF(-20, 50.),
                                                             QPointF(20., 50.),     QPointF(20., 20.),       QPointF(50., 20.),
                                                             QPointF(50., -20.),    QPointF(20., -20.),      QPointF(20., -50.),
                                                             QPointF(-20., -50.),   QPointF(-20., -20.),     QPointF(-50., -20.)}))},
    {NodePolygon::X,             QPolygonF(QVector<QPointF>({QPointF(-22., 50.),    QPointF(0., 30.),        QPointF(22., 50.),
                                                             QPointF(50., 22.),     QPointF(30., 0.),        QPointF(50., -22.),
                                                             QPointF(22., -50.),    QPointF(0., -30.),       QPointF(-22., -50.),
                                                             QPointF(-50., -22.),   QPointF(-30., -0.),      QPointF(-50., 20.)}))},
    {NodePolygon::Mask,          QPolygonF(QVector<QPointF>({QPointF(-5.2, -40.5),  QPointF(-10.4, -38.0),   QPointF(-22.5, -31.4),
                                                             QPointF(-28.2, -28.6), QPointF(-34.4, -26.0),   QPointF(-44.2, -23.1),
                                                             QPointF(-44.2, -8.2),  QPointF(-44.8, 17.5),    QPointF(-29.3, 27.8),
                                                             QPointF(-10.0, 39.6),  QPointF(-5.1, 40.6),     QPointF(-0.0, 40.9),
                                                             QPointF(5.1, 40.6),    QPointF(10.0, 39.6),     QPointF(29.3, 27.8),
                                                             QPointF(44.8, 17.5),   QPointF(44.2, -8.2),     QPointF(44.2, -23.1),
                                                             QPointF(34.4, -26.0),  QPointF(28.2, -28.6),    QPointF(22.5, -31.4),
                                                             QPointF(10.4, -38.0),  QPointF(4.4, -40.7),     QPointF(0.0, -40.9)}))},
    {NodePolygon::Heart,         QPolygonF(QVector<QPointF>({QPointF(-0.0, 55.8),   QPointF(-7.4, 50.0),     QPointF(-23.8, 35.2),
                                                             QPointF(-32.6, 25.8),  QPointF(-40.2, 15.6),    QPointF(-45.6, 5.2),
                                                             QPointF(-47.1, 0.0),   QPointF(-47.7, -5.0),    QPointF(-47.2, -9.9),
                                                             QPointF(-45.8, -14.6), QPointF(-43.5, -18.9),   QPointF(-40.3, -22.7),
                                                             QPointF(-36.5, -25.8), QPointF(-32.2, -28.1),   QPointF(-27.5, -29.5),
                                                             QPointF(-22.6, -30.0), QPointF(-15.6, -29.0),   QPointF(-9.2, -26.1),
                                                             QPointF(-3.9, -21.6),  QPointF(-0.0, -15.7),    QPointF(3.9, -21.6),
                                                             QPointF(9.2, -26.1),   QPointF(15.6, -29.0),    QPointF(22.6, -30.0),
                                                             QPointF(27.5, -29.5),  QPointF(32.2, -28.1),    QPointF(36.5, -25.8),
                                                             QPointF(40.3, -22.7),  QPointF(43.5, -18.9),    QPointF(45.8, -14.6),
                                                             QPointF(47.2, -9.9),   QPointF(47.7, -5.0),     QPointF(47.1, 0.0),
                                                             QPointF(45.6, 5.2),    QPointF(40.2, 15.6),     QPointF(32.6, 25.8),
                                                             QPointF(23.8, 35.2),   QPointF(7.4, 50.0),      QPointF(-0.0, 55.8)}))},
    {NodePolygon::Spade,         QPolygonF(QVector<QPointF>({QPointF(40.7, 13.2),   QPointF(38.6, 5.5),      QPointF(34.0, -3.3),
                                                             QPointF(27.6, -12.6),  QPointF(20.4, -22.0),    QPointF(6.9, -38.8),
                                                             QPointF(2.2, -45.3),   QPointF(0.2, -49.8),     QPointF(-1.8, -45.3),
                                                             QPointF(-6.5, -38.9),  QPointF(-20.0, -22.0),   QPointF(-27.3, -12.6),
                                                             QPointF(-33.6, -3.3),  QPointF(-38.2, 5.5),     QPointF(-40.3, 13.2),
                                                             QPointF(-40.1, 17.8),  QPointF(-39.2, 21.8),    QPointF(-37.5, 25.0),
                                                             QPointF(-35.2, 27.6),  QPointF(-29.5, 30.9),    QPointF(-23.1, 32.0),
                                                             QPointF(-19.7, 31.4),  QPointF(-16.5, 29.9),    QPointF(-10.8, 25.2),
                                                             QPointF(-3.5, 16.5),   QPointF(-4.3, 22.8),     QPointF(-7.5, 33.3),
                                                             QPointF(-11.4, 43.1),  QPointF(-13.2, 46.3),    QPointF(-14.5, 47.5),
                                                             QPointF(14.9, 47.5),   QPointF(13.6, 46.3),     QPointF(11.8, 43.1),
                                                             QPointF(7.8, 33.3),    QPointF(4.7, 22.8),      QPointF(3.9, 16.5),
                                                             QPointF(10.6, 25.0),   QPointF(16.3, 29.8),     QPointF(19.7, 31.3),
                                                             QPointF(23.5, 32.0),   QPointF(29.9, 30.9),     QPointF(35.6, 27.6),
                                                             QPointF(37.9, 25.0),   QPointF(39.5, 21.8),     QPointF(40.5, 17.8),
                                                             QPointF(40.7, 13.2),   QPointF(40.7, 13.2)}))},
    {NodePolygon::Club,          QPolygonF(QVector<QPointF>({QPointF(11.1, -5.3),   QPointF(13.0, -7.0),     QPointF(17.2, -11.9),
                                                             QPointF(21.5, -19.4),  QPointF(22.9, -23.9),    QPointF(23.4, -28.9),
                                                             QPointF(22.1, -35.6),  QPointF(17.8, -42.6),    QPointF(14.5, -45.6),
                                                             QPointF(10.5, -48.1),  QPointF(5.6, -49.7),     QPointF(-0.2, -50.3),
                                                             QPointF(-5.9, -49.7),  QPointF(-10.8, -48.1),   QPointF(-14.9, -45.6),
                                                             QPointF(-18.2, -42.6), QPointF(-22.4, -35.6),   QPointF(-23.8, -28.9),
                                                             QPointF(-23.3, -23.9), QPointF(-21.9, -19.4),   QPointF(-17.6, -11.9),
                                                             QPointF(-13.4, -7.0),  QPointF(-11.4, -5.3),    QPointF(-17.0, -8.4),
                                                             QPointF(-23.2, -10.0), QPointF(-29.6, -9.9),    QPointF(-35.7, -8.3),
                                                             QPointF(-41.2, -5.2),  QPointF(-45.6, -0.6),    QPointF(-48.6, 5.4),
                                                             QPointF(-49.7, 12.7),  QPointF(-48.1, 20.8),    QPointF(-46.2, 24.6),
                                                             QPointF(-43.6, 28.0),  QPointF(-40.4, 30.9),    QPointF(-36.5, 33.2),
                                                             QPointF(-32.1, 34.7),  QPointF(-27.2, 35.2),    QPointF(-21.4, 34.5),
                                                             QPointF(-16.5, 32.4),  QPointF(-12.5, 29.5),    QPointF(-9.2, 26.2),
                                                             QPointF(-4.9, 20.0),   QPointF(-3.6, 17.2),     QPointF(-3.4, 20.6),
                                                             QPointF(-4.0, 28.9),   QPointF(-5.1, 33.9),     QPointF(-7.0, 39.2),
                                                             QPointF(-9.7, 44.2),   QPointF(-13.7, 48.7),    QPointF(13.3, 48.7),
                                                             QPointF(9.4, 44.2),    QPointF(6.6, 39.2),      QPointF(4.7, 33.9),
                                                             QPointF(3.7, 28.9),    QPointF(3.0, 20.6),      QPointF(3.2, 17.2),
                                                             QPointF(4.6, 20.0),    QPointF(8.8, 26.2),      QPointF(12.1, 29.5),
                                                             QPointF(16.2, 32.4),   QPointF(21.1, 34.5),     QPointF(26.8, 35.2),
                                                             QPointF(31.7, 34.7),   QPointF(36.1, 33.2),     QPointF(40.0, 30.9),
                                                             QPointF(43.2, 28.0),   QPointF(45.8, 24.6),     QPointF(47.7, 20.8),
                                                             QPointF(49.3, 12.7),   QPointF(48.2, 5.4),      QPointF(45.3, -0.6),
                                                             QPointF(40.8, -5.2),   QPointF(35.3, -8.3),     QPointF(29.2, -9.9),
                                                             QPointF(22.8, -10.0),  QPointF(16.6, -8.4),     QPointF(11.1, -5.3),
                                                             QPointF(11.1, -5.3)}))},
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
    QBrush overlayBrush();
    void setOverlayBrush(QBrush brush);
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
    void scalePolygon();
    NodePolygon polygon();
    void setPolygon(NodePolygon polygon_id);
    QPolygonF customPolygon();
    void setCustomPolygon(QPolygonF polygon);

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
    NodePolygon stock_polygon_ = NodePolygon::Circle;
    QBrush overlay_brush_;
};

Q_DECLARE_METATYPE(Node *);

#endif // NODE_H
