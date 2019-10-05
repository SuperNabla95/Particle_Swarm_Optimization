#include <iostream>
#include <mutex>
#include <ff/parallel_for.hpp>
#include "conf.cpp"
using namespace ff;
using namespace std;

#define USELESS -1
#define MIN_FLOAT -numeric_limits<float>::max()

#include<algorithm>
#include<cfloat>
#include<functional>
#include<random>
#include<thread>
#include<utility>
#include<vector>

struct global_maximum{
  float value, pos_x, pos_y;

  global_maximum(){
    value = MIN_FLOAT;
    pos_x = USELESS;
    pos_y = USELESS;
  }

  inline bool operator<(const global_maximum &other){
    return this->value < other.value;
  }

  inline void operator=(const global_maximum &other){
    this->value = other.value;
    this->pos_x = other.pos_x;
    this->pos_y = other.pos_y;
  }
};

float func(float a,float b){
  return 1000 - ((a-5)*(a-5)+(b-70)*(b-70));
}

int main(int argc, char* argv[]){
    if(argc != 7+1){
      cout << "Usage is: " << argv[0] << " <niter> <points> <min_x> <max_x> <min_y> <max_y> <nt>" << endl;
      return -1;
    }
    int niter = atoi(argv[1]);
    int pts = atoi(argv[2]);
    float min_x = atof(argv[3]);
    float max_x = atof(argv[4]);
    float min_y = atof(argv[5]);
    float max_y = atof(argv[6]);
    int nt = atoi(argv[7]);

    float (*_func)(float,float) = func;

    long int t0 = std::chrono::system_clock::now().time_since_epoch().count();
    //initialization
    vector<pair<float,float>> points(pts), velocity(pts), lmax_pos(pts);
    vector<float> lmax(pts);
    default_random_engine dre;
    dre.seed(rand());
    uniform_real_distribution<float> dis_x(min_x,max_x),dis_y(min_y,max_y),random_fraction(0,1);
    
    struct global_maximum gmax;
    const struct global_maximum gmax_id;
    
    ParallelForReduce<global_maximum> pfr(nt,SPINWAIT);

    pfr.parallel_for(0,pts,[&points,&velocity,&lmax_pos,&lmax,&dis_x,&dis_y,&dre,&random_fraction,&_func](const long i) {
      //iteration 0
      points[i].first = dis_x(dre);
      points[i].second = dis_y(dre);
      velocity[i].first = random_fraction(dre);
      velocity[i].second = random_fraction(dre);
      lmax_pos[i].first = USELESS;
      lmax_pos[i].second = USELESS;
      lmax[i] = FLT_MIN;

      float value = (_func)(points[i].first,points[i].second);
      //map (phase 1)
      lmax[i] = value;
      lmax_pos[i].first = points[i].first;
      lmax_pos[i].second = points[i].second;
    });

    for(int iter=0;iter<=niter-2;iter++){
      pfr.parallel_reduce(
        gmax,
        gmax_id,
        0,pts,1,
        
        [&lmax,&lmax_pos](const long int i, global_maximum &pgmax){
          //local reduce of iteration iter
          if(pgmax.value < lmax[i]){
            pgmax.value = lmax[i];
            pgmax.pos_x = lmax_pos[i].first;
            pgmax.pos_y = lmax_pos[i].second;
          }
        },
        
        [](global_maximum &accum, const global_maximum other){
          //global reduce of iteration iter
          if(accum < other){
            accum = other;
          }
        }
      
      );

      pfr.parallel_for(0,pts,[&points,&velocity,&min_x,&max_x,&min_y,&max_y,&random_fraction,&dre,&lmax,&lmax_pos,&gmax,&_func](const long int i){
        //phase 3 of iteration iter
        float r_1, r_2;
        r_1 = random_fraction(dre);
        r_2 = random_fraction(dre);
        velocity[i].first = 
                    A*velocity[i].first +
                    B*r_1*(lmax_pos[i].first - points[i].first) +
                    C*r_2*(gmax.pos_x - points[i].first);
        velocity[i].second = 
                    A*velocity[i].second +
                    B*r_1*(lmax_pos[i].second - points[i].second) +
                    C*r_2*(gmax.pos_y - points[i].second);
        points[i].first += velocity[i].first;
        points[i].second += velocity[i].second;
        points[i].first = max<float>(points[i].first,min_x);
        points[i].first = min<float>(points[i].first,max_x);
        points[i].second = max<float>(points[i].second,min_y);
        points[i].second = min<float>(points[i].second,max_y);

        //phase 1 of iteration iter+1
        float value = (_func)(points[i].first,points[i].second);
        if(lmax[i] < value){
          lmax[i] = value;
          lmax_pos[i].first = points[i].first;
          lmax_pos[i].second = points[i].second;
        }
      });
    }//end iteration for loop

    pfr.parallel_reduce(
      gmax,
      gmax_id,
      0,pts,1,
      
      [&lmax,&lmax_pos](const long int i, global_maximum &pgmax){
        //local reduce of last iteration
        if(pgmax.value < lmax[i]){
          pgmax.value = lmax[i];
          pgmax.pos_x = lmax_pos[i].first;
          pgmax.pos_y = lmax_pos[i].second;
        }
      },
      
      [](global_maximum &accum, const global_maximum other){
        //global reduce of last iterationelse{
        if(accum < other){
          accum = other;
        }
      }
    );


    long int elapsed = std::chrono::system_clock::now().time_since_epoch().count() - t0;
    //cout << "best extimate: " << gmax.value << " (x: " << gmax.pos_x << ", y: " << gmax.pos_y << ")" << endl;
    cout << "completion time (microseconds): " << elapsed/1000 << endl;

    return 0;
}
