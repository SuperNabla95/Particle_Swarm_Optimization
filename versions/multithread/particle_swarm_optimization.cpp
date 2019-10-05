#include <chrono>
#include <iostream>
#include <string>
#include <cmath>

#include "Threads.cpp"
using namespace std;

float func (float a, float b){
    return 1000 - ((a-5)*(a-5)+(b-70)*(b-70));
    //return (a+b)*(a+b);
}

int main(int argc, char* argv[]){
	if(argc != 7+1){
		cout << "Usage is: " << argv[0] << " <niter> <points> <min_x> <max_x> <min_y> <max_y> <nt>" << endl;
		return -1;
	}

    int niter = atoi(argv[1]);
    int points = atoi(argv[2]);
    float min_x = atof(argv[3]);
    float max_x = atof(argv[4]);
    float min_y = atof(argv[5]);
    float max_y = atof(argv[6]);
    int nt = atoi(argv[7]);

    int points_per_thread = points / nt;
    Threads t(func,niter,points_per_thread,min_x,max_x,min_y,max_y,nt);
    auto res = t.do_job();
    cout << res.value << " " << res.pos_x << " " << res.pos_y << endl;
    return 0;
}
