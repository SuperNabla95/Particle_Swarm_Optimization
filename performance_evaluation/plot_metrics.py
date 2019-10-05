import os
import matplotlib.pyplot as plt
from matplotlib import cm
import statistics as stats
from scipy.signal import lfilter


dashed = [6,2]
dash_dot = [4,2,2,2]

nt_max = 4
nts = [nt for nt in range(1,nt_max+1)]

low_niter = 10
high_niter = 50
sample_niter = [low_niter,high_niter]

few_particles = 2000
many_particles = 15000
sample_particles = [few_particles,many_particles]

labels_particle = ['{} particles'.format(particles) for particles in sample_particles]
labels_niter = ['{} iterations'.format(it) for it in sample_niter]


def plot_completion_time(tokens_list,is_labels_particle) :
    front = tokens_list.pop(0)
    ydata_mt0 = [float(tokens[0]) for tokens in tokens_list]
    ydata_ff0 = [float(tokens[1]) for tokens in tokens_list]
    ydata_id0 = [float(tokens[2]) for tokens in tokens_list]
    ydata_mt1 = [float(tokens[3]) for tokens in tokens_list]
    ydata_ff1 = [float(tokens[4]) for tokens in tokens_list]
    ydata_id1 = [float(tokens[5]) for tokens in tokens_list]
    seq = [float(front[0]), float(front[1])]

    if is_labels_particle :
        plt.plot(nts, ydata_mt0, 'r', label=labels_particle[0])
        plt.plot(nts,ydata_ff0, 'r', dashes=dashed)
        plt.plot(nts, ydata_id0, 'r', dashes=dash_dot)
        plt.plot(nts,ydata_mt1, 'b', label=labels_particle[1])
        plt.plot(nts, ydata_ff1, 'b', dashes=dashed)
        plt.plot(nts,ydata_id1, 'b', dashes=dash_dot)
    else :
        plt.plot(nts, ydata_mt0, 'r', label=labels_niter[0])
        plt.plot(nts,ydata_ff0, 'r', dashes=dashed)
        plt.plot(nts, ydata_id0, 'r', dashes=dash_dot)
        plt.plot(nts,ydata_mt1, 'b', label=labels_niter[1])
        plt.plot(nts, ydata_ff1, 'b', dashes=dashed)
        plt.plot(nts,ydata_id1, 'b', dashes=dash_dot)

    plt.legend(loc='upper right')
    return ydata_mt0, ydata_ff0, ydata_id0, ydata_mt1, ydata_ff1, ydata_id1, seq

def plot_speed_up(ydata_mt0, ydata_ff0, ydata_id0, ydata_mt1, ydata_ff1, ydata_id1, seq,is_labels_particle) :
    ydata_mt0 = [seq[0]/y for y in ydata_mt0]
    ydata_ff0 = [seq[0]/y for y in ydata_ff0]
    ydata_id0 = [seq[0]/y for y in ydata_id0]
    ydata_mt1 = [seq[1]/y for y in ydata_mt1]
    ydata_ff1 = [seq[1]/y for y in ydata_ff1]
    ydata_id1 = [seq[1]/y for y in ydata_id1]

    if is_labels_particle :
        plt.plot(nts, ydata_mt0, 'r', label=labels_particle[0])
        plt.plot(nts,ydata_ff0, 'r', dashes=dashed)
        plt.plot(nts, ydata_id0, 'r', dashes=dash_dot)
        plt.plot(nts,ydata_mt1, 'b', label=labels_particle[1])
        plt.plot(nts, ydata_ff1, 'b', dashes=dashed)
        plt.plot(nts,ydata_id1, 'b', dashes=dash_dot)
    else :
        plt.plot(nts, ydata_mt0, 'r', label=labels_niter[0])
        plt.plot(nts,ydata_ff0, 'r', dashes=dashed)
        plt.plot(nts, ydata_id0, 'r', dashes=dash_dot)
        plt.plot(nts,ydata_mt1, 'b', label=labels_niter[1])
        plt.plot(nts, ydata_ff1, 'b', dashes=dashed)
        plt.plot(nts,ydata_id1, 'b', dashes=dash_dot)

    plt.legend(loc='upper left')
    return

