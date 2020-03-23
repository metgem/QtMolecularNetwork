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
    QBrush nodeBrush(const bool selected=false) const;
    QColor nodeTextColor(const bool selected=false) const;
    QPen nodePen(const bool selected=false) const;
    QFont nodeFont(const bool selected=false);
    QPen edgePen(const bool selected=false) const;
    QBrush backgroundBrush() const;
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