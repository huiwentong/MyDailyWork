#include<iostream>

#define TIME int times = 1;
#define TIMEADD void func(int& times){times+=1;}


#ifndef _TESTTINY_H //避免出现重定义错误 这里的 _TESTTINT_H其实可以随意命名，之所以采用这种命名方式其实就是一种规范，防止头文件的define和一些其他功能宏重名
#define _TESTTINY_H //这样我们在编写程序的时候就知道，只要是 _*_H 这样的宏声明，就一定是头文件，很好理解，如果在导入头文件是，判断def了此头文件，则直接跳到#endif处
#define PRINT()
using namespace std;
TIME
class test {
    public:
        static const int a = 1; //常量静态成员变量可以在类内进行定义 
        static int b; //静态成员变量只能在类外进行定义
        int c;
        test() = default; //强制此构造函数为默认构造函数
        ~test();
        int return_sth() const;
        int modi_b();
};

class t1:public test{
    public:
        t1();

};




t1::t1():test(){ //派生类的构造函数必须指定父类的构造函数，如果父类存在默认构造函数则不非要指定父类构造函数，但是最好保持一个良好的习惯,指定一下
    cout << "调用了t1的构造函数" << endl;
}




int test::b = 10;

// test::test(){
//     cout << "调用了test的构造函数" << endl; //会报错，因为默认构造函数不能有定义！！！

// }
test::~test(){
    cout << "调用了test的析构函数" << endl;
}
int test::return_sth() const{
    // this->c = 100; //会报错，const 成员函数无法更改成员变量，但是却可以更改静态成员变量
    return this->b;
}
int test::modi_b(){
    this->c = 55;
    return this->b;
}
#else

TIMEADD
func(times);
#define PRINT() printf("已经是第%d次导入了呦！\n", times)

#endif // _TESTTINY_H