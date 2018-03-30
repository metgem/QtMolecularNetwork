%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class Node : public QGraphicsEllipseItem {

%TypeHeaderCode
#include "node.h"
%End

public:
    Node(int index, QString label);

    int index();
    void setColor(const QColor color);
    void setLabel(QString label);
    void addEdge(Edge *edge);
    QList<Edge *> edges() const;
};

%End