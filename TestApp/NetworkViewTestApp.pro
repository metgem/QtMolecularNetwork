RESOURCES += images.qrc

HEADERS += mainwindow.h view.h \
    ../src/config.h \
    ../src/edge.h \
    ../src/mol_depiction.h \
    ../src/networkscene.h \
    ../src/node.h \
    ../src/style.h
SOURCES += main.cpp \
    ../src/edge.cpp \
    ../src/mol_depiction.cpp \
    ../src/networkscene.cpp \
    ../src/node.cpp \
    ../src/style.cpp
SOURCES += mainwindow.cpp view.cpp

QT += widgets svg
qtHaveModule(printsupport): QT += printsupport
qtHaveModule(opengl): QT += opengl

build_all:!build_pass {
    CONFIG -= build_all
    CONFIG += release
}

LIBS += -L/home/nicolas/miniconda3/envs/metgem/lib/ -lRDKitDepictor -lRDKitMolDraw2D -lRDKitRDGeneral -lRDKitSmilesParse -lRDKitRDInchiLib -lRDKitInchi
INCLUDEPATH += /home/nicolas/miniconda3/envs/metgem/include/rdkit
INCLUDEPATH += /home/nicolas/miniconda3/envs/metgem/include/cairo
