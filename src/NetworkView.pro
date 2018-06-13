QT += core gui widgets
config += c++11

TARGET = NetworkView
TEMPLATE = lib

win32 {
	CONFIG += staticlib	
}

DEFINES += NETWORKVIEW_LIBRARY
SOURCES += \
    node.cpp \
    edge.cpp \
    networkscene.cpp
HEADERS += \
    node.h \
    edge.h \
    networkscene.h \
    style.h \
    graphicsitem.h
    
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