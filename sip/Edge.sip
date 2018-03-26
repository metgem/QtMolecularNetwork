%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class Edge : public QGraphicsPathItem {

%TypeHeaderCode
#include "edge.h"
%End

public:
    Edge(int index, Node *sourceNode, Node *destNode, qreal weight /TransferThis/ = 1, qreal width /TransferThis/ = 1);
    Node *sourceNode() const;
    Node *destNode() const;
    void setColor(const QColor color);
    void setWidth(qreal width);
    void setSourceNode(Node *node);
    void setDestNode(Node *node);
    void adjust();
};

%End