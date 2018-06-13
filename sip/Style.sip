%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class NetworkStyle {

%TypeHeaderCode
#include "style.h"
%End

public:
    QString name();
    QBrush nodeBrush() const;
    QColor textColor() const;
    int nodeRadius();
    QPen nodePen() const;
    QFont font();
    QPen edgePen() const;
    QBrush backgroundBrush();
};

class DefaultStyle : public NetworkStyle {

%TypeHeaderCode
#include "style.h"
%End

public:
    QString name();
    QBrush nodeBrush() const;
    QColor textColor() const;
    int nodeRadius();
    QPen nodePen() const;
    QFont font();
    QPen edgePen() const;
    QBrush backgroundBrush();
};

class DarkStyle : public NetworkStyle {

%TypeHeaderCode
#include "style.h"
%End

public:
    QString name();
    QBrush nodeBrush() const;
    QColor textColor() const;
    int nodeRadius();
    QPen nodePen() const;
    QFont font();
    QPen edgePen() const;
    QBrush backgroundBrush();
};

%End