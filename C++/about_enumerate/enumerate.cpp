#include<iostream>
using namespace std;

//枚举类 的几种构建方式
enum week {MON, TU, WEN, THUR, FRI, SAT, SUN};

enum SUIT {jack=5, PANTS=15};

typedef enum{yaw, roll, pitch}something;



int main(){
    week today = WEN;
    enum SUIT cloth = jack;
    cout << today << endl;
    cout << cloth << endl;
    // switch结合枚举类的使用案例
    switch (today)
    {
    case(MON):
        cout << "today is Monday! work!work!" << endl;
        break;
    case(WEN):
        cout << "today is wensday, not happy!" << endl;
        break;
    default:
        cout << "todat is not monday or wensday!" << endl;
        break;
    }
    // 枚举类配合if逻辑语句的使用
    something asd = yaw;
    if(asd==yaw){
        printf("你这是在开飞机呢！？？");
    }
    
    return 0;
}