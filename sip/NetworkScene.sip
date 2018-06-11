%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class NetworkScene : public QGraphicsScene {

%TypeHeaderCode
#include "networkscene.h"
#include "graphicsitem.h"
%End

public:
    NetworkScene(QWidget *parent /TransferThis/ = 0);
    
    void clear();
    
    QList<Node *> addNodes(QList<int> indexes, QList<QString> labels=QList<QString>(), QList<QPointF> positions = QList<QPointF>(), QList<QVariant> colors = QList<QVariant>());
    QList<Edge *> addEdges(QList<int> indexes, QList<Node *> sourceNodes, QList<Node *> destNodes, QList<qreal> weights, QList<qreal> widths);
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
    
    QList<QColor> nodesColors();
    void setNodesColors(QList<QVariant> colors);
    void setSelectedNodesColor(QColor color);
    
    Node *nodeAt(const QPointF &position, const QTransform &deviceTransform) const;
    Node *nodeAt(qreal x, qreal y, const QTransform &deviceTransform) const;
    Edge *edgeAt(const QPointF &position, const QTransform &deviceTransform) const;
    Edge *edgeAt(qreal x, qreal y, const QTransform &deviceTransform) const;
};

%End