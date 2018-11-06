QT += core gui widgets
CONFIG += c++11

TARGET = NetworkView
TEMPLATE = lib

win32 {
	CONFIG += staticlib	
}

DEFINES += NETWORKVIEW_LIBRARY
SOURCES += \
    node.cpp \
    edge.cpp \
    networkscene.cpp \
    style.cpp
HEADERS += \
    networkscene.h \
    node.h \
    edge.h \
    style.h \
    graphicsitem.h \
    config.h
    
unix {
    networkview.files=$PWD/src/libPyNetworkView.so*
    networkview.path = /usr/lib
    INSTALLS += networkview

    target.path = /usr/lib
    INSTALLS += target
}

mac {
	QMAKE_LFLAGS += -stdlib=libc++
	QMAKE_CXXFLAGS += -stdlib=libc++

    target.path = /usr/local/lib
    INSTALLS += target
}
