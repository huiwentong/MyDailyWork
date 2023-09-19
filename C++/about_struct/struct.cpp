#include<iostream>
using namespace std;
//标准的struct构建方式
struct s_a{
    int a = 0;
    int b = 1;
};
//构建struct同时还定义结构体变量
struct s_b
{
    int a = 0;
    int b = 1;
    int c = 2;
}b_type;
//没有结构体名，因此后续不可以再定义新的结构体变量。
struct {
    int a = 1;
    int b = 2;
}type_three1,type_three2;
//没有结构体名只有别名的struct
typedef struct{
    int a;
    int b;
}type_five_alias_s;

int main(){
    s_a a_type;//在c中创建结构体变量的话还需要在最前边加上struct
    a_type.a = 999;
    s_a a_type2 = {555, 666};//这种赋值方式更快
    printf("这是用了s_a的结构体，且a的值为：%d\n", a_type.a);
    printf("这是用了s_a的结构体{}赋值，且a的值为：%d, b的值为： %d\n", a_type2.a, a_type2.b);
    cout << b_type.a << endl;
    return 0;
}