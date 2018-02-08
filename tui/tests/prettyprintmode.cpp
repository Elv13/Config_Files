#include <qt5/QtCore/QtGlobal>
#include <qt5/QtCore/QStringListModel>
#include <qt5/QtCore/QIdentityProxyModel>
#include <qt5/QtCore/QSortFilterProxyModel>

// Some elements can take a lot of place when pretty printing, but sometime
// compactness can improve readability
void a(QStringList l)
{
    QHash<QString, int> h {
       {"one"   , 1 },
       {"two"   , 2 },
       {"three" , 3 },
       {"four"  , 4 },
       {"five"  , 5 },
       {"-one"   , 1 },
       {"-two"   , 2 },
       {"-three" , 3 },
       {"-four"  , 4 },
       {"-five"  , 5 },
       {"--one"   , 1 },
       {"--two"   , 2 },
       {"--three" , 3 },
       {"--four"  , 4 },
       {"--five"  , 5 },
       {"---one"   , 1 },
       {"---two"   , 2 },
       {"---three" , 3 },
       {"---four"  , 4 },
       {"---five"  , 5 },
    };

    QStringList l3 {};

    auto ll = l;
    Q_ASSERT(false);
}

int main() {
    //TODO turn this into columns in normal mode
    //[0] "one"     | [0] "1"       | [0] "two"     | [0] "2"       |
    //[0] "three"   | [0] "3"       | [0] "four"    |               |
    //[0] "4"       | [0] "five"    | [0] "5"       | [0] "one"     |
    //[0] "1"       | [0] "two"     | [0] "2"       | [0] "three"   |
    //[0] "3"       | [0] "four"    | [0] "4"       | [0] "five"    |
    //[0] "5"       | [0] "one"     | [0] "1"       | [0] "two"     |
    //[0] "2"       | [0] "three"   | [0] "3"       | [0] "four"    |
    //[0] "4"       | [0] "five"    | [0] "5"       | [0] "one"     |
    //[0] "1"       | [0] "two"     | [0] "2"       | [0] "three"   |
    //[0] "3"       | [0] "four"    | [0] "4"       | [0] "five"    |

    //TODO Short mode [5 elems] with some color

    QStringList l {
        "one"   , "1",
        "two"   , "2",
        "three" , "3",
        "four"  , "4",
        "five"  , "5",
        "one"   , "1",
        "two"   , "2",
        "three" , "3",
        "four"  , "4",
        "five"  , "5",
        "one"   , "1",
        "two"   , "2",
        "three" , "3",
        "four"  , "4",
        "five"  , "5",
        "one"   , "1",
        "two"   , "2",
        "three" , "3",
        "four"  , "4",
        "five"  , "5",
    };

    a(l);

    return 0;
}
