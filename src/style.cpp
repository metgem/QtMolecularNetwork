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

void NetworkStyle::setStyleName(QString name)
{
    this->name = name;
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

void NetworkStyle::setNodeBrush(const QBrush brush, const QString &state)
{
    if (this->node.contains("bgcolor"))
    {
        QVariant var = this->node.value("bgcolor");
        QVariantMap map = var.toMap();
        map[state] = brush;
        this->node["bgcolor"] = map;
    }
    else
    {
        QVariantMap map;
        map[state] = brush;
        this->node["bgcolor"] = map;
    }
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

void NetworkStyle::setNodeTextColor(const QColor color, const QString &state)
{
    if (this->node.contains("txtcolor"))
    {
        QVariant var = this->node.value("txtcolor");
        QVariantMap map = var.toMap();
        map[state] = color;
        this->node["txtcolor"] = map;
    }
    else
    {
        QVariantMap map;
        map[state] = color;
        this->node["txtcolor"] = map;
    }
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

void NetworkStyle::setNodePen(const QPen pen, const QString &state)
{
    if (this->node.contains("border"))
    {
        QVariant var = this->node.value("border");
        QVariantMap map = var.toMap();
        map[state] = pen;
        this->node["border"] = map;
    }
    else
    {
        QVariantMap map;
        map[state] = pen;
        this->node["border"] = map;
    }
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

void NetworkStyle::setNodeFont(const QFont font, const QString &state)
{
    if (this->node.contains("font"))
    {
        QVariant var = this->node.value("font");
        QVariantMap map = var.toMap();
        map[state] = font;
        this->node["font"] = map;
    }
    else
    {
        QVariantMap map;
        map[state] = font;
        this->node["font"] = map;
    }
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

void NetworkStyle::setEdgePen(const QPen pen, const QString &state)
{
    if (this->edge.contains("color"))
    {
        QVariant var = this->node.value("color");
        QVariantMap map = var.toMap();
        map[state] = pen;
        this->edge["color"] = map;
    }
    else
    {
        QVariantMap map;
        map[state] = pen;
        this->edge["color"] = map;
    }
}

QBrush NetworkStyle::backgroundBrush() const {
    if (this->scene.contains("color"))
    {
        QVariant var = this->scene.value("color");
        return var.value<QBrush>();
    }

    return QBrush(QColor(Qt::white));
}

void NetworkStyle::setBackgroundBrush(const QBrush brush)
{
    this->scene["color"] = brush;
}
