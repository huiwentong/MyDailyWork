#include <iostream>
using namespace std;

class Box
{
    public:
        double length;
        double height;
        double width;
        double get(void);
        void set(const double len, const double hei, const double wi);
        friend void printBox(const Box& b);
        Box(const Box& b);
        Box(double l, double w, double h);
        ~Box(void);
        Box operator+(const Box& b);
        friend ostream &operator<<(const ostream& cout ,const Box& b);
    private:
        char* secret = "我是的大大啊";

};

int main() {
    /* int var[10] = {10,2,10,5,50,60,80,70,50,2};
    short int t = 1000000000;
    long int tt = 1000000000; */
    system("chcp 65001");
    //枚举类
    enum week {MON=5, TU, WEN, THUR, FRI, SAT, SUN};
    enum week today = WEN;
    enum SUIT {jack=5, PANTS=15};
    enum SUIT cloth = jack;
    typedef enum{yaw, roll, pitch}something;
    something asd = yaw;
    //枚举类
    Box a(5,5,5);
    Box b = a;
    Box c(a);
    cout << b.get() << endl;
    cout << today << endl;
    cout << cloth << endl;
    printBox(b);
    system("pause");
    return 0;
}



Box::Box(double l=1.0, double w=2.0, double h=3.0){
    cout << "调用了构造函数" << endl;
    length = l;
    width = w;
    height = h;
}
Box::Box(const Box& b){
    cout << "调用拷贝构造函数啦哈哈哈" << endl;
    length = b.length;
    width = b.width;
    height = b.height;
}
Box::~Box(void){
    cout << "调用了析构函数" << endl;
}

double Box::get(void){
    return height* width* length;
}
void Box::set(const double len, const double hei, const double wi){
    length = len;
    height = hei;
    width = wi;
}
void printBox(const Box& b){
    cout << &b << "'s length is : " << b.length << endl;
}