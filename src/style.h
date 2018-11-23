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


class Q_DECL_EXPORT NetworkStyle
{
public:
    NetworkStyle(QString name, QVariantMap node, QVariantMap edge, QMap<QString, QBrush> scene);
    NetworkStyle() {}
    QString styleName();
    QBrush nodeBrush(const QString &state = "normal") const;
    QColor nodeTextColor(const QString &state = "normal") const;
    QPen nodePen(const QString &state = "normal") const;
    QFont nodeFont(const QString &state = "normal");
    QPen edgePen(const QString &state = "normal") const;
    QBrush backgroundBrush() const;

protected:
    QString name = "";
    QVariantMap node;
    QVariantMap edge;
    QMap<QString, QBrush> scene;
};

class Q_DECL_EXPORT DefaultStyle: public NetworkStyle
{
public:
    DefaultStyle() {
        name = "default";

        QVariantMap bgcolor;
        bgcolor["normal"]= QBrush(Qt::lightGray);
        bgcolor["selected"]= QBrush(Qt::yellow);
        node["bgcolor"] = bgcolor;

        QVariantMap txtcolor;
        txtcolor["normal"]= QColor(Qt::black);
        txtcolor["selected"]= QColor(Qt::black);
        node["txtcolor"] = txtcolor;

        QVariantMap border;
        border["normal"]= QPen(Qt::black, 1, Qt::SolidLine);
        border["selected"]= QPen(Qt::black, 1, Qt::SolidLine);
        node["border"] = border;

        QVariantMap font;
        font["normal"]= QPen(Qt::black, 1, Qt::SolidLine);
        font["selected"]= QPen(Qt::black, 1, Qt::SolidLine);
        node["font"] = font;

        QVariantMap epen;
        epen["normal"] = QPen(QColor(Qt::darkGray));
        epen["selected"] = QPen(QColor(Qt::red));
        edge["color"] = epen;

        scene["color"] = QBrush(Qt::white);
    }
};

#endif // STYLE_H
