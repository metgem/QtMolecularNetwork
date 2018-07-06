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
    QBrush nodeBrush(QString state = "normal") const;
    QColor nodeTextColor(QString state = "normal") const;
    QPen nodePen(QString state = "normal") const;
    QFont nodeFont(QString state = "normal");
    QPen edgePen(QString state = "normal") const;
    QBrush backgroundBrush() const;
};

class DefaultStyle : public NetworkStyle {

%TypeHeaderCode
#include "style.h"
%End

public:
    QString styleName();
    QBrush nodeBrush(QString state = "normal") const;
    QColor nodeTextColor(QString state = "normal") const;
    QPen nodePen(QString state = "normal") const;
    QFont nodeFont(QString state = "normal");
    QPen edgePen(QString state = "normal") const;
    QBrush backgroundBrush() const;
};

%End