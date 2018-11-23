%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

%If (Qt_5_0_0 -)

class NetworkScene : public QGraphicsScene {

%TypeHeaderCode
#include "networkscene.h"
#include "graphicsitem.h"
#include "style.h"
%End

public:
    NetworkScene(QWidget *parent /TransferThis/ = nullptr);
    
    NetworkStyle *networkStyle();
    void setNetworkStyle(NetworkStyle *style /KeepReference/ = nullptr);
    
    void clear();
    
    void addNode(Node *node);
    void addEdge(Edge *edge);
    QList<Node *> addNodes(QList<int> indexes,
                           QList<QString> labels=QList<QString>(),
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
    /*void setNodesSelection(QList<int> indexes);
    void setNodesSelection(QList<Node *> nodes);*/
    void setNodesSelection(SIP_PYOBJECT) /NoArgParser/;
%Docstring
setNodesSelection(self, Iterable[int])
setNodesSelection(self, Iterable[Node])
%End
%MethodCode
    PyObject *sipParseErr = NULL;

    {
         ::QList<int>* a0;
        int a0State = 0;
         ::NetworkScene *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "BJ1", &sipSelf, sipType_NetworkScene, &sipCpp, sipType_QList_1800,&a0, &a0State))
        {
            sipCpp->setNodesSelection(*a0);
            sipReleaseType(a0,sipType_QList_1800,a0State);

            Py_INCREF(Py_None);
            return Py_None;
        }
    }
    
    if (sipParseErr != NULL)
    {
        PyObject *sipParseErr2 = NULL;
        
        {
            QList< ::Node*>* a0;
            int a0State = 0;
             ::NetworkScene *sipCpp;

            if (sipParseArgs(&sipParseErr2, sipArgs, "BJ1", &sipSelf, sipType_NetworkScene, &sipCpp, sipType_QList_0101Node,&a0, &a0State))
            {
                sipCpp->setNodesSelection(*a0);
                sipReleaseType(a0,sipType_QList_0101Node,a0State);

                Py_INCREF(Py_None);
                return Py_None;
            }
        }
        
        if (sipParseErr2 != NULL)
        {
            PyList_Append(sipParseErr, PyList_GET_ITEM(sipParseErr2, 0));
        }
    }

    /* Raise an exception if the arguments couldn't be parsed. */
    sipNoMethod(sipParseErr, sipName_NetworkScene, sipName_setNodesSelection, doc_NetworkScene_setNodesSelection);

    return NULL;
%End
    QRectF selectedNodesBoundingRect();
    
    QList<Edge *> edges() const;
    QList<Edge *> selectedEdges() const;
    /*void setEdgesSelection(QList<int> indexes);
    void setEdgesSelection(QList<Edge *> edges);*/
void setEdgesSelection(SIP_PYOBJECT) /NoArgParser/;
%Docstring
setEdgesSelection(self, Iterable[int])
setEdgesSelection(self, Iterable[Edge])
%End
%MethodCode
    PyObject *sipParseErr = NULL;

    {
         ::QList<int>* a0;
        int a0State = 0;
         ::NetworkScene *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "BJ1", &sipSelf, sipType_NetworkScene, &sipCpp, sipType_QList_1800,&a0, &a0State))
        {
            sipCpp->setEdgesSelection(*a0);
            sipReleaseType(a0,sipType_QList_1800,a0State);

            Py_INCREF(Py_None);
            return Py_None;
        }
    }
    
    if (sipParseErr != NULL)
    {
        PyObject *sipParseErr2 = NULL;
        
        {
            QList< ::Edge*>* a0;
            int a0State = 0;
             ::NetworkScene *sipCpp;

            if (sipParseArgs(&sipParseErr2, sipArgs, "BJ1", &sipSelf, sipType_NetworkScene, &sipCpp, sipType_QList_0101Edge,&a0, &a0State))
            {
                sipCpp->setEdgesSelection(*a0);
                sipReleaseType(a0,sipType_QList_0101Edge,a0State);

                Py_INCREF(Py_None);
                return Py_None;
            }
        }
        
        if (sipParseErr2 != NULL)
        {
            PyList_Append(sipParseErr, PyList_GET_ITEM(sipParseErr2, 0));
        }
    }

    /* Raise an exception if the arguments couldn't be parsed. */
    sipNoMethod(sipParseErr, sipName_NetworkScene, sipName_setEdgesSelection, doc_NetworkScene_setEdgesSelection);

    return NULL;
%End    
    
    void setLayout(QList<qreal> layout, qreal scale=0);
    void setLayout(QList<QPointF> layout, qreal scale=0);
    qreal scale();
    void setScale(qreal scale=1);
    void setLabelsFromModel(QAbstractItemModel *model, int column_id, int role=Qt::DisplayRole);
    void resetLabels();
    QList<QColor> pieColors();
    void setPieColors(QList<QColor> colors);
    void setPieChartsFromModel(QAbstractItemModel *model, QList<int> column_ids, int role=Qt::DisplayRole);
    void resetPieCharts();
    
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
};

%End