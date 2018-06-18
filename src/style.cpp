#include "style.h"

NetworkStyle::NetworkStyle(QString name, QMap<QString, QVariant> node, QMap<QString, QVariant> edge, QMap<QString, QBrush> scene)
{
    this->name = name;
    this->node = node;
    this->edge = edge;
    this->scene = scene;
}

QString NetworkStyle::styleName()
{
    return this->name;
}

QBrush NetworkStyle::nodeBrush(QString state) const
{
    if (this->node.contains("bgcolor"))
    {
        QVariant var = this->node.value("bgcolor");
        QMap<QString, QVariant> map = var.toMap();
        if (map.contains(state))
            return map.value(state).value<QBrush>();
    }

    if (state == "selected")
        return QBrush(QColor());
    else
        return QBrush(QColor(Qt::lightGray));
}

QColor NetworkStyle::nodeTextColor(QString state) const
{
    if (this->node.contains("txtcolor"))
    {
        QVariant var = this->node.value("txtcolor");
        QMap<QString, QVariant> map = var.toMap();
        if (map.contains(state))
            return map.value(state).value<QColor>();
    }

    if (state == "selected")
        return QColor();
    else
        return QColor(Qt::black);
}

int NetworkStyle::nodeRadius()
{
    if (this->node.contains("radius"))
    {
        QVariant var = this->node.value("radius");
        return var.toInt();
    }

    return 30;
}

QPen NetworkStyle::nodePen(QString state) const
{
    if (this->node.contains("border"))
    {
        QVariant var = this->node.value("border");
        QMap<QString, QVariant> map = var.toMap();
        if (map.contains(state))
            return map.value(state).value<QPen>();
    }

    return QPen(Qt::black, 1);
}

QFont NetworkStyle::nodeFont(QString state)
{
    if (this->node.contains("font"))
    {
        QVariant var = this->node.value("font");
        QMap<QString, QVariant> map = var.toMap();
        if (map.contains(state))
            return map.value(state).value<QFont>();
    }

    return QFont();
}

QPen NetworkStyle::edgePen(QString state) const
{
    if (this->edge.contains("color"))
    {
        QVariant var = this->edge.value("color");
        QMap<QString, QVariant> map = var.toMap();
        if (map.contains(state))
            return map.value(state).value<QPen>();
    }

    if (state == "selected")
        return QPen(Qt::red);
    else
        return QPen(Qt::darkGray);
}

QBrush NetworkStyle::backgroundBrush() const {
    if (this->scene.contains("color"))
    {
        QVariant var = this->scene.value("color");
        return var.value<QBrush>();
    }

    return QBrush(QColor(Qt::white));
}
