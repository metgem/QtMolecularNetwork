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
    QBrush nodeBrush(const QString &state = "normal") const;
    QColor nodeTextColor(const QString &state = "normal") const;
    QPen nodePen(const QString &state = "normal") const;
    QFont nodeFont(const QString &state = "normal");
    QPen edgePen(const QString &state = "normal") const;
    QBrush backgroundBrush() const;
};

class DefaultStyle : public NetworkStyle {

%TypeHeaderCode
#include "style.h"
%End

public:
    QString styleName();
    QBrush nodeBrush(const QString &state = "normal") const;
    QColor nodeTextColor(const QString &state = "normal") const;
    QPen nodePen(const QString &state = "normal") const;
    QFont nodeFont(const QString &state = "normal");
    QPen edgePen(const QString &state = "normal") const;
    QBrush backgroundBrush() const;
};

%End