import os
import matplotlib.pyplot as plt
from matplotlib import cm
import statistics as stats
from scipy.signal import lfilter

import conf

dashed = [6,2]
dash_dot = [4,2,2,2]


nts = [nt for nt in range(1,conf.nt_max+1)]

def extract_data(tokens_list) :
    front = tokens_list.pop(0)
    seq = float(front[0])
    y_mt = [float(tokens[0]) for tokens in tokens_list]
    y_ff = [float(tokens[1]) for tokens in tokens_list]
    y_id = [float(tokens[2]) for tokens in tokens_list]
    return seq, y_mt, y_ff, y_id
    
def plot_completion_time(seq,y_mt,y_ff,y_id) :
    plt.plot(nts, y_mt, 'red', label='c++ threads')
    plt.plot(nts, y_ff, 'green', label='fastflow', dashes=dashed)
    plt.plot(nts, y_id, 'blue', label='ideal', dashes=dash_dot)
    plt.legend(loc='upper right')
    return

def plot_speed_up(seq,y_mt,y_ff,y_id) :
    y_mt_su = [seq/y for y in y_mt]
    y_ff_su = [seq/y for y in y_ff]
    y_id_su = [seq/y for y in y_id]

    plt.plot(nts, y_mt_su, 'red', label='c++ threads')
    plt.plot(nts, y_ff_su, 'green', label='fastflow', dashes=dashed)
    plt.plot(nts, y_id_su, 'blue', label='ideal', dashes=dash_dot)
    plt.legend(loc='upper right')
    return

def plot_efficiency(seq,y_mt,y_ff,y_id) :
    y_mt_ef = [(seq/y)/(i+1) for (i,y) in enumerate(y_mt)]
    y_ff_ef = [(seq/y)/(i+1) for (i,y) in enumerate(y_ff)]
    y_id_ef = [(seq/y)/(i+1) for (i,y) in enumerate(y_id)]

    plt.plot(nts, y_mt_ef, 'red', label='c++ threads')
    plt.plot(nts, y_ff_ef, 'green', label='fastflow', dashes=dashed)
    plt.plot(nts, y_id_ef, 'blue', label='ideal', dashes=dash_dot)
    plt.legend(loc='upper right')
    return

###############################
# FINE GRAINED (low delay, high particles)
###############################
fin = open('./data/fg.txt','r')
lines = fin.readlines()
fin.close()
tokens_list = [line.split(';') for line in lines]

seq, y_mt, y_ff, y_id = extract_data(tokens_list)

# completion time
figure_name = 'fg_ct'
plt.figure(figure_name)
plot_completion_time(seq,y_mt,y_ff,y_id)
plt.title('completion time ({} iterations, {} particles, {} microseconds delay)'.format(str(conf.iterations),str(conf.fg_particles),str(conf.fg_delay)))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#speed up
figure_name = 'fg_su'
plt.figure(figure_name)
plot_speed_up(seq,y_mt,y_ff,y_id)
plt.title('speed up ({} iterations, {} particles, {} microseconds delay)'.format(str(conf.iterations),str(conf.fg_particles),str(conf.fg_delay)))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#efficiency
figure_name = 'fg_ef'
plt.figure(figure_name)
plot_efficiency(seq,y_mt,y_ff,y_id)
plt.title('efficiency ({} iterations, {} particles, {} microseconds delay)'.format(str(conf.iterations),str(conf.fg_particles),str(conf.fg_delay)))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

###############################
# COARSE GRAINED
###############################
fin = open('./data/cg.txt','r')
lines = fin.readlines()
fin.close()
tokens_list = [line.split(';') for line in lines]

seq, y_mt, y_ff, y_id = extract_data(tokens_list)

# completion time
figure_name = 'cg_ct'
plt.figure(figure_name)
plot_completion_time(seq,y_mt,y_ff,y_id)
plt.title('completion time ({} iterations, {} particles, {} microseconds delay)'.format(str(conf.iterations),str(conf.cg_particles),str(conf.cg_delay)))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#speed up
figure_name = 'cg_su'
plt.figure(figure_name)
plot_speed_up(seq,y_mt,y_ff,y_id)
plt.title('speed up ({} iterations, {} particles, {} microseconds delay)'.format(str(conf.iterations),str(conf.cg_particles),str(conf.cg_delay)))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#efficiency
figure_name = 'cg_ef'
plt.figure(figure_name)
plot_efficiency(seq,y_mt,y_ff,y_id)
plt.title('efficiency ({} iterations, {} particles, {} microseconds delay)'.format(str(conf.iterations),str(conf.cg_particles),str(conf.cg_delay)))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)