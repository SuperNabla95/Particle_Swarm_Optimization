#include<algorithm>
#include<iostream>
#include<cfloat>
#include<functional>
#include<random>
#include<thread>
#include<utility>
#include<vector>

#include "Timer.cpp"

using namespace std;

#define ROOT 0
#define USELESS -1

#define PRINT_STATS true

class Threads{
  public:
    int a;
    float (*func)(float,float);

    const int niter,pts,min_x,max_x,min_y,max_y,nt;

  private:
    struct map_reduce_pattern{

        struct state {
            
            volatile bool is_done;
            volatile float gmax;
            volatile pair<float,float> gmax_pos;
            int tid;

            state() {}
            state(int tid) : is_done(false), gmax(FLT_MIN), gmax_pos(pair<float,float>(USELESS,USELESS)), tid(tid) {}

            void set_tid(int tid){
                this->is_done=false;
                this->gmax=FLT_MIN;
                this->tid=tid;
            }
        };

        /*inline static pair<float,float> &update_point(pair<float,float> point,pair<float,float> velocity){
            //TODO
            return nullptr;//new pair<float,float>(0,0);
        }*/

        inline void init_map_reduce(Threads *outer, thread *threads, struct state *children_s){
            if(children_s[0].tid >= outer->nt)
                return;
            threads[0] = thread(map_reduce_pattern(),outer,children_s);
            if(children_s[1].tid >= outer->nt)
                return;
            threads[1] = thread(map_reduce_pattern(),outer,children_s+1);
        }

        inline void gmax_reduce(Threads *outer, struct state *children_s, struct state *local_s){
            if(children_s[0].tid >= outer->nt)
                return;
            if(local_s->gmax < children_s[0].gmax){
                local_s->gmax = children_s[0].gmax;
                local_s->gmax_pos.first = children_s[0].gmax_pos.first;
                local_s->gmax_pos.second = children_s[0].gmax_pos.second;
            }
            if(children_s[1].tid >= outer->nt)
                return;
            if(local_s->gmax < children_s[1].gmax){
                local_s->gmax = children_s[1].gmax;
                local_s->gmax_pos.first = children_s[1].gmax_pos.first;
                local_s->gmax_pos.second = children_s[1].gmax_pos.second;
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
            //if(PRINT_STATS){outer->_timer->register_event(wid,tid,MAP_OPS);}
            vector<thread> v(2);
            int tid0,tid1;
            tid0 = 2*local_s->tid+1;
            tid1 = tid0+1;
            struct state *children_s = (state*)malloc(2*sizeof(state));
            children_s[0].set_tid(tid0);
            children_s[1].set_tid(tid1);
            init_map_reduce(outer,v.data(),children_s);

            //init local data structures
            vector<pair<float,float>> points(outer->pts), velocity(outer->pts);
            random_device rd;  //Will be used to obtain a seed for the random number engine
            mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()
            uniform_real_distribution<float> dis_x(outer->min_x,outer->max_x),dis_y(outer->min_y,outer->max_y),velo(0,1);
            for(int i=0;i<outer->pts;++i){
                points[i].first = dis_x(gen);
                points[i].second = dis_y(gen);
                velocity[i].first = velo(gen);
                velocity[i].second = velo(gen);
            }

            //processing
            //if(PRINT_STATS){outer->_timer->register_event(wid,tid,NEW_IMAGE);}
            for(int iter=0; iter<outer->niter; iter++){
                /*std::transform<>(
                    points.begin(),
                    points.end(),
                    velocity.begin(),
                    points.begin(),
                    map_reduce_pattern::update_point
                );*/

                //aggiorna velocità TODO

                for(auto e : points){
                    float value = (outer->func)(e.first,e.second);
                    if(local_s->gmax < value){
                        local_s->gmax = value;
                        local_s->gmax_pos.first = e.first;
                        local_s->gmax_pos.second = e.second;
                    }
                }
                gmax_reduce(outer,children_s,local_s);
            }            

            //if(PRINT_STATS){outer->_timer->register_event(wid,tid,MAP_OPS);}
            exit_map_reduce(outer,v.data(),children_s);
            //if(PRINT_STATS){outer->_timer->register_event(wid,tid,DONE);}
        }   
    };//end struct map_reduce_pattern

    Threads(
        float (*func)(float,float),
        int niter,
        int points_per_thread,
        int min_x,
        int max_x,
        int min_y,
        int max_y,
        int nt
    );
    //~Threads();
    void do_job();
    
}; //end class Threads

Threads::Threads(
        float (*func)(float,float),
        int niter,
        int points_per_thread,
        int min_x,
        int max_x,
        int min_y,
        int max_y,
        int nt
    ) :
      func(func),
      niter(niter),
      pts(points_per_thread),
      min_x(min_x),
      max_x(max_x),
      min_y(min_y),
      max_y(max_y),
      nt(nt) {}

void Threads::do_job(){
    auto s = new map_reduce_pattern::state(ROOT);
    map_reduce_pattern()(this,s);
}

int main(){return 0;}

/*int main(int argc, char* argv[]){
	if(argc != 2+1){
		cout << "Usage is: " << argv[0] << " <nw> nt>" << endl;
        return -1;
	}
    int nw,nt;
    nw = atoi(argv[1]);
    nt = atoi(argv[2]);

    char *src_dir_path = "/home/ftosoni/Desktop/spm/repo/large";
    char *wmark_path = "/home/ftosoni/Desktop/spm/repo/large/logo_large.png";
	imagevec *images = load_images(src_dir_path);
    Image *wmark = new Image(wmark_path);
    Timer *timer = new Timer(nw,nt);
    char *dst_path = "./qui";


    cout << "Computing" << endl;
    Threads t(nw,nt,images,wmark,timer);
    t.do_job();

    cout << "Saving" << endl;
	int counter = 0;
	for(auto img : *images){
		string img_path = string(dst_path) + "/" + to_string(counter) + ".bmp";
		char ch[img_path.size() + 1];
		std::strcpy(ch, img_path.c_str());
		img.save_bmp(ch);
		counter++;
	}
    timer->print_data();
    return 0;
}*/

