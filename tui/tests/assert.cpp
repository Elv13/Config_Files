#include <qt5/QtCore/QtGlobal>

class C {
public:
    void c(int d, int e, int f) {
        short var  = 42;
        float var2 = 1.337;
        Q_ASSERT(var+var2 == var2-var);
    }
private:
    long attr {666};
};

void b() {C cc; cc.c(1,2,3);}
void a() {b();}

int main() {
    a();
}