def plot_efficiency(ydata_mt0, ydata_ff0, ydata_id0, ydata_mt1, ydata_ff1, ydata_id1,is_labels_particle) :
    ydata_mt0 = [i / j for i, j in zip(ydata_mt0, nts)]
    ydata_ff0 = [i / j for i, j in zip(ydata_ff0, nts)]
    ydata_id0 = [i / j for i, j in zip(ydata_id0, nts)]
    ydata_mt1 = [i / j for i, j in zip(ydata_mt1, nts)]
    ydata_ff1 = [i / j for i, j in zip(ydata_ff1, nts)]
    ydata_id1 = [i / j for i, j in zip(ydata_id1, nts)]

    if is_labels_particle :
        plt.plot(nts, ydata_mt0, 'r', label=labels_particle[0])
        plt.plot(nts,ydata_ff0, 'r', dashes=dashed)
        plt.plot(nts, ydata_id0, 'r', dashes=dash_dot)
        plt.plot(nts,ydata_mt1, 'b', label=labels_particle[1])
        plt.plot(nts, ydata_ff1, 'b', dashes=dashed)
        plt.plot(nts,ydata_id1, 'b', dashes=dash_dot)
    else :
        plt.plot(nts, ydata_mt0, 'r', label=labels_niter[0])
        plt.plot(nts,ydata_ff0, 'r', dashes=dashed)
        plt.plot(nts, ydata_id0, 'r', dashes=dash_dot)
        plt.plot(nts,ydata_mt1, 'b', label=labels_niter[1])
        plt.plot(nts, ydata_ff1, 'b', dashes=dashed)
        plt.plot(nts,ydata_id1, 'b', dashes=dash_dot)

    plt.legend(loc='upper right')
    return

###############################
# PARTICLES (low niter)
###############################

fin = open('./data/particles_for_low_niter.txt','r')
lines = fin.readlines()
fin.close()
tokens_list = [line.split(';') for line in lines]

# completion time
figure_name = 'ct_particles_for_low_niter'
plt.figure(figure_name)
y1,y2,y3,y4,y5,y6,y7 = plot_completion_time(tokens_list,True)
plt.title('completion time ({} iterations)'.format(low_niter))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#speed up
figure_name = 'su_particles_for_low_niter'
plt.figure(figure_name)
plot_speed_up(y1,y2,y3,y4,y5,y6,y7,True)
plt.title('speed up ({} iterations)'.format(low_niter))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#efficiency
figure_name = 'ef_particles_for_low_niter'
plt.figure(figure_name)
plot_efficiency(y1,y2,y3,y4,y5,y6,True)
plt.title('efficiency ({} iterations)'.format(low_niter))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

###############################
# PARTICLES (high niter)
###############################

fin = open('./data/particles_for_high_niter.txt','r')
lines = fin.readlines()
fin.close()
tokens_list = [line.split(';') for line in lines]


# completion time
figure_name = 'ct_particles_for_high_niter'
plt.figure(figure_name)
y1,y2,y3,y4,y5,y6,y7 = plot_completion_time(tokens_list,True)
plt.title('completion time ({} iterations)'.format(high_niter))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#speed up
figure_name = 'su_particles_for_high_niter'
plt.figure(figure_name)
plot_speed_up(y1,y2,y3,y4,y5,y6,y7,True)
plt.title('speed up ({} iterations)'.format(high_niter))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#efficiency
figure_name = 'ef_particles_for_high_niter'
plt.figure(figure_name)
plot_efficiency(y1,y2,y3,y4,y5,y6,True)
plt.title('efficiency ({} iterations)'.format(high_niter))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

###############################
# NITER (few particles)
###############################
fin = open('./data/niter_for_few_particles.txt','r')
lines = fin.readlines()
fin.close()
tokens_list = [line.split(';') for line in lines]

# completion time
figure_name = 'ct_niter_for_few_particles'
plt.figure(figure_name)
y1,y2,y3,y4,y5,y6,y7 = plot_completion_time(tokens_list,False)
plt.title('completion time ({} particles)'.format(few_particles))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#speed up
figure_name = 'su_niter_for_few_particles'
plt.figure(figure_name)
plot_speed_up(y1,y2,y3,y4,y5,y6,y7,False)
plt.title('speed up ({} particles)'.format(few_particles))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#efficiency
figure_name = 'ef_niter_for_few_particles'
plt.figure(figure_name)
plot_efficiency(y1,y2,y3,y4,y5,y6,False)
plt.title('efficiency ({} particles)'.format(few_particles))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

###############################
# NITER (many particles)
###############################
fin = open('./data/niter_for_many_particles.txt','r')
lines = fin.readlines()
fin.close()
tokens_list = [line.split(';') for line in lines]

# completion time
figure_name = 'ct_niter_for_many_particles'
plt.figure(figure_name)
y1,y2,y3,y4,y5,y6,y7 = plot_completion_time(tokens_list,False)
plt.title('completion time ({} particles)'.format(many_particles))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#speed up
figure_name = 'su_niter_for_many_particles'
plt.figure(figure_name)
plot_speed_up(y1,y2,y3,y4,y5,y6,y7,False)
plt.title('speed up ({} particles)'.format(many_particles))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#efficiency
figure_name = 'ef_niter_for_many_particles'
plt.figure(figure_name)
plot_efficiency(y1,y2,y3,y4,y5,y6,False)
plt.title('efficiency ({} particles)'.format(many_particles))
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)