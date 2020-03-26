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
    QBrush nodeBrush(const QString &state = "normal") const;
    void setNodeBrush(const QBrush brush, const QString &state = "normal");
    QColor nodeTextColor(const QString &state = "normal") const;
    void setNodeTextColor(const QColor color, const QString &state = "normal");
    QPen nodePen(const QString &state = "normal") const;
    void setNodePen(const QPen pen, const QString &state = "normal");
    QFont nodeFont(const QString &state = "normal");
    void setNodeFont(const QFont font, const QString &state = "normal");
    QPen edgePen(const QString &state = "normal") const;
    void setEdgePen(const QPen pen, const QString &state = "normal");
    QBrush backgroundBrush() const;
    void setBackgroundBrush(const QBrush brush);
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
