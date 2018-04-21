#ifndef NETWORKSCENE_H
#define NETWORKSCENE_H

#include "graphicsitem.h"

#include <QGraphicsScene>
#include <QWidget>
#include <QAbstractTableModel>

class Node;
class Edge;

class Q_DECL_EXPORT NetworkScene : public QGraphicsScene
{
    Q_OBJECT

signals:
   void scaleChanged(qreal);
   void layoutChanged();

public:
    NetworkScene(QWidget *parent = 0);

    void clear();

    QList<Node *> addNodes(QList<int> indexes, QList<QString> labels=QList<QString>(), QList<QPointF> positions = QList<QPointF>());
    QList<Edge *> addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> weights, QList<qreal> widths);

    QList<Node *> nodes() const;
    QList<Node *> selectedNodes() const;
    void setNodesSelection(QList<int> indexes);
    void setNodesSelection(QList<Node *> nodes);
    QRectF selectedNodesBoundingRect();

    QList<Edge *> edges() const;
    QList<Edge *> selectedEdges() const;
    void setEdgesSelection(QList<int> indexes);
    void setEdgesSelection(QList<Edge *> edges);

    void setLayout(QList<qreal> layout, qreal scale=0);
    void setLayout(QList<QPointF> layout, qreal scale=0);
    qreal scale();
    void setScale(qreal scale=1);
    void setLabelsFromModel(QAbstractTableModel* model, int column_id, int role=Qt::DisplayRole);
    void resetLabels();
    QList<QColor> pieColors();
    void setPieColors(QList<QColor> colors);
    void setPieChartsFromModel(QAbstractTableModel* model, QList<int> column_ids, int role=Qt::DisplayRole);
    void resetPieCharts();

    void hideItems(QList<QGraphicsItem *> items);
    void showItems(QList<QGraphicsItem *> items);
    void hideSelectedItems();
    void showAllItems();

    Node *nodeAt(const QPointF &position, const QTransform &deviceTransform) const;
    Node *nodeAt(qreal x, qreal y, const QTransform &deviceTransform) const;
    Edge *edgeAt(const QPointF &position, const QTransform &deviceTransform) const;
    Edge *edgeAt(qreal x, qreal y, const QTransform &deviceTransform) const;

private:
    GraphicsItemLayer *nodesLayer;
    GraphicsItemLayer *edgesLayer;
    qreal scale_;
    QList <QColor> colors_;
};

#endif // NETWORKSCENE_H
