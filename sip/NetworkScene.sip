%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class NetworkScene : public QGraphicsScene {

%TypeHeaderCode
#include "networkscene.h"
#include "graphicsitem.h"
%End

public:
    NetworkScene(QWidget *parent /TransferThis/ = 0);
    
    void clear();
    
    QList<Node *>  addNodes(QList<int> indexes, QList<QString> labels, QList<QPointF> positions = QList<QPointF>());
    QList<Edge *>  addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> weights, QList<qreal> widths);
    
    QList<Node *> nodes() const;
    QList<Edge *> edges() const;  
    
    void setLayout(QList<qreal> layout);
    void setLayout(QList<QPointF> layout);
};

%End