

CONFIG += c++17

LIBS+=-LC:\Qt\5.15.2\mingw81_64\lib\libQt5OpenGL.a -framework OpenGL

QT       += core gui opengl openglwidgets


greaterThan(QT_MAJOR_VERSION, 5): QT += widgets

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    letter.cpp \
    main.cpp \
    mainwindow.cpp

HEADERS += \
    letter.h \
    mainwindow.h

FORMS += \
    mainwindow.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
