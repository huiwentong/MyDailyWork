#include<iostream>
#include<typeinfo>
using namespace std;
typedef int (*func_type) (int);  // typedef定义函数指针类型
using func_type_other = int (*) (int);  // using定义指针类型语法

int* test(int* num){
    cout << "这是返回int指针的函数" << endl;
    return num;
}
int (*test1)(int* num);

int test2(int num){
    cout << " 这是一个普通的函数" << endl;
    return num;
}
// int hello(){
//     printf("hi nihao !");
//     return 0;
// }

int main(){
    int var = 3000;
    int* ptr = &var;
    int** pptr = &ptr;
    int list[5] ;
    func_type ptrfunc = test2;
    // test1 = test2;
    // cout << "ptr的值为: " << ptr << endl;
    // cout << "ptr的地址为: " << &ptr << endl;
    // cout << "ptr的类型为: " << typeid(ptr).name() << endl;
    // cout << "ptr的大小为: " << sizeof(ptr) << endl;
    // cout << "ptr偏移值为: " << ptr<<1 << endl;


    // cout << "pptr的值为" << pptr << endl;
    // cout << "pptr的地址为" << pptr << endl;

    cout<< "test1指针的值为" << test1 << endl;
    cout<< "test2指针为" << test2 << endl;
    cout<< "test指针指向的值为" << test << endl;
    cout<< "list指针指向的值为" << list << endl;

    return 0;
}