/* Detect signals and slot in frame filters */

#include <qt5/QtCore/QObject>
#include <qt5/QtCore/QString>

class A : public QObject
{
    Q_OBJECT
public slots:
    void myslot(const QString& a, int b);
};

void A::myslot(const QString& a, int b)
{
    // Boom
    const QString s = *((QString*)0x0);
    if (s.size() == 42)
        Q_ASSERT(false);
}

class B : public QObject
{
    Q_OBJECT
signals:
    void mysignal(const QString&, int);
};

int main() {
    B b;
    A a;

    QObject::connect(&b, &B::mysignal, &a, &A::myslot);

    emit b.mysignal("foobar", 1337);

    return 0;
}

////////////////////////

/****************************************************************************
** Meta object code from reading C++ file 'qtconnect.cpp'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.6.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'qtconnect.cpp' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.6.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_A_t {
    QByteArrayData data[5];
    char stringdata0[14];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_A_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_A_t qt_meta_stringdata_A = {
    {
QT_MOC_LITERAL(0, 0, 1), // "A"
QT_MOC_LITERAL(1, 2, 6), // "myslot"
QT_MOC_LITERAL(2, 9, 0), // ""
QT_MOC_LITERAL(3, 10, 1), // "a"
QT_MOC_LITERAL(4, 12, 1) // "b"

    },
    "A\0myslot\0\0a\0b"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_A[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
       1,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    2,   19,    2, 0x0a /* Public */,

 // slots: parameters
    QMetaType::Void, QMetaType::QString, QMetaType::Int,    3,    4,

       0        // eod
};

void A::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        A *_t = static_cast<A *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->myslot((*reinterpret_cast< const QString(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        default: ;
        }
    }
}

const QMetaObject A::staticMetaObject = {
    { &QObject::staticMetaObject, qt_meta_stringdata_A.data,
      qt_meta_data_A,  qt_static_metacall, Q_NULLPTR, Q_NULLPTR}
};


const QMetaObject *A::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *A::qt_metacast(const char *_clname)
{
    if (!_clname) return Q_NULLPTR;
    if (!strcmp(_clname, qt_meta_stringdata_A.stringdata0))
        return static_cast<void*>(const_cast< A*>(this));
    return QObject::qt_metacast(_clname);
}

int A::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 1)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 1;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 1)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 1;
    }
    return _id;
}
struct qt_meta_stringdata_B_t {
    QByteArrayData data[3];
    char stringdata0[12];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_B_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_B_t qt_meta_stringdata_B = {
    {
QT_MOC_LITERAL(0, 0, 1), // "B"
QT_MOC_LITERAL(1, 2, 8), // "mysignal"
QT_MOC_LITERAL(2, 11, 0) // ""

    },
    "B\0mysignal\0"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_B[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
       1,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    2,   19,    2, 0x06 /* Public */,

 // signals: parameters
    QMetaType::Void, QMetaType::QString, QMetaType::Int,    2,    2,

       0        // eod
};

void B::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        B *_t = static_cast<B *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->mysignal((*reinterpret_cast< const QString(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        void **func = reinterpret_cast<void **>(_a[1]);
        {
            typedef void (B::*_t)(const QString & , int );
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&B::mysignal)) {
                *result = 0;
                return;
            }
        }
    }
}

const QMetaObject B::staticMetaObject = {
    { &QObject::staticMetaObject, qt_meta_stringdata_B.data,
      qt_meta_data_B,  qt_static_metacall, Q_NULLPTR, Q_NULLPTR}
};


const QMetaObject *B::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *B::qt_metacast(const char *_clname)
{
    if (!_clname) return Q_NULLPTR;
    if (!strcmp(_clname, qt_meta_stringdata_B.stringdata0))
        return static_cast<void*>(const_cast< B*>(this));
    return QObject::qt_metacast(_clname);
}

int B::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 1)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 1;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 1)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 1;
    }
    return _id;
}

// SIGNAL 0
void B::mysignal(const QString & _t1, int _t2)
{
    void *_a[] = { Q_NULLPTR, const_cast<void*>(reinterpret_cast<const void*>(&_t1)), const_cast<void*>(reinterpret_cast<const void*>(&_t2)) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}
QT_END_MOC_NAMESPACE
