#include <cstdlib>

class C1 {
private:
    void method1() {
        return;
    }
    
    int method2() {
        return 5;
    }

    operator bool() const {
        return rand() % 2 == 0;
    }
};
