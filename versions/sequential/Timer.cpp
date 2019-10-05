#include <thread>
#include <iostream>
#include <fstream>
#include <atomic>
#include <chrono>
#include <future>
#include <vector>
#include <queue>
#include <string>

#include "conf.cpp"

using namespace std;

struct event{
    const long int time;
    const int event_type, iter;

    event(long int t, int et, int iter) : 
      time(t),
      event_type(et),
      iter(iter) {}

    string to_string(){//bool is_even){
        string color;
        bool is_even = this->iter%2==0;
        switch (event_type)
        {
        case INITIALIZATION:
            color = color_event<INITIALIZATION>::value;
            break;
        case FORK_JOIN_OPS:
            color = color_event<FORK_JOIN_OPS>::value;
            break;
        case REDUCE_OPS:
            color = color_event<REDUCE_OPS>::value;
            break;
        case STEP_COMPUTATION:
            color = is_even ? color_event<EVEN_STEP_COMPUTATION>::value : color_event<ODD_STEP_COMPUTATION>::value;
            break;
        default:
            color = color_event<DEFAULT>::value;
            break;
        }
        //conversion nano- to microseconds
        return ::to_string(time/100) + "@" + color;
    }
};

// stopwatch. Returns time in seconds
class Timer {
  private:
    const long int origin;
    queue<struct event> times;

  public:

    Timer() : origin(std::chrono::system_clock::now().time_since_epoch().count())
    {
        this->times = queue<struct event>();
    }

    inline void register_event(int event_type, int iter) {
        long int elapsed = std::chrono::system_clock::now().time_since_epoch().count() - this->origin;
        struct event ev(elapsed,event_type,iter);
        this->times.push(ev);
    }

    void print_data(int niter,int pts){
        string out_file_path = "stats/pso_" + to_string(pts) + "_" + to_string(niter) + ".txt";
        ofstream outfile (out_file_path,ofstream::binary);
        //bool is_even = true;
        queue<event> q = this->times;
        outfile << "@main" << endl;
        while (!q.empty()) {
            auto ev = q.front();
            //is_even = ev.event_type!=NEW_IMAGE ? is_even : !is_even;
            outfile << ev.to_string() << endl; 
            q.pop(); 
        } 
    }
};
