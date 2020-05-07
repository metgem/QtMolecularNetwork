%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class Edge : QGraphicsPathItem
{

%TypeHeaderCode
#include "edge.h"
%End

public:
    Edge(int index, Node *sourceNode, Node *destNode, qreal width = 1.);
    
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
    
    QVariant itemChange(QGraphicsItem::GraphicsItemChange change, const QVariant &value);
    int type() const;
    QRectF boundingRect() const;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget);
};

%End
