%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class Node : public QGraphicsEllipseItem {

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
    void addEdge(Edge *edge);
    void removeEdge(Edge *edge);
    QSet<Edge *> edges() const;
    void updateStyle(NetworkStyle *style, NetworkStyle* old=nullptr);
};

%End