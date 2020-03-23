RESOURCES += images.qrc

HEADERS += mainwindow.h view.h \
    ../src/config.h \
    ../src/edge.h \
    ../src/graphicsitem.h \
    ../src/networkscene.h \
    ../src/node.h \
    ../src/style.h
SOURCES += main.cpp \
    ../src/edge.cpp \
    ../src/networkscene.cpp \
    ../src/node.cpp \
    ../src/style.cpp
SOURCES += mainwindow.cpp view.cpp

QT += widgets
qtHaveModule(printsupport): QT += printsupport
qtHaveModule(opengl): QT += opengl

build_all:!build_pass {
    CONFIG -= build_all
    CONFIG += release
}

