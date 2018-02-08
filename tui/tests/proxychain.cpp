#include <qt5/QtCore/QtGlobal>
#include <qt5/QtCore/QStringListModel>
#include <qt5/QtCore/QIdentityProxyModel>
#include <qt5/QtCore/QSortFilterProxyModel>

// This test case doesn't have a "real bug", but that's not the point.
// The issue it's trying to solve is tracking "flat" models across a proxy chain
// is "hard" because it never makes it to the backtrace.
int main() {
    QStringList l {
        "one"   , "1",
        "two"   , "2",
        "three" , "3",
        "four"  , "4",
        "five"  , "5",
        "six"
    };
    QStringListModel origin(l);

    QSortFilterProxyModel filter(&origin);
    filter.setSourceModel(&origin);
    filter.setFilterRegExp("[a-z]+");

    QIdentityProxyModel identity(&filter);
    identity.setSourceModel(&filter);

    auto idx1 = origin.index(origin.rowCount()-1,0);
    auto idx2 = identity.index(identity.rowCount()-1,0);

    // False because they don't have the same proxy, but they point to the
    // same source.
    Q_ASSERT(idx1 == idx2);

    return 0;
}
