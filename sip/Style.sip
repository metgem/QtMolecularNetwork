%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class NetworkStyle {

%TypeHeaderCode
#include "style.h"
%End

public:
    NetworkStyle(QString name, QVariantMap node,
                 QVariantMap edge, QMap<QString, QBrush> scene);
    NetworkStyle();
    QString styleName();
    void setStyleName(QString name);
    QBrush nodeBrush(const bool selected = false) const;
    void setNodeBrush(const QBrush brush, const bool selected = false);
    QColor nodeTextColor(const bool selected = false) const;
    void setNodeTextColor(const QColor color, const bool selected = false);
    QPen nodePen(const bool selected = false) const;
    void setNodePen(const QPen pen, const bool selected = false);
    QFont nodeFont(const bool selected = false);
    void setNodeFont(const QFont font, const bool selected = false);
    QPen edgePen(const bool selected = false) const;
    void setEdgePen(const QPen pen, const bool selected = false);
    QBrush backgroundBrush() const;
    void setBackgroundBrush(const QBrush brush);
};

class DefaultStyle : public NetworkStyle {

%TypeHeaderCode
#include "style.h"
%End

public:
    QString styleName();
    QBrush nodeBrush(const bool selected=false) const;
    QColor nodeTextColor(const bool selected=false) const;
    QPen nodePen(const bool selected=false) const;
    QFont nodeFont(const bool selected=false);
    QPen edgePen(const bool selected=false) const;
    QBrush backgroundBrush() const;
};

%End
