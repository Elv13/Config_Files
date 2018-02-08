
void a();

void c() {
    a();
}

void b() {c();}
void a() {b();}

int main() {
    a();
}
