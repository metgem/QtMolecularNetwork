%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

%ModuleHeaderCode
#include "node.h"
%End

enum NodePolygon {
    Circle,
    Square,
    Diamond,
    ThinDiamond,
    TriangleDown,
    TriangleUp,
    TriangleLeft,
    TriangleRight,
    Pentagon,
    Octagon,
    Hexagon,
    Star,
    Plus,
    X,
    Mask
};

class Node : QGraphicsEllipseItem
{

%TypeHeaderCode
#include "node.h"
%End

public:
    Node(int index, const QString &label = QString());

    int index();
    int radius();
    void setRadius(int radius);
    QFont font();
    void setFont(const QFont &font);
    const QColor textColor();
    void setTextColor(const QColor &color);
    void setBrush(const QBrush &brush);
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
    void updateStyle(NetworkStyle *style, NetworkStyle* old = nullptr);
    
    int type() const;

    virtual QVariant itemChange(GraphicsItemChange change, const QVariant &value);
    QPainterPath shape() const;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget);

};

%End
