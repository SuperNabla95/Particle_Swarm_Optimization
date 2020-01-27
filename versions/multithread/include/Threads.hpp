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

class Threads{
    const int niter,pts,nt;
    const float min_x,max_x,min_y,max_y;
    volatile pair<float,float> gmin_pos;
    volatile float gmin;
    volatile int iter;

  private:
    std::function<float(float,float)> _func;
    Timer *_timer;

    struct map_reduce_pattern{

        struct state {
            volatile bool is_done;
            volatile float pgmin;
            volatile pair<float,float> pgmin_pos;
            int tid;

            state() {}
            state(int tid) : 
                is_done(false),
                pgmin(MAX_FLOAT),
                pgmin_pos(pair<float,float>(USELESS,USELESS)),
                tid(tid) {}

            void set_tid(int tid){
                this->is_done=false;
                this->pgmin=MAX_FLOAT;
                this->tid=tid;
            }
        };

        inline void init_map_reduce(Threads *outer, thread *threads, struct state *children_s){
            if(children_s[0].tid >= outer->nt)
                return;
            threads[0] = thread(map_reduce_pattern(),outer,children_s);
            if(children_s[1].tid >= outer->nt)
                return;
            threads[1] = thread(map_reduce_pattern(),outer,children_s+1);
        }

        inline void gmin_reduce(Threads *outer, struct state *children_s, struct state *local_s){
            //child 0
            if(children_s[0].tid >= outer->nt)
                return;
            while(!children_s[0].is_done){
                //spin loop
            }
            children_s[0].is_done = false;
            if(local_s->pgmin > children_s[0].pgmin){
                local_s->pgmin = children_s[0].pgmin;
                local_s->pgmin_pos.first = children_s[0].pgmin_pos.first;
                local_s->pgmin_pos.second = children_s[0].pgmin_pos.second;
            }

            //child 1
            if(children_s[1].tid >= outer->nt)
                return;
            while(!children_s[1].is_done){
                //spin loop
            }
            children_s[1].is_done = false;
            if(local_s->pgmin > children_s[1].pgmin){
                local_s->pgmin = children_s[1].pgmin;
                local_s->pgmin_pos.first = children_s[1].pgmin_pos.first;
                local_s->pgmin_pos.second = children_s[1].pgmin_pos.second;
            }
        }

        inline void exit_map_reduce(Threads *outer, thread *threads, struct state *children_s){
            if(children_s[0].tid >= outer->nt)
                return;
            threads[0].join();
            if(children_s[1].tid >= outer->nt)
                return;
            threads[1].join();
        }

        void operator() (Threads *outer, struct state *local_s)
        {
            if(PRINT_STATS){outer->_timer->register_event(local_s->tid,FORK_JOIN_OPS,USELESS);}
            vector<thread> v(2);
            int tid0,tid1;
            tid0 = 2*local_s->tid+1;
            tid1 = tid0+1;
            struct state *children_s = (state*)malloc(2*sizeof(state));
            children_s[0].set_tid(tid0);
            children_s[1].set_tid(tid1);
            init_map_reduce(outer,v.data(),children_s);

            if(PRINT_STATS){outer->_timer->register_event(local_s->tid,INITIALIZATION,USELESS);}
            //init local data structures
            vector<pair<float,float>> points(outer->pts), velocity(outer->pts), lmin_pos(outer->pts);
            vector<float> lmin(outer->pts);

            default_random_engine dre;
            dre.seed(7*local_s->tid*local_s->tid*rand()+5*local_s->tid+3);
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
                if(PRINT_STATS){outer->_timer->register_event(local_s->tid,STEP_COMPUTATION,iter);}
                //local min computation
                for(int p=0; p<outer->pts; p++){
                    float value = (outer->_func)(points[p].first,points[p].second);
                    if(lmin[p] > value){
                        lmin[p] = value;
                        lmin_pos[p].first = points[p].first;
                        lmin_pos[p].second = points[p].second;

                        //local reduce
                        if(outer->gmin > value){
                                local_s->pgmin = value;
                                local_s->pgmin_pos.first = points[p].first;
                                local_s->pgmin_pos.second = points[p].second;
                        }
                    }
                }
                //global reduce
                if(PRINT_STATS){outer->_timer->register_event(local_s->tid,REDUCE_OPS,iter);}
                gmin_reduce(outer,children_s,local_s);
                //flag is_done
                local_s->is_done = true;
                if(local_s->tid == ROOT){
                    if(outer->gmin > local_s->pgmin){
                        outer->gmin_pos.first = local_s->pgmin_pos.first;
                        outer->gmin_pos.second = local_s->pgmin_pos.second;
                        outer->gmin = local_s->pgmin;
                    }
                    if(PRINT_LOG){cout << "********************************************************************\nITERATION " + to_string(iter) + " gmin("+to_string(outer->gmin_pos.first)+","+to_string(outer->gmin_pos.second)+")="+to_string(outer->gmin)+"\n";}
                    outer->iter += 1;
                }
                //wait reduce termination
                while(iter >= outer->iter){
                    //spin loop
                }
                //update local
                if(PRINT_STATS){outer->_timer->register_event(local_s->tid,STEP_COMPUTATION,iter);}
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
                if(PRINT_LOG){cout << "tid: " + to_string(local_s->tid) + " (iter "+to_string(iter)+") pgmin("+to_string(local_s->pgmin_pos.first)+","+to_string(local_s->pgmin_pos.second)+")="+to_string(local_s->pgmin)+"\n";}
                }//end iteration for            

            if(PRINT_STATS){outer->_timer->register_event(local_s->tid,FORK_JOIN_OPS,USELESS);}
            exit_map_reduce(outer,v.data(),children_s); 
            if(PRINT_STATS){outer->_timer->register_event(local_s->tid,DONE,USELESS);}
        }
    };//end struct map_reduce_pattern

  public:
    Threads(
        std::function<float(float,float)> func,
        int niter,
        int points_per_thread,
        int min_x,
        int max_x,
        int min_y,
        int max_y,
        int nt
    );
    //~Threads();
    job_result do_job();
    
}; //end class Threads

Threads::Threads(
        std::function<float(float,float)> func,
        int niter,
        int points_per_thread,
        int min_x,
        int max_x,
        int min_y,
        int max_y,
        int nt
    ) :
      _func(func),
      _timer(new Timer(nt)),
      niter(niter),
      pts(points_per_thread),
      min_x(min_x),
      max_x(max_x),
      min_y(min_y),
      max_y(max_y),
      nt(nt),
      gmin_pos(USELESS,USELESS),
      gmin(MAX_FLOAT),
      iter(0) {}

job_result Threads::do_job(){
    long int t0 = std::chrono::system_clock::now().time_since_epoch().count();
    auto s = new map_reduce_pattern::state(ROOT);
    map_reduce_pattern()(this,s);
    long int elapsed = std::chrono::system_clock::now().time_since_epoch().count() - t0;
    cout << "completion time (microseconds): " << elapsed/1000 << endl;
    cout << "best extimate: " << gmin << " (x: " << gmin_pos.first << ", y: " << gmin_pos.second << ")" << endl;
    if(PRINT_STATS){this->_timer->print_data(this->niter,this->pts);}
    return job_result{this->gmin,this->gmin_pos.first,this->gmin_pos.second};
}



