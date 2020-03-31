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
    void setStyleName(QString name);
    QBrush nodeBrush(const bool selected = false) const;
    void setNodeBrush(const QBrush brush, const bool selected = false);
    QColor nodeTextColor(const bool selected = false) const;
    void setNodeTextColor(const QColor color, const bool selected = false);
    QPen nodePen(const bool selected = false) const;
    void setNodePen(const QPen pen, const bool selected = false);
    QFont nodeFont(const bool selected = false);
    void setNodeFont(const QFont font, const bool selected = false);
    QPen edgePen(const bool selected = false) const;
    void setEdgePen(const QPen pen, const bool selected = false);
    QBrush backgroundBrush() const;
    void setBackgroundBrush(const QBrush brush);

protected:
    QString name = "";
    QBrush nb; // Node Brush
    QBrush nbs; // Node Brush Selected
    QColor ntc; // Node Text Color
    QColor ntcs; // Node Text Color Selected
    QPen np; // Node Pen
    QPen nps; // Node Pen Selected
    QFont nf; // Node Font
    QFont nfs; // Node Font Selected

    QPen ep; // Edge Pen
    QPen eps; // Edge Pen Selected

    QBrush sb; // Scene Brush
};

class Q_DECL_EXPORT DefaultStyle: public NetworkStyle
{
public:
    DefaultStyle() {
        name = "default";

        nb = QBrush(Qt::lightGray);
        nbs = QBrush(Qt::yellow);

        ntc = QColor(Qt::black);
        ntcs = QColor(Qt::black);

        np = QPen(Qt::black, 1, Qt::SolidLine);
        nps = QPen(Qt::black, 1, Qt::SolidLine);

        nf = QFont();
        nfs = QFont();

        ep = QPen(QColor(Qt::darkGray));
        eps = QPen(QColor(Qt::red));

        sb = QBrush(Qt::white);
    }
};

#endif // STYLE_H
