
#include<iostream>
#include<pthread.h>
#include<thread>
//这个文件不太好测试是因为编译的时候需要在g++ pthread.cpp -pthread 执行这一条指令才可以，否则的话找不到相关的库文件
#define NUM_THREAD   5

using namespace std;

// 基于 POSIX 开发多线程程序
void* thread_func(void* args){

    int tid = *(int *)args;
    cout << tid <<":Hello Thread!" << endl;
    pthread_exit(NULL);
    
}
// C++11 中加入了 <thread> 头文件，此头文件主要声明了 std::thread 线程类
void t_func(int &num){
    cout << num << ":Hello thread!" << endl;
}

int main(){

    pthread_t tids[NUM_THREAD];
    int index[NUM_THREAD];
    for(int i=0;i<NUM_THREAD;i++){
        index[i] = i;
        pthread_create(&tids[i], NULL, thread_func, (void*)&index[i]);
    }
    for(int i=0;i<NUM_THREAD;i++){
        pthread_join(tids[i], NULL);
    }
    pthread_exit(NULL);

     

    return 0;
}
