#include<algorithm>
#include<iostream>
#include<cfloat>
#include<functional>
#include<random>
#include<thread>
#include<utility>
#include<vector>

#include "Timer.hpp"

using namespace std;

#define ROOT 0
#define USELESS -1
#define MAX_FLOAT numeric_limits<float>::max()

struct job_result{
    const float value, pos_x, pos_y;
};

class Thread{
    const int niter,pts;
    const float min_x,max_x,min_y,max_y;
    pair<float,float> gmin_pos;
    float gmin;

  private:
    std::function<float(float,float)> _func;
    Timer *_timer;

    struct sequential_model{

        void operator() (Thread *outer)
        {
            //init local data structures
            if(PRINT_STATS){outer->_timer->register_event(INITIALIZATION,USELESS);}
            vector<pair<float,float>> points(outer->pts), velocity(outer->pts), lmin_pos(outer->pts);
            vector<float> lmin(outer->pts);

            default_random_engine dre;
            dre.seed(7*rand()+3);
            uniform_real_distribution<float> dis_x(outer->min_x,outer->max_x),dis_y(outer->min_y,outer->max_y),random_fraction(0,1);
            for(int i=0;i<outer->pts;++i){
                points[i].first = dis_x(dre);
                points[i].second = dis_y(dre);
                velocity[i].first = random_fraction(dre);
                velocity[i].second = random_fraction(dre);
                lmin_pos[i].first = USELESS;
                lmin_pos[i].second = USELESS;
                lmin[i] = MAX_FLOAT;
            }

            //processing
            for(int iter=0; iter<outer->niter; iter++){
                if(PRINT_STATS){outer->_timer->register_event(STEP_COMPUTATION,iter);}
                //local min computation
                for(int p=0; p<outer->pts; p++){
                    float value = (outer->_func)(points[p].first,points[p].second);
                    if(lmin[p] > value){
                        lmin[p] = value;
                        lmin_pos[p].first = points[p].first;
                        lmin_pos[p].second = points[p].second;

                        //reduce
                        if(outer->gmin > value){
                                outer->gmin = value;
                                outer->gmin_pos.first = points[p].first;
                                outer->gmin_pos.second = points[p].second;
                        }
                    }
                }

                for(int i=0;i<outer->pts;i++){
                    float r_1, r_2;
                    r_1 = random_fraction(dre);
                    r_2 = random_fraction(dre);
                    velocity[i].first = 
                                A*velocity[i].first +
                                B*r_1*(lmin_pos[i].first - points[i].first) +
                                C*r_2*(outer->gmin_pos.first - points[i].first);
                    velocity[i].second = 
                                A*velocity[i].second +
                                B*r_1*(lmin_pos[i].second - points[i].second) +
                                C*r_2*(outer->gmin_pos.second - points[i].second);
                    points[i].first += velocity[i].first;
                    points[i].second += velocity[i].second;
                    //limits
                    points[i].first = max<float>(points[i].first,outer->min_x);
                    points[i].first = min<float>(points[i].first,outer->max_x);
                    points[i].second = max<float>(points[i].second,outer->min_y);
                    points[i].second = min<float>(points[i].second,outer->max_y);
                }
            }//end iteration for            
            if(PRINT_STATS){outer->_timer->register_event(DONE,USELESS);}
        }
    };//end struct sequential model

  public:
    Thread(
        std::function<float(float,float)> func,
        int niter,
        int points,
        int min_x,
        int max_x,
        int min_y,
        int max_y
    );
    //~Thread();
    job_result do_job();
    
}; //end class Thread

Thread::Thread(
        std::function<float(float,float)> func,
        int niter,
        int points,
        int min_x,
        int max_x,
        int min_y,
        int max_y
    ) :
      _func(func),
      _timer(new Timer()),
      niter(niter),
      pts(points),
      min_x(min_x),
      max_x(max_x),
      min_y(min_y),
      max_y(max_y),
      gmin_pos(USELESS,USELESS),
      gmin(MAX_FLOAT) {}

job_result Thread::do_job(){
    long int t0 = std::chrono::system_clock::now().time_since_epoch().count();
    sequential_model()(this);
    long int elapsed = std::chrono::system_clock::now().time_since_epoch().count() - t0;
    cout << "completion time (microseconds): " << elapsed/1000 << endl;
    cout << "best extimate: " << gmin << " (x: " << gmin_pos.first << ", y: " << gmin_pos.second << ")" << endl;
    if(PRINT_STATS){this->_timer->print_data(this->niter,this->pts);}
    return job_result{gmin,gmin_pos.first,gmin_pos.second};
}





