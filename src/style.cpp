#include "style.h"

NetworkStyle::NetworkStyle(QString name, QVariantMap node, QVariantMap edge, QMap<QString, QBrush> scene)
{
    this->name = name;

    nb = QBrush(QColor(Qt::lightGray));
    nbs = QBrush(QColor());
    if (node.contains("bgcolor"))
    {
        QVariant var = node.value("bgcolor");
        QVariantMap map = var.toMap();
        if (map.contains("normal"))
            nb = map.value("normal").value<QBrush>();
        if (map.contains("selected"))
            nbs = map.value("selected").value<QBrush>();
    }

    ntc = QColor(Qt::black);
    ntcs = QColor();
    if (node.contains("txtcolor"))
    {
        QVariant var = node.value("txtcolor");
        QVariantMap map = var.toMap();
        if (map.contains("normal"))
            ntc = map.value("normal").value<QColor>();
        if (map.contains("selected"))
            ntcs = map.value("selected").value<QColor>();
    }

    np = nps = QPen(Qt::black, 1);
    if (node.contains("border"))
    {
        QVariant var = node.value("border");
        QVariantMap map = var.toMap();
        if (map.contains("normal"))
            np = map.value("normal").value<QPen>();
        if (map.contains("selected"))
            nps = map.value("selected").value<QPen>();
    }

    nf = nfs = QFont();
    if (node.contains("font"))
    {
        QVariant var = node.value("font");
        QVariantMap map = var.toMap();
        if (map.contains("normal"))
            nf = map.value("normal").value<QFont>();
        if (map.contains("selected"))
            nfs = map.value("selected").value<QFont>();
    }

    ep = QPen(Qt::darkGray);
    eps = QPen(Qt::red);
    if (edge.contains("color"))
    {
        QVariant var = edge.value("color");
        QVariantMap map = var.toMap();
        if (map.contains("normal"))
            ep = map.value("normal").value<QPen>();
        if (map.contains("selected"))
            eps = map.value("selected").value<QPen>();
    }


    sb = QBrush(QColor(Qt::white));
    if (scene.contains("color"))
    {
        QVariant var = scene.value("color");
        sb = var.value<QBrush>();
    }
}

QString NetworkStyle::styleName()
{
    return this->name;
}

void NetworkStyle::setStyleName(QString name)
{
    this->name = name;
}

QBrush NetworkStyle::nodeBrush(const bool selected) const
{
    if (selected)
        return nbs;
    else
        return nb;
}

void NetworkStyle::setNodeBrush(const QBrush brush, const bool selected)
{
    if (selected)
        this->nbs = brush;
    else
        this->nb = brush;
}

QColor NetworkStyle::nodeTextColor(const bool selected) const
{
    if (selected)
        return ntcs;
    else
        return ntc;
}

void NetworkStyle::setNodeTextColor(const QColor color, const bool selected)
{
    if (selected)
        this->nbs = color;
    else
        this->nb = color;
}

QPen NetworkStyle::nodePen(const bool selected) const
{
    if (selected)
        return nps;
    else
        return np;
}

void NetworkStyle::setNodePen(const QPen pen, const bool selected)
{
    if (selected)
        this->nps = pen;
    else
        this->np = pen;
}

QFont NetworkStyle::nodeFont(const bool selected)
{
    if (selected)
        return nfs;
    else
        return nf;
}

void NetworkStyle::setNodeFont(const QFont font, const bool selected)
{
    if (selected)
        this->nfs = font;
    else
        this->nf = font;
}

QPen NetworkStyle::edgePen(const bool selected) const
{
    if (selected)
        return eps;
    else
        return ep;
}

void NetworkStyle::setEdgePen(const QPen pen, const bool selected)
{
    if (selected)
        this->eps = pen;
    else
        this->ep = pen;
}

QBrush NetworkStyle::backgroundBrush() const {
    return sb;
}

void NetworkStyle::setBackgroundBrush(const QBrush brush)
{
    this->sb = brush;
}
