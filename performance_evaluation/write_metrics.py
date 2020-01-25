import os
#import statistics as stats
import math

import conf as conf

def avg(lst): 
    #compute median without using external libraries
    sorted_lst = sorted(lst)
    m = int(len(lst)/2)
    return sorted_lst[m]

def time(version,delay,particles,nt="") :
    command = "../versions/{}/build/apps/particle_swarm_optimization {} {} 0 100 0 100 {} {} > temporary_file.txt".format(version,str(conf.iterations),str(particles),str(delay),str(nt))
    os.system(command)
    f = open("temporary_file.txt","r")
    lines = f.readlines()
    #print(lines)
    time_string = lines[-2].split(": ")[-1].split("\n")[0]
    return int(time_string)

def ideal_time(delay,particles,nt) :
    return conf.iterations*delay*particles / nt

nts = [nt for nt in range(1,conf.nt_max+1)]

###############################
# FINE GRAINED (low delay, high particles)
###############################
print('fine grained')
fout = open('./data/fg.txt','w')

l_seq = []
for m in range(2*conf.measurements) :
    time_seq = time('sequential',conf.fg_delay,conf.fg_particles)
    l_seq.append(time_seq)
avg_seq = avg(l_seq)
fout.write('{};'.format(str(avg_seq)))
fout.write('\n')


for nt in nts :
    print('fg, nt:', nt)
    l_mt = []
    l_ff = []
    for m in range(conf.measurements) :
        time_mt = time('multithread',conf.fg_delay,conf.fg_particles,nt)
        time_ff = time('fastflow',conf.fg_delay,conf.fg_particles,nt)
        l_mt.append(time_mt)
        l_ff.append(time_ff)
    avg_mt = avg(l_mt)
    avg_ff = avg(l_ff)
    ideal = ideal_time(conf.fg_delay,conf.fg_particles,nt)
    fout.write('{};{};{};'.format(str(avg_mt),str(avg_ff),str(ideal)))
    fout.write('\n')
fout.close()

###############################
# COARSE GRAINED (high delay, few particles)
###############################
print('coarse grained')
fout = open('./data/cg.txt','w')

l_seq = []
for m in range(2*conf.measurements) :
    time_seq = time('sequential',conf.cg_delay,conf.cg_particles)
    l_seq.append(time_seq)
avg_seq = avg(l_seq)
fout.write('{};'.format(str(avg_seq)))
fout.write('\n')


for nt in nts :
    print('cg, nt:', nt)
    l_mt = []
    l_ff = []
    for m in range(conf.measurements) :
        time_mt = time('multithread',conf.cg_delay,conf.cg_particles,nt)
        time_ff = time('fastflow',conf.cg_delay,conf.cg_particles,nt)
        l_mt.append(time_mt)
        l_ff.append(time_ff)
    avg_mt = avg(l_mt)
    avg_ff = avg(l_ff)
    ideal = ideal_time(conf.cg_delay,conf.cg_particles,nt)
    fout.write('{};{};{};'.format(str(avg_mt),str(avg_ff),str(ideal)))
    fout.write('\n')
fout.close()