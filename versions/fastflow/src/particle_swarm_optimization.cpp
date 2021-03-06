#include <iostream>
#include <mutex>
#include <ff/parallel_for.hpp>
#include "conf.hpp"
using namespace ff;
using namespace std;

#define USELESS -1
#define MAX_FLOAT numeric_limits<float>::max()

#include<algorithm>
#include<cfloat>
#include<functional>
#include<random>
#include<thread>
#include<utility>
#include<vector>

#define STRIDE 1

inline float test_func (float a, float b, int delay_microsecs){
    const unsigned start = std::chrono::system_clock::now().time_since_epoch().count();
    unsigned end = start;
    while( end <= start + 1000*delay_microsecs ){
        end = std::chrono::system_clock::now().time_since_epoch().count();
    }
    return (a-5)*(a-5)+(b-70)*(b-70) + end%2;
}

struct global_minimum{
  float value, pos_x, pos_y;

  global_minimum(){
    value = MAX_FLOAT;
    pos_x = USELESS;
    pos_y = USELESS;
  }

  inline bool operator>(const global_minimum &other){
    return this->value > other.value;
  }

  inline void operator=(const global_minimum &other){
    this->value = other.value;
    this->pos_x = other.pos_x;
    this->pos_y = other.pos_y;
  }
};

int main(int argc, char* argv[]){
	if(argc != 8+1){
		cout << "Usage is: " << argv[0] << " <niter> <points> <min_x> <max_x> <min_y> <max_y> <delay_microsecs> <nt>" << endl;
		return -1;
	}

  int niter = atoi(argv[1]);
  int pts = atoi(argv[2]);
  float min_x = atof(argv[3]);
  float max_x = atof(argv[4]);
  float min_y = atof(argv[5]);
  float max_y = atof(argv[6]);
  int delay_microsecs = atoi(argv[7]);
  int nt = atoi(argv[8]);

  std::function<float(float,float)> _func =
      [delay_microsecs](int x, int y){return test_func(x,y,delay_microsecs);};

  long int t0 = std::chrono::system_clock::now().time_since_epoch().count();
  //initialization
  vector<pair<float,float>> points(pts), velocity(pts), lmin_pos(pts);
  vector<float> lmin(pts);
  default_random_engine dre;
  dre.seed(rand());
  uniform_real_distribution<float> dis_x(min_x,max_x),dis_y(min_y,max_y),random_fraction(0,1);
  
  struct global_minimum gmin;
  const struct global_minimum gmin_id;
  
  ParallelForReduce<global_minimum> pfr(nt,SPINWAIT);
  //ParallelForReduce<global_minimum> pfr(nt);

  //only phases 1 and 2 of the very first iteration here:
  pfr.parallel_reduce(
      gmin,
      gmin_id,
      0,pts,STRIDE,
      
      [&points,&velocity,&lmin_pos,&lmin,&dis_x,&dis_y,&dre,&random_fraction,&_func](const long i, global_minimum &pgmin) {
        //init
        points[i].first = dis_x(dre);
        points[i].second = dis_y(dre);
        velocity[i].first = random_fraction(dre);
        velocity[i].second = random_fraction(dre);
        lmin_pos[i].first = USELESS;
        lmin_pos[i].second = USELESS;
        lmin[i] = FLT_MIN;

        float value = (_func)(points[i].first,points[i].second);
        //phase 1 - map
        lmin[i] = value;
        lmin_pos[i].first = points[i].first;
        lmin_pos[i].second = points[i].second;

        //phase 2 - local reduce of iteration iter
        if(pgmin.value > lmin[i]){
          pgmin.value = lmin[i];
          pgmin.pos_x = lmin_pos[i].first;
          pgmin.pos_y = lmin_pos[i].second;
        }
      },

      [](global_minimum &accum, const global_minimum other){
        //phase 2 - global reduce of iteration iter
        if(accum > other){
          accum = other;
        }
      }
  
  );

  //all the other iterations here:
  for(int iter=0;iter<niter;iter++){
    pfr.parallel_reduce(
      gmin,
      gmin_id,
      0,pts,STRIDE,
      
      [&points,&velocity,&lmin_pos,&lmin,&dis_x,&dis_y,&dre,&random_fraction,&_func,&gmin,&min_x,&max_x,&min_y,&max_y](const long i, global_minimum &pgmin) {
        //phase 3 (of previous iteration) - map
        float r_1, r_2;
        r_1 = random_fraction(dre);
        r_2 = random_fraction(dre);
        velocity[i].first = 
                    A*velocity[i].first +
                    B*r_1*(lmin_pos[i].first - points[i].first) +
                    C*r_2*(gmin.pos_x - points[i].first);
        velocity[i].second = 
                    A*velocity[i].second +
                    B*r_1*(lmin_pos[i].second - points[i].second) +
                    C*r_2*(gmin.pos_y - points[i].second);
        points[i].first += velocity[i].first;
        points[i].second += velocity[i].second;
        points[i].first = max<float>(points[i].first,min_x);
        points[i].first = min<float>(points[i].first,max_x);
        points[i].second = max<float>(points[i].second,min_y);
        points[i].second = min<float>(points[i].second,max_y);

        //phase 1 - map
        float value = (_func)(points[i].first,points[i].second);
        if(lmin[i] > value){
          lmin[i] = value;
          lmin_pos[i].first = points[i].first;
          lmin_pos[i].second = points[i].second;
        }

        //phase 2 - local reduce of iteration iter
        if(pgmin.value > lmin[i]){
          pgmin.value = lmin[i];
          pgmin.pos_x = lmin_pos[i].first;
          pgmin.pos_y = lmin_pos[i].second;
        }
      },

      [](global_minimum &accum, const global_minimum other){
        //global reduce of iteration iter
        if(accum > other){
          accum = other;
        }
      }
    
    );
  } // end iterations

  long int elapsed = std::chrono::system_clock::now().time_since_epoch().count() - t0;
  cout << "completion time (microseconds): " << elapsed/1000 << endl;
  cout << "best extimate: " << gmin.value << " (x: " << gmin.pos_x << ", y: " << gmin.pos_y << ")" << endl;


  return 0;
}
