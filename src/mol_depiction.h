#ifndef MOL_DEPICTION_H
#define MOL_DEPICTION_H

#include <QPixmap>
#include <QSize>

QPixmap SvgToPixmap(const QByteArray &svg_data, const QSize &size);
QPixmap SmilesToPixmap(const QString &smiles, const QSize &size);
QPixmap InchiToPixmap(const QString &inchi, const QSize &size);

#endif // MOL_DEPICTION_H
