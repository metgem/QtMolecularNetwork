%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class NetworkStyle {

%TypeHeaderCode
#include "style.h"
%End

public:
    NetworkStyle(QString name, QBrush node_brush, QColor node_text_color, int node_radius, QPen node_pen, QPen edge_pen, QBrush background_brush);
    NetworkStyle();
    QString styleName();
    QBrush nodeBrush() const;
    QColor nodeTextColor() const;
    int nodeRadius();
    QPen nodePen() const;
    QFont nodeFont();
    QPen edgePen() const;
    QBrush backgroundBrush() const;
};

class DefaultStyle : public NetworkStyle {

%TypeHeaderCode
#include "style.h"
%End

public:
    QString styleName();
    QBrush nodeBrush() const;
    QColor nodeTextColor() const;
    int nodeRadius();
    QPen nodePen() const;
    QFont nodeFont();
    QPen edgePen() const;
    QBrush backgroundBrush() const;
};

class DarkStyle : public NetworkStyle {

%TypeHeaderCode
#include "style.h"
%End

public:
    QString styleName();
    QBrush nodeBrush() const;
    QColor nodeTextColor() const;
    int nodeRadius();
    QPen nodePen() const;
    QFont nodeFont();
    QPen edgePen() const;
    QBrush backgroundBrush() const;
};

%End