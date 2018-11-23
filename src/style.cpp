#include "style.h"

NetworkStyle::NetworkStyle(QString name, QVariantMap node, QVariantMap edge, QMap<QString, QBrush> scene)
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

QBrush NetworkStyle::nodeBrush(const QString &state) const
{
    if (this->node.contains("bgcolor"))
    {
        QVariant var = this->node.value("bgcolor");
        QVariantMap map = var.toMap();
        if (map.contains(state))
            return map.value(state).value<QBrush>();
    }

    if (state == "selected")
        return QBrush(QColor());
    else
        return QBrush(QColor(Qt::lightGray));
}

QColor NetworkStyle::nodeTextColor(const QString &state) const
{
    if (this->node.contains("txtcolor"))
    {
        QVariant var = this->node.value("txtcolor");
        QVariantMap map = var.toMap();
        if (map.contains(state))
            return map.value(state).value<QColor>();
    }

    if (state == "selected")
        return QColor();
    else
        return QColor(Qt::black);
}

QPen NetworkStyle::nodePen(const QString &state) const
{
    if (this->node.contains("border"))
    {
        QVariant var = this->node.value("border");
        QVariantMap map = var.toMap();
        if (map.contains(state))
            return map.value(state).value<QPen>();
    }

    return QPen(Qt::black, 1);
}

QFont NetworkStyle::nodeFont(const QString &state)
{
    if (this->node.contains("font"))
    {
        QVariant var = this->node.value("font");
        QVariantMap map = var.toMap();
        if (map.contains(state))
            return map.value(state).value<QFont>();
    }

    return QFont();
}

QPen NetworkStyle::edgePen(const QString &state) const
{
    if (this->edge.contains("color"))
    {
        QVariant var = this->edge.value("color");
        QVariantMap map = var.toMap();
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
