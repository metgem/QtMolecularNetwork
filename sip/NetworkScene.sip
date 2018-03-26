%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class NetworkScene : public QGraphicsScene {

%TypeHeaderCode
#include "networkscene.h"
%End

public:
    NetworkScene(QWidget *parent /TransferThis/ = 0);
    void addNodes(QList<int> indexes, QList<QString> labels, QList<QPointF> positions);
    void addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> weights, QList<qreal> widths);
};

%End