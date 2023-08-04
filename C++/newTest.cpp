#include <iostream>
#include <string>
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
        Box()=default; //默认构造函数就不需要再定义了
        Box(const Box& b);
        Box(double l, double w, double h):length(l), width(w), height(h){cout << "另一种赋值方式" << endl;}
        ~Box();
        Box operator+(const Box& b);
        friend ostream &operator<<(const ostream& cout ,const Box& b);
    private:
        string secret = "我是的大大啊";

};
class TinyBox: public Box{
    public:
        TinyBox(double l);
    private:
        Box g;
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
    TinyBox d(3);
    cout << b.get() << endl;
    cout << today << endl;
    cout << cloth << endl;
    cout << d.get() << endl;
    printBox(b);
    system("pause");
    return 0;
}


TinyBox::TinyBox(double l){
    cout << "调用了基类的默认构造函数" <<endl;
    length = l;
    height = l;
    width = l;
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