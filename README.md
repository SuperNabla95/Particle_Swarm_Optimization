# Particle Swarm Optimization ― SPM :helicopter:
[SPM, spring 2018]

----
## What is all about? :mega:
from the :globe_with_meridians:[Wikipedia page](https://en.wikipedia.org/wiki/Digital_watermarking):

> the Particle Swarm Optimization (PSO) is “a computational method that optimizes a problem by iteratively trying to improve a candidate solution."

> "It solves a problem by having a population of candidate solutions, here dubbed particles, and moving these particles around in the search-space according to simple mathematical formulae over the particle’s position and velocity."
---
## The project :pencil:
This project aims at the implementation of a C++ multi-thread (and so faster) version of the PSO application. The PSO technique is here utilized to perform an **approximated calculation of the minimum of a function ina 2-dimensional search space**.

---
## Run the code :rocket:

First of all you need to clone the `fastflow` repository from the [official website](https://github.com/fastflow/fastflow). Clone the repository in the **home** directory of your machine. 

In the `versions` folder of the PSO project you will find three sub-directory, namely:
- sequential
- multithread
- fastflow

In order to compile the code execute the following operations from the linux terminal:
```bash
cd <PSO HOME>/versions/
make release -C sequential
make release -C multithread
make release -C fastflow
```

The compilation process will output -- for each of the three versions -- the `particle_swarm_optimization` executable. The executable will be made available at the path: `<PSO HOME>/versions/<VERSION>/build/apps/particle_swarm_optimization`. 

:exclamation: **Note:** if you do **not** want the optimized version (option `O3`) simply use `make` instead of `make release`. If you meet some problems during the compilation process, or you simply want to re-compile from scratch the project for some reason, use `make clean release` instead of `make release`.

:exclamation: **Note:** To compile the code on the **Xeon Phi** machine of the University of Pisa you can use the standard old compiler available when you access the machine (i.e. there is no need to use the `source` command).


When launching the application, you need to pass **seven numeric arguments** in the following order:
- the number of particles in the swarm
- the number of iterations
- the minimum x-value in the search space
- the maximum x-value in the search space
- the minimum y-value in the search space
- the maximum y-value in the search space
- the time needed for the function to be evaluated

For the `fastflow` and the `multithread` versions you need to specify yet another argument:
- the parallelism degree

For example, from the `<PSO HOME>` you could do:
```bash
#example
./versions/multithread/build/apps/particle_swarm_optimization 1000 10 0 100 0 100 10 4
```

----
## Visualize the time statistics :chart_with_upwards_trend:
In the `performance_evaluation` folder you could find some utilities to measure the times of the application.
- You can run the `write_metrics.py` script to run *two* experiments about the time performances of the PSO application. The parameters of the experiments can be set in `conf.py`.
- After running `write_metrics.py`, you can plot the resulting data using `plot_metrics.py` (:warning: Warning: this second step requires Python 3, so cannot be executed on the Xeon Phi machine)

In the `multithread` and in the `sequential` directories you will find a sub-folder called `stats`, which can be used to plot a timeline chart (:warning: Python 3 required).
For example, from the `<PSO HOME>/versions/multithread` directory you could run:
```bash
#example
./build/apps/particle_swarm_optimization 10 10 0 100 0 100 10 4
cd ./stats/
python3 plot_timeline.py pso_4_8_10.txt 

```

----
## last update
* 25-Jan-2020 updated read-me version
