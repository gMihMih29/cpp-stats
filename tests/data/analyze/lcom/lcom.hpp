class Class1 {
public:
    void SetX(int x) {
        x_ = x;
    }

    void SetY(int y) {
        y_ = y;
    }

    int GetX() const {
        return x_;
    }

    int GetY() const {
        return y_;
    }
private:
    int x_;
    int y_;
};

class Class2 {
public:
    void SetX(int x) {
        x_ = x;
        y_ = x * 2;
    }

    void SetY(int y) {
        y_ = y;
        x_ = y * y;
        SetX(x_);
    }

    int GetX() const {
        return x_;
    }

    int GetY() const {
        return y_;
    }
private:
    int x_;
    int y_;
};
