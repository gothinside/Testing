#include<iostream>
using namespace std;
void NOK(int n1,int n2){
    int max;
    max = (n1>n2) ?n1 : n2;
    do {
       if (max%n1==0 && max%n2==0)
       {
       cout << max;
       break;
       }
       else ++max;
     } while (true); 
}
int main(){
    int x,y;
    cin >> x>>y;
    NOK(x,y);
}
