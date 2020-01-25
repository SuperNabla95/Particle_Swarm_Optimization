#include <chrono>
#include <iostream>
#include <string>
#include <cmath>

#include "Threads.hpp"
using namespace std;

inline float test_func (float a, float b, int delay_microsecs){
    const unsigned start = std::chrono::system_clock::now().time_since_epoch().count();
    unsigned end = start;
    while( end <= start + 1000*delay_microsecs ){
        end = std::chrono::system_clock::now().time_since_epoch().count();
    }
    return 1000 - ((a-5)*(a-5)+(b-70)*(b-70)) + end%2;
}

int main(int argc, char* argv[]){
	if(argc != 8+1){
		cout << "Usage is: " << argv[0] << " <niter> <points> <min_x> <max_x> <min_y> <max_y> <delay_microsecs> <nt>" << endl;
		return -1;
	}

    int niter = atoi(argv[1]);
    int points = atoi(argv[2]);
    float min_x = atof(argv[3]);
    float max_x = atof(argv[4]);
    float min_y = atof(argv[5]);
    float max_y = atof(argv[6]);
    int delay_microsecs = atoi(argv[7]);
    int nt = atoi(argv[8]);

    std::function<float(float,float)> func =
        [delay_microsecs](int x, int y){return test_func(x,y,delay_microsecs);};

    int points_per_thread = points / nt;
    Threads t(func,niter,points_per_thread,min_x,max_x,min_y,max_y,nt);
    auto res = t.do_job();
    //cout << res.value << " " << res.pos_x << " " << res.pos_y << endl;
    return 0;
}
