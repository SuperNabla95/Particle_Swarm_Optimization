import os
import matplotlib.pyplot as plt
from matplotlib import cm
import statistics as stats

def avg(lst): 
    #return sum(lst) / len(lst)
    return stats.median(lst)

nts = 4
measurements = 40

max_particles = 8000
step_particles = 20

viridis = cm.get_cmap('viridis', nts)

os.system("make -C sequential")
os.system("make -C multithread")
seq = []
multit = [ [] for nt in range(nts) ]
xvalues = []
for x in range(int(max_particles/step_particles)+1) :
    particles = x*step_particles
    print('particles',particles)
    xvalues.append(particles)
    seq.append([])
    for nt in range(nts) :
        multit[nt].append([])

    for measurement in range(measurements) :
        #sequential
        os.system("./sequential/pso 20 {} 0 100 0 100 > temporary_file.txt".format(str(particles)))
        f = open("temporary_file.txt","r")
        lines = f.readlines()
        time_string = lines[-1].split(": ")[-1].split("\n")[0]
        time = int(time_string)
        seq[x].append(time)
        f.close()

        #multithread
        for nt in range(1,nts+1) :
            os.system("./multithread/pso 20 {} 0 100 0 100 {} > temporary_file.txt".format(str(particles),str(nt)))
            f = open("temporary_file.txt","r")
            lines = f.readlines()
            time_string = lines[-1].split(": ")[-1].split("\n")[0]
            time = int(time_string)
            multit[nt-1][x].append(time)
            f.close()
os.system("rm temporary_file.txt")

#####################
# COMPLETION TIME 
#####################
plt.figure(1)
seq_avgs = [avg(lst) for lst in seq]
multit_avgs = []
for nt in range(nts) :
    l = [avg(lst) for lst in multit[nt]]
    multit_avgs.append(l)

plt.plot(xvalues, seq_avgs, '--r')
for nt in range(nts) :
    plt.plot(xvalues, multit_avgs[nt], viridis(1/(nt+1)))

# Custom axis
plt.ylabel("completion time (milliseconds)")
plt.xlabel("particles")
plt.title("completion time")
plt.grid(True)
#plt.xscale("log", basex=2)

#####################
# SPEED-UP 
#####################
plt.figure(2)
speedup = []
for nt in range(nts) :
    l = [i / j for i, j in zip(seq_avgs, multit_avgs[nt])] 
    speedup.append(l)

for nt in range(nts) :
    plt.plot(xvalues, speedup[nt], viridis(1/(nt+1)))

# Custom axis
plt.ylabel("speed-up factor")
plt.xlabel("particles")
plt.title("speed up")
plt.grid(True)
#plt.xscale("log", basex=2)

#####################
# EFFICIENCY 
#####################
plt.figure(3)
eff = []
for nt in range(nts) :
    l = [i / (nt+1) for i in speedup[nt]] 
    eff.append(l)

for nt in range(nts) :
    plt.plot(xvalues, eff[nt], viridis(1/(nt+1)))

# Custom axis
plt.ylabel("efficiency")
plt.xlabel("particles")
plt.title("efficiency")
plt.grid(True)
#plt.xscale("log", basex=2)

plt.show()


