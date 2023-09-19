#define CREATEDELL_API_DU _declspec(dllexport)
 
#include <iostream>
#include "DLL1.h"
using namespace std;
//父类中函数实现 
void animal::getWide(int x) {
     wide = x;
}
void CREATEDELL_API_DU animal::getHigh(int y){
     high = y;
}//子类cat中数据输出实现
int CREATEDELL_API_DU cat::outDate(){
     return (wide + high);wide += wide;high += high;
}//子类dog数据输出实现
int CREATEDELL_API_DU dog::outDate(){
     return (wide - high);
}//函数的实现
int CREATEDELL_API_DU exportDate(){
     return 666;
}