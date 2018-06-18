#ifndef STYLE_H
#define STYLE_H

#include <QWidget>
#include <QString>
#include <QPen>
#include <QColor>
#include <QFont>
#include <QObject>
#include <QBrush>

#include <QMap>
#include <QVariant>

class NetworkStyle
{
public:
    NetworkStyle(QString name, QMap<QString, QVariant> node, QMap<QString, QVariant> edge, QMap<QString, QBrush> scene);
    NetworkStyle() {}
    QString styleName();
    QBrush nodeBrush(QString state = "normal") const;
    QColor nodeTextColor(QString state = "normal") const;
    int nodeRadius();
    QPen nodePen(QString state = "normal") const;
    QFont nodeFont(QString state = "normal");
    QPen edgePen(QString state = "normal") const;
    QBrush backgroundBrush() const;

protected:
    QString name = "";
    QMap<QString, QVariant> node;
    QMap<QString, QVariant> edge;
    QMap<QString, QBrush> scene;
};

class DefaultStyle: public NetworkStyle
{
public:
    DefaultStyle() {
        name = "default";

        node["radius"] = 30;

        QMap<QString, QVariant> bgcolor;
        bgcolor["normal"]= QBrush(Qt::lightGray);
        bgcolor["selected"]= QBrush(Qt::yellow);
        node["bgcolor"] = bgcolor;

        QMap<QString, QVariant> txtcolor;
        txtcolor["normal"]= QColor(Qt::black);
        txtcolor["selected"]= QColor(Qt::black);
        node["txtcolor"] = txtcolor;

        QMap<QString, QVariant> border;
        border["normal"]= QPen(Qt::black, 1, Qt::SolidLine);
        border["selected"]= QPen(Qt::black, 1, Qt::SolidLine);
        node["border"] = border;

        QMap<QString, QVariant> font;
        font["normal"]= QPen(Qt::black, 1, Qt::SolidLine);
        font["selected"]= QPen(Qt::black, 1, Qt::SolidLine);
        node["font"] = font;

        QMap<QString, QVariant> epen;
        epen["normal"] = QPen(QColor(Qt::darkGray));
        epen["selected"] = QPen(QColor(Qt::red));
        edge["color"] = epen;

        scene["color"] = QBrush(Qt::white);
    }
};

#endif // STYLE_H
