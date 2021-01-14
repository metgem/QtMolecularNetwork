#include "mol_depiction.h"

#include <QByteArray>
#include <QtSvg/QSvgRenderer>
#include <QPixmap>
#include <QPainter>

#include <GraphMol/SmilesParse/SmilesParse.h>
#include <GraphMol/Depictor/RDDepictor.h>
#include <GraphMol/MolDraw2D/MolDraw2DSVG.h>
#include <GraphMol/inchi.h>

QPixmap SvgToPixmap(const QByteArray &svg_data, const QSize &size)
{
    if (size.isNull())
            return QPixmap();

     QSvgRenderer svgRenderer(svg_data);
     QPixmap pixmap(size);
     QPainter painter;

     pixmap.fill(Qt::transparent);
     painter.begin(&pixmap);
     svgRenderer.render(&painter);
     painter.end();

     return pixmap;
}

QPixmap MolToPixmap(RDKit::ROMol &mol, const QSize &size)
{
    if (size.isNull())
        return QPixmap();

    if (!mol.getNumConformers())
        RDDepict::compute2DCoords( mol, nullptr, true );
    RDKit::MolDraw2DSVG svg_drawer(size.width(), size.height());
    svg_drawer.drawOptions().clearBackground = false;
    svg_drawer.drawMolecule( mol );
    svg_drawer.finishDrawing();
    std::string drawing_text = svg_drawer.getDrawingText();
    QByteArray svg_data(drawing_text.c_str(), drawing_text.length());
    return SvgToPixmap(svg_data, size);
}

QPixmap SmilesToPixmap(const QString &smiles, const QSize &size)
{
    if (size.isNull())
        return QPixmap();

    try
    {
        std::shared_ptr<RDKit::ROMol> mol(RDKit::SmilesToMol( smiles.toStdString() ) );
        if (mol != nullptr)
            return MolToPixmap( *mol, size);
    } catch( ... ) {
    }

    return QPixmap();
}

QPixmap InchiToPixmap(const QString &inchi, const QSize &size)
{
    if (size.isNull())
        return QPixmap();

    try
    {
        RDKit::ExtraInchiReturnValues rv;
        std::shared_ptr<RDKit::ROMol> mol(RDKit::InchiToMol( inchi.toStdString(), rv ) );
        if (mol != nullptr)
            return MolToPixmap( *mol, size);
    } catch( ... ) {
    }
    return QPixmap();
}
