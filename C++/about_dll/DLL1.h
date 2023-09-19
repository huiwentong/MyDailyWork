#ifndef CREATEDELL_API_DU                                                                      
#define CREATEDELL_API_DU _declspec(dllimport) //当编译时，头文件不参加编译，所以.cpp文件中先定义，后头文件被包含进来，因此外部使用时，为dllexport，而在内部编译时，则为dllimport
#endif                                         
#include<iostream>

class CREATEDELL_API_DU  animal                //需要被外界调用的类（父类）
{
public:
    virtual int outDate() = 0;                 //纯虚函数
    void getWide(int x); 
    void getHigh(int y);
 
protected:
    int wide;
    int high;
};
 
                                                
class CREATEDELL_API_DU cat:public animal      //需要被调用的类（子类cat）
{
public:
    int outDate();
};
 
 
class  CREATEDELL_API_DU dog :public animal     //需要被调用的类（子类dog）
{
public:
    int outDate();
};
 
int CREATEDELL_API_DU exportDate();             //需要被调用的函数（单独的一个函数，不属于任何一个类）