#include <chrono>
#include <iostream>
#include <string>
#include <cmath>

#include "Thread.cpp"
using namespace std;


int main(int argc, char* argv[]){
	if(argc != 6+1){
		cout << "Usage is: " << argv[0] << " <niter> <points> <min_x> <max_x> <min_y> <max_y>" << endl;
		return -1;
	}

    int niter = atoi(argv[1]);
    int points = atoi(argv[2]);
    int min_x = atoi(argv[3]);
    int max_x = atoi(argv[4]);
    int min_y = atoi(argv[5]);
    int max_y = atoi(argv[6]);
    Thread t(func,niter,points,min_x,max_x,min_y,max_y);
    t.do_job();
    return 0;
}
