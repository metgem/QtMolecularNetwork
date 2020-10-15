#ifndef NETWORKSCENE_H
#define NETWORKSCENE_H

#include <QGraphicsScene>
#include <QGraphicsItem>
#include <QWidget>
#include <QAbstractTableModel>

#include "style.h"
#include "graphicsitem.h"

class Node;
class Edge;

class Q_DECL_EXPORT NetworkScene : public QGraphicsScene
{
    Q_OBJECT

signals:
   void scaleChanged(qreal);
   void layoutChanged();
   void pieChartsVisibilityChanged(bool);
   void pixmapVisibilityChanged(bool);
   void locked(bool);

public:
    NetworkScene(QWidget *parent=nullptr);

    NetworkStyle *networkStyle();
    void setNetworkStyle(NetworkStyle *style=nullptr);

    void clear();
    void render(QPainter *painter, const QRectF &target = QRectF(), const QRectF &source = QRectF(), Qt::AspectRatioMode aspectRatioMode = Qt::KeepAspectRatio);

    void addNode(Node *node);
    void addEdge(Edge *edge);
    void addNodes(QList<Node*> nodes);
    void addEdges(QList<Edge*> edges);
    QList<Node *> createNodes(QList<int> indexes,
                           QList<QString> labels = QList<QString>(),
                           QList<QPointF> positions = QList<QPointF>(),
                           QList<QVariant> colors = QList<QVariant>(),
                           QList<QVariant> radii = QList<QVariant>());
    QList<Edge *> createEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> widths);
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
    bool pixmapVisibility();
    void setPixmapVisibility(bool visibility=true);
    void resetPixmaps();

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

    void lock(bool lock=true);
    void unlock();
    bool isLocked();

private:
    NetworkStyle *style_;
    GraphicsItemLayer *nodesLayer;
    GraphicsItemLayer *edgesLayer;
    qreal scale_;
    QList <QColor> colors_;
    bool pie_charts_visibility;
    bool pixmap_visibility;
    bool is_locked = false;
};

#endif // NETWORKSCENE_H
