#!/bin/sh

g++ assert.cpp -o assert -lQt5Core -I/usr/include/qt5/ -fPIC -ggdb
g++ prettyprintmode.cpp -o pptm -lQt5Core -I/usr/include/qt5/ -fPIC -ggdb -std=c++11
g++ proxychain.cpp -o proxychain -lQt5Core -I/usr/include/qt5/ -fPIC -ggdb -std=c++11
g++ qtconnect.cpp -o qtconnect -lQt5Core -I/usr/include/qt5/ -fPIC -ggdb
g++ stackoverflow.cpp -o stackoverflow -fPIC -ggdb
g++ nullobj.cpp -o nullobj -fPIC -ggdb -std=c++11
