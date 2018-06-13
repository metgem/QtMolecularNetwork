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
    QString name() { return name_; }
    QBrush nodeBrush() const { return node_brush; }
    QColor textColor() const { return text_color; }
    int nodeRadius() { return node_radius; }
    QPen nodePen() const { return node_pen; }
    QFont font() { return font_; }
    QPen edgePen() const { return edge_pen; }
    QBrush backgroundBrush() { return background_brush; }

protected:
    QString name_ = "";
    QBrush node_brush;
    QColor text_color;
    int node_radius = 0;
    QPen node_pen;
    QFont font_;
    QPen edge_pen;
    QBrush background_brush;
};

class DefaultStyle: public NetworkStyle
{
public:
    DefaultStyle() {
        name_ = "default";
        node_brush = QBrush(Qt::lightGray, Qt::SolidPattern);
        text_color = QColor(Qt::black);
        node_radius = 30;
        node_pen = QPen(Qt::black, 1);
        font_ = QFont("Arial", 10);
        edge_pen = QPen(Qt::darkGray);
        background_brush = QBrush(Qt::white);
    }
};

class DarkStyle: public NetworkStyle
{
public:
    DarkStyle() {
        name_ = "dark";

        node_brush = QBrush(Qt::darkGray);
        node_radius = 30;
        text_color = QColor(Qt::white);
        node_pen = QPen(Qt::white, 2);
        font_ = QFont("Times New Roman", 12);
        edge_pen = QPen(Qt::lightGray);
        background_brush = QBrush(QColor(Qt::darkGray).darker());
    }
};

#endif // STYLE_H
