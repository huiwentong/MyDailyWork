#include <iostream>
using namespace std;

class Static_Mesh
{
public:

    int num;
    Static_Mesh();
    static void test();
};
Static_Mesh::Static_Mesh()
{
    int num = 0;
}

void Static_Mesh::test()
{
    cout<<"hellow!"<<endl;
    system("pause");
}