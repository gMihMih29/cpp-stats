class ClassForLengthOfMethod {
private:
    void method1();

    void method2() {
        int n = 100;
        int j = 0;
        for (int i = 0; i < n; ++i) {
            j += i * (-i % 2);
        }
    }

    int method3() { return 1; }
};
