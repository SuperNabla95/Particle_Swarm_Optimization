import os
import matplotlib.pyplot as plt
from matplotlib import cm
import statistics as stats
from scipy.signal import lfilter
import math

#in microseconds
t_f = 200
t_j = 50
alpha = 1.5 / 60
beta = 0
gamma = 0

def avg(lst): 
    #return sum(lst) / len(lst)
    return stats.median(lst)

def time(version,niter,particles,nt="") :
    command = "../versions/{}/pso {} {} 0 100 0 100 {} > temporary_file.txt".format(version,str(niter),str(particles),str(nt))
    os.system(command)
    f = open("temporary_file.txt","r")
    lines = f.readlines()
    #print(lines)
    time_string = lines[-1].split(": ")[-1].split("\n")[0]
    return int(time_string)

def ideal_time(niter,particles,nt) :
    #fork-join
    a = (nt+1)*math.sqrt(5)
    base = (1 + math.sqrt(5)) / 2
    ceil = math.ceil(math.log(a,base))
    fork_join = (t_f + t_j) * (ceil -3)
    #core
    core = niter * (alpha + beta + gamma) * (particles / nt)
    #total
    tot = fork_join + core
    return tot #microseconds


measurements = 5
nt_max = 4

low_niter = 10
high_niter = 50
sample_niter = [low_niter,high_niter]

few_particles = 2000
many_particles = 15000
sample_particles = [few_particles,many_particles]

nts = [nt for nt in range(1,nt_max+1)]


###############################
# PARTICLES (low niter)
###############################
print('particles for low niter')
fout = open('./data/particles_for_low_niter.txt','w')

for particles in sample_particles :
    l_seq = []
    for m in range(measurements) :
        time_seq = time('sequential',low_niter,particles)
        l_seq.append(time_seq)
    avg_seq = avg(l_seq)
    fout.write('{};'.format(str(avg_seq)))
fout.write('\n')


for nt in nts :
    for particles in sample_particles :
        l_mt = []
        l_ff = []
        for m in range(measurements) :
            time_mt = time('multithread',low_niter,particles,nt)
            time_ff = time('fastflow',low_niter,particles,nt)
            l_mt.append(time_mt)
            l_ff.append(time_ff)
        avg_mt = avg(l_mt)
        avg_ff = avg(l_ff)
        ideal = ideal_time(low_niter,particles,nt)
        fout.write('{};{};{};'.format(str(avg_mt),str(avg_ff),str(ideal)))
    fout.write('\n')
fout.close()

###############################
# PARTICLES (high niter)
###############################
print('particles for high niter')
fout = open('./data/particles_for_high_niter.txt','w')

for particles in sample_particles :
    l_seq = []
    for m in range(measurements) :
        time_seq = time('sequential',low_niter,particles)
        l_seq.append(time_seq)
    avg_seq = avg(l_seq)
    fout.write('{};'.format(str(avg_seq)))
fout.write('\n')

for nt in nts :
    for particles in sample_particles :
        l_mt = []
        l_ff = []
        for m in range(measurements) :
            time_mt = time('multithread',high_niter,particles,nt)
            time_ff = time('fastflow',high_niter,particles,nt)
            l_mt.append(time_mt)
            l_ff.append(time_ff)
        avg_mt = avg(l_mt)
        avg_ff = avg(l_ff)
        ideal = ideal_time(high_niter,particles,nt)
        fout.write('{};{};{};'.format(str(avg_mt),str(avg_ff),str(ideal)))
    fout.write('\n')
fout.close()

###############################
# NITER (few particles)
###############################
print('niter for few particles')
fout = open('./data/niter_for_few_particles.txt','w')

for particles in sample_particles :
    l_seq = []
    for m in range(measurements) :
        time_seq = time('sequential',low_niter,particles)
        l_seq.append(time_seq)
    avg_seq = avg(l_seq)
    fout.write('{};'.format(str(avg_seq)))
fout.write('\n')

for nt in nts :
    for niter in sample_niter :
        l_mt = []
        l_ff = []
        for m in range(measurements) :
            time_mt = time('multithread',niter,few_particles,nt)
            time_ff = time('fastflow',niter,few_particles,nt)
            l_mt.append(time_mt)
            l_ff.append(time_ff)
        avg_mt = avg(l_mt)
        avg_ff = avg(l_ff)
        ideal = ideal_time(niter,few_particles,nt)
        fout.write('{};{};{};'.format(str(avg_mt),str(avg_ff),str(ideal)))
    fout.write('\n')
fout.close()

###############################
# NITER (many particles)
###############################
print('niter for many particles')
fout = open('./data/niter_for_many_particles.txt','w')

for particles in sample_particles :
    l_seq = []
    for m in range(measurements) :
        time_seq = time('sequential',low_niter,particles)
        l_seq.append(time_seq)
    avg_seq = avg(l_seq)
    fout.write('{};'.format(str(avg_seq)))
fout.write('\n')

for nt in nts :
    for niter in sample_niter :
        l_mt = []
        l_ff = []
        for m in range(measurements) :
            time_mt = time('multithread',niter,many_particles,nt)
            time_ff = time('fastflow',niter,many_particles,nt)
            l_mt.append(time_mt)
            l_ff.append(time_ff)
        avg_mt = avg(l_mt)
        avg_ff = avg(l_ff)
        ideal = ideal_time(niter,many_particles,nt)
        fout.write('{};{};{};'.format(str(avg_mt),str(avg_ff),str(ideal)))
    fout.write('\n')
fout.close()
