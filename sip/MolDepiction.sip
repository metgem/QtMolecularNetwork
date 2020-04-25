%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

%ModuleHeaderCode
#include "mol_depiction.h"
%End

QPixmap SvgToPixmap(const QByteArray &svg_data, const QSize &size = QSize(300, 300));
QPixmap SmilesToPixmap(const QString &smiles, const QSize &size = QSize(300, 300)
QPixmap InchiToPixmap(const QString &inchi, const QSize &size = QSize(300, 300)

%End
