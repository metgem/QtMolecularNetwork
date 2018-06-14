#ifndef STYLE_H
#define STYLE_H

#include <QWidget>
#include <QString>
#include <QPen>
#include <QColor>
#include <QFont>
#include <QObject>
#include <QBrush>

class NetworkStyle
{
public:
    NetworkStyle(QString name, QBrush node_brush, QColor node_text_color, int node_radius, QPen node_pen, QPen edge_pen, QBrush background_brush)
    {
        this->name = name;
        this->node_brush = node_brush;
        this->node_text_color = node_text_color;
        this->node_radius = node_radius;
        this->node_pen = node_pen;
        this->edge_pen = edge_pen;
        this->background_brush = background_brush;
    }
    NetworkStyle();
    QString styleName() { return name; }
    QBrush nodeBrush() const { return node_brush; }
    QColor nodeTextColor() const { return node_text_color; }
    int nodeRadius() { return node_radius; }
    QPen nodePen() const { return node_pen; }
    QFont nodeFont() { return node_font; }
    QPen edgePen() const { return edge_pen; }
    QBrush backgroundBrush() const { return background_brush; }

protected:
    QString name = "";
    QBrush node_brush;
    QColor node_text_color;
    int node_radius = 0;
    QPen node_pen;
    QFont node_font;
    QPen edge_pen;
    QBrush background_brush;
};

class DefaultStyle: public NetworkStyle
{
public:
    DefaultStyle() {
        name = "default";
        node_brush = QBrush(Qt::lightGray, Qt::SolidPattern);
        node_text_color = QColor(Qt::black);
        node_radius = 30;
        node_pen = QPen(Qt::black, 1);
        node_font = QFont("Arial", 10);
        edge_pen = QPen(Qt::darkGray);
        background_brush = QBrush(Qt::white);
    }
};

class DarkStyle: public NetworkStyle
{
public:
    DarkStyle() {
        name = "dark";
        node_brush = QBrush(Qt::darkGray);
        node_text_color = QColor(Qt::white);
        node_radius = 30;
        node_pen = QPen(Qt::white, 2);
        node_font = QFont("Times New Roman", 12);
        edge_pen = QPen(Qt::lightGray);
        background_brush = QBrush(QColor(Qt::darkGray).darker());
    }
};

#endif // STYLE_H
