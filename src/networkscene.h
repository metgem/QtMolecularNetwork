#ifndef NETWORKSCENE_H
#define NETWORKSCENE_H

#include <QGraphicsScene>
#include <QGraphicsItem>
#include <QWidget>
#include <QAbstractTableModel>

#include "graphicsitem.h"
#include "style.h"

class Node;
class Edge;

class Q_DECL_EXPORT NetworkScene : public QGraphicsScene
{
    Q_OBJECT

signals:
   void scaleChanged(qreal);
   void layoutChanged();
   void pieChartsVisibilityChanged(bool);
   void locked(bool);

public:
    NetworkScene(QWidget *parent=nullptr);

    NetworkStyle *networkStyle();
    void setNetworkStyle(NetworkStyle *style=nullptr);

    void clear();
    void render(QPainter *painter, const QRectF &target = QRectF(), const QRectF &source = QRectF(), Qt::AspectRatioMode aspectRatioMode = Qt::KeepAspectRatio);

    void addNode(Node *node);
    void addEdge(Edge *edge);
    QList<Node *> addNodes(QList<int> indexes,
                           QList<QString> labels = QList<QString>(),
                           QList<QPointF> positions = QList<QPointF>(),
                           QList<QVariant> colors = QList<QVariant>(),
                           QList<QVariant> radii = QList<QVariant>());
    QList<Edge *> addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> widths);
    void removeAllNodes();
    void removeNodes(QList<Node *> nodes);
    void removeAllEdges();
    void removeEdges(QList<Edge *> edges);

    QList<Node *> nodes() const;
    QList<Node *> selectedNodes() const;
    void setNodesSelection(QList<int> indexes);
    void setNodesSelection(QList<Node *> nodes);
    QRectF selectedNodesBoundingRect();

    QList<Edge *> edges() const;
    QList<Edge *> selectedEdges() const;
    void setEdgesSelection(QList<int> indexes);
    void setEdgesSelection(QList<Edge *> edges);

    QList<QPointF> layout();
    void setLayout(QList<qreal> layout, qreal scale=0, QList<int> isolated_nodes=QList<int>());
    void setLayout(QList<QPointF> layout, qreal scale=0, QList<int> isolated_nodes=QList<int>());
    qreal scale();
    void setScale(qreal scale=1);
    void setLabelsFromModel(QAbstractItemModel *model, int column_id, int role=Qt::DisplayRole);
    void resetLabels();
    QList<QColor> pieColors();
    void setNodesRadiiFromModel(QAbstractItemModel *model, int column_id, int role=Qt::DisplayRole, const std::function<int (qreal)> &func=nullptr);
    void resetNodesRadii();
    void setPieColors(QList<QColor> colors);
    void setPieChartsFromModel(QAbstractItemModel *model, QList<int> column_ids, int role=Qt::DisplayRole);
    void resetPieCharts();
    bool pieChartsVisibility();
    void setPieChartsVisibility(bool visibility=true);

    void hideItems(QList<QGraphicsItem *> items);
    void showItems(QList<QGraphicsItem *> items);
    void hideSelectedItems();
    void showAllItems();
    void hideAllItems();

    QList<QColor> nodesColors();
    void setNodesColors(QList<QVariant> colors);
    void setSelectedNodesColor(QColor color);

    QList<int> nodesRadii();
    void setNodesRadii(QList<int> radii);
    void setSelectedNodesRadius(int radius);

    Node *nodeAt(const QPointF &position, const QTransform &deviceTransform) const;
    Node *nodeAt(qreal x, qreal y, const QTransform &deviceTransform) const;
    Edge *edgeAt(const QPointF &position, const QTransform &deviceTransform) const;
    Edge *edgeAt(qreal x, qreal y, const QTransform &deviceTransform) const;

    void lock(bool lock=true);
    void unlock();

    QRectF itemsBoundingRect() const;

private:
    NetworkStyle *style_;
    qreal scale_;
    QList <QColor> colors_;
    bool pie_charts_visibility;
};

#endif // NETWORKSCENE_H
