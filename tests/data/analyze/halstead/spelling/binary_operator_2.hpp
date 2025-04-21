class Cls {
public:
    int& GetX() {
        return x;
    }

private:
    int x;
};

int test() {
    Cls c;
    c.GetX() ^= 12;
}
