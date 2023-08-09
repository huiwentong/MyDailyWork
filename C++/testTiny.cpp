#include <iostream>
#include "testTiny.h"
#include "testTiny.h"//如果头文件没有 #ifndef 的声明，则会报重定义的错误
#define STR(x)  #x //相当于输出“x”
#define MACRO_UNWARP(x) STR(X) //不管MACRO_UNWARP()中的x是啥，都会转换成STR(X)
#define MACRO_T() AAAAA //将MACRO_T()转换成AAAAA
#define MACRO_T1(a, b) INI##a##b


using namespace std;


// 左右值引用问题
void process_value(int& i){
    cout << "左值引用" << i << endl;
}
void r_process_value(int&& i){
    cout << "右值引用" << i << endl;
}
// 宏的测试

void INIab(){
    printf("只要是采用MACRO_T1的宏,就会合并成这个函数INIab,有意思吧\n");
}
void INIaa(){
    printf("只要是采用MACRO_T1的宏,就会合并成这个函数INIaa,有意思吧\n");
}
void INIbb(){
    printf("只要是采用MACRO_T1的宏,就会合并成这个函数INIbb,有意思吧\n");
}

int main(){
    system("chcp 65001");
    
    test a;
    t1 b;
    // a.a = 10; //会报错，常量静态成员变量无法被更改
    b.b = 55;
    cout << a.modi_b() << endl;
    cout << b.b << endl;
    int lr = 1;
    process_value(lr);
    // process_value(5); //会报错，因为无法引用常数
    r_process_value(5);
    // r_process_value(lr);// 会报错，因为引用了变量

    std::cout << MACRO_UNWARP(MACRO_T()) << std::endl; 

    MACRO_T1(a, b)();
    MACRO_T1(a, a)();
    MACRO_T1(b, b)();
    PRINT(); // 预定义的宏
    printf(__FILE__"\n");
    printf("%d\n", __LINE__);

    system("pause");
    return 0;
}

