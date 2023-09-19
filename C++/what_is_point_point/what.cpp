#include<iostream>
#include<typeinfo>
#include<pthread.h>

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


//使用二级指针来给char*类型进行值替换
char* swap(char** a, char** b){
    char* temp = *a;
    *a = *b;
    *b = temp;
}

//使用引用可以指针降维,结果和上方swap相同
char* swap_ref(const char* &a, const char* &b){
    const char* temp = a;
    a = b;
    b = temp;
}

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

    const char* a = "abc";
    const char* b = "xyz";
    
    swap(a, b);
    cout << a << endl;
    cout << b << endl;
    swap_ref(a, b);
    cout << a << endl;
    cout << b << endl;

    return 0;
}