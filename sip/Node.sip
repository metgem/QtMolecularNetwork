%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class Node : public QGraphicsEllipseItem {

%TypeHeaderCode
#include "node.h"
%End

public:
    Node(int index, int radius, QString label=NULL);

    int index();
    int radius();
    void setRadius(int radius);
    QFont font();
    void setFont(QFont font);
    const QColor textColor();
    void setTextColor(const QColor color);
    void setBrush(const QBrush brush);
    QString label();
    void setLabel(QString label);
    void setPie(QList<qreal> values);
    void addEdge(Edge *edge);
    QList<Edge *> edges() const;
    void updateStyle(NetworkStyle *style, NetworkStyle* old=NULL);
};

%End