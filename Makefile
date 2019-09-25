all: Threads.cpp
	g++ -std=c++11 particle_swarm_optimization.cpp -o pso -L/usr/X11R6/lib -lm -lpthread -lX11

clean:
	$(RM) main
