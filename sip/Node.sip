%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class Node : public QGraphicsEllipseItem {

%TypeHeaderCode
#include "node.h"
%End

public:
    Node(int index, QString label=0);

    int index();
    const QColor color();
    void setColor(const QColor color);
    QString label();
    void setLabel(QString label);
    void addEdge(Edge *edge);
    QList<Edge *> edges() const;
};

%End