

class A
{
        void foo() {printf("FOO! %x", this);}
};

class B
{
        A a;
}

// The backtrace gets to `foo`, but `b` is nullptr
void main() {
        B* b = nullptr;

        b->a.foo();
        
        return;
}
