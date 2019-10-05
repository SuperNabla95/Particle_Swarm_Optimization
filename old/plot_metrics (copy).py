import os
import matplotlib.pyplot as plt
from matplotlib import cm
import statistics as stats
from scipy.signal import lfilter


cmap = cm.get_cmap('cool',4)
dashes = [6,2,2,2]

nt_max = 4
nts = [nt for nt in range(1,nt_max+1)]

low_niter = 10
high_niter = 80
sample_niter = [10,20,40,80]

few_particles = 1000
many_particles = 64000
sample_particles = [1000,4000,16000,64000]

labels_particle = ['{} particles'.format(particles) for particles in sample_particles]
labels_niter = ['{} iterations'.format(it) for it in sample_niter]


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

ydata_mt0 = [float(tokens[0]) for tokens in tokens_list]
ydata_ff0 = [float(tokens[1]) for tokens in tokens_list]
ydata_mt1 = [float(tokens[2]) for tokens in tokens_list]
ydata_ff1 = [float(tokens[3]) for tokens in tokens_list]
ydata_mt2 = [float(tokens[4]) for tokens in tokens_list]
ydata_ff2 = [float(tokens[5]) for tokens in tokens_list]
ydata_mt3 = [float(tokens[6]) for tokens in tokens_list]
ydata_ff3 = [float(tokens[7]) for tokens in tokens_list]

seq = [ydata_mt0[0], ydata_mt1[0], ydata_mt2[0], ydata_mt3[0]]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_particle[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_particle[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_particle[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_particle[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('completion time ({} iterations)'.format(low_niter))
plt.legend(loc='upper right')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#speed up
figure_name = 'su_particles_for_low_niter'
plt.figure(figure_name)

ydata_mt0 = [seq[0]/y for y in ydata_mt0]
ydata_ff0 = [seq[0]/y for y in ydata_ff0]
ydata_mt1 = [seq[1]/y for y in ydata_mt1]
ydata_ff1 = [seq[1]/y for y in ydata_ff1]
ydata_mt2 = [seq[2]/y for y in ydata_mt2]
ydata_ff2 = [seq[2]/y for y in ydata_ff2]
ydata_mt3 = [seq[3]/y for y in ydata_mt3]
ydata_ff3 = [seq[3]/y for y in ydata_ff3]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_particle[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_particle[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_particle[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_particle[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('speed up ({} iterations)'.format(low_niter))
plt.legend(loc='upper left')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#efficiency
figure_name = 'ef_particles_for_low_niter'
plt.figure(figure_name)

ydata_mt0 = [i / j for i, j in zip(ydata_mt0, nts)]
ydata_ff0 = [i / j for i, j in zip(ydata_ff0, nts)]
ydata_mt1 = [i / j for i, j in zip(ydata_mt1, nts)]
ydata_ff1 = [i / j for i, j in zip(ydata_ff1, nts)]
ydata_mt2 = [i / j for i, j in zip(ydata_mt2, nts)]
ydata_ff2 = [i / j for i, j in zip(ydata_ff2, nts)]
ydata_mt3 = [i / j for i, j in zip(ydata_mt3, nts)]
ydata_ff3 = [i / j for i, j in zip(ydata_ff3, nts)]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_particle[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_particle[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_particle[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_particle[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('efficiency ({} iterations)'.format(low_niter))
plt.legend(loc='upper right')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)


###############################
# PARTICLES (high niter)
###############################

fin = open('./data/particles_for_high_niter.txt','r')
lines = fin.readlines()
fin.close()
tokens_list = [line.split(';') for line in lines]

#completion time
figure_name = 'ct_particles_for_high_niter'
plt.figure(figure_name)

ydata_mt0 = [float(tokens[0]) for tokens in tokens_list]
ydata_ff0 = [float(tokens[1]) for tokens in tokens_list]
ydata_mt1 = [float(tokens[2]) for tokens in tokens_list]
ydata_ff1 = [float(tokens[3]) for tokens in tokens_list]
ydata_mt2 = [float(tokens[4]) for tokens in tokens_list]
ydata_ff2 = [float(tokens[5]) for tokens in tokens_list]
ydata_mt3 = [float(tokens[6]) for tokens in tokens_list]
ydata_ff3 = [float(tokens[7]) for tokens in tokens_list]

seq = [ydata_mt0[0], ydata_mt1[0], ydata_mt2[0], ydata_mt3[0]]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_particle[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_particle[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_particle[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_particle[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('completion time ({} iterations)'.format(high_niter))
plt.legend(loc='upper right')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#speed up
figure_name = 'su_particles_for_high_niter'
plt.figure(figure_name)

ydata_mt0 = [seq[0]/y for y in ydata_mt0]
ydata_ff0 = [seq[0]/y for y in ydata_ff0]
ydata_mt1 = [seq[1]/y for y in ydata_mt1]
ydata_ff1 = [seq[1]/y for y in ydata_ff1]
ydata_mt2 = [seq[2]/y for y in ydata_mt2]
ydata_ff2 = [seq[2]/y for y in ydata_ff2]
ydata_mt3 = [seq[3]/y for y in ydata_mt3]
ydata_ff3 = [seq[3]/y for y in ydata_ff3]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_particle[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_particle[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_particle[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_particle[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('speed up ({} iterations)'.format(high_niter))
plt.legend(loc='upper left')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#efficiency
figure_name = 'ef_particles_for_high_niter'
plt.figure(figure_name)

ydata_mt0 = [i / j for i, j in zip(ydata_mt0, nts)]
ydata_ff0 = [i / j for i, j in zip(ydata_ff0, nts)]
ydata_mt1 = [i / j for i, j in zip(ydata_mt1, nts)]
ydata_ff1 = [i / j for i, j in zip(ydata_ff1, nts)]
ydata_mt2 = [i / j for i, j in zip(ydata_mt2, nts)]
ydata_ff2 = [i / j for i, j in zip(ydata_ff2, nts)]
ydata_mt3 = [i / j for i, j in zip(ydata_mt3, nts)]
ydata_ff3 = [i / j for i, j in zip(ydata_ff3, nts)]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_particle[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_particle[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_particle[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_particle[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('efficiency ({} iterations)'.format(high_niter))
plt.legend(loc='upper right')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

###############################
# NITER (few particles)
###############################
fin = open('./data/niter_for_few_particles.txt','r')
lines = fin.readlines()
fin.close()
tokens_list = [line.split(';') for line in lines]

#completion time
figure_name = 'ct_niter_niter_for_few_particles'
plt.figure(figure_name)

ydata_mt0 = [float(tokens[0]) for tokens in tokens_list]
ydata_ff0 = [float(tokens[1]) for tokens in tokens_list]
ydata_mt1 = [float(tokens[2]) for tokens in tokens_list]
ydata_ff1 = [float(tokens[3]) for tokens in tokens_list]
ydata_mt2 = [float(tokens[4]) for tokens in tokens_list]
ydata_ff2 = [float(tokens[5]) for tokens in tokens_list]
ydata_mt3 = [float(tokens[6]) for tokens in tokens_list]
ydata_ff3 = [float(tokens[7]) for tokens in tokens_list]

seq = [ydata_mt0[0], ydata_mt1[0], ydata_mt2[0], ydata_mt3[0]]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_niter[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_niter[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_niter[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_niter[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('completion time ({} particles)'.format(few_particles))
plt.legend(loc='upper right')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#speed up
figure_name = 'su_niter_niter_for_few_particles'
plt.figure(figure_name)

ydata_mt0 = [seq[0]/y for y in ydata_mt0]
ydata_ff0 = [seq[0]/y for y in ydata_ff0]
ydata_mt1 = [seq[1]/y for y in ydata_mt1]
ydata_ff1 = [seq[1]/y for y in ydata_ff1]
ydata_mt2 = [seq[2]/y for y in ydata_mt2]
ydata_ff2 = [seq[2]/y for y in ydata_ff2]
ydata_mt3 = [seq[3]/y for y in ydata_mt3]
ydata_ff3 = [seq[3]/y for y in ydata_ff3]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_niter[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_niter[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_niter[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_niter[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('speed up ({} particles)'.format(few_particles))
plt.legend(loc='upper left')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#efficiency
figure_name = 'ef_niter_niter_for_few_particles'
plt.figure(figure_name)

ydata_mt0 = [i / j for i, j in zip(ydata_mt0, nts)]
ydata_ff0 = [i / j for i, j in zip(ydata_ff0, nts)]
ydata_mt1 = [i / j for i, j in zip(ydata_mt1, nts)]
ydata_ff1 = [i / j for i, j in zip(ydata_ff1, nts)]
ydata_mt2 = [i / j for i, j in zip(ydata_mt2, nts)]
ydata_ff2 = [i / j for i, j in zip(ydata_ff2, nts)]
ydata_mt3 = [i / j for i, j in zip(ydata_mt3, nts)]
ydata_ff3 = [i / j for i, j in zip(ydata_ff3, nts)]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_niter[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_niter[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_niter[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_niter[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('efficiency ({} particles)'.format(few_particles))
plt.legend(loc='upper right')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

###############################
# NITER (many particles)
###############################
fin = open('./data/niter_for_many_particles.txt','r')
lines = fin.readlines()
fin.close()
tokens_list = [line.split(';') for line in lines]

#completion time
figure_name = 'ct_niter_niter_for_many_particles'
plt.figure(figure_name)

ydata_mt0 = [float(tokens[0]) for tokens in tokens_list]
ydata_ff0 = [float(tokens[1]) for tokens in tokens_list]
ydata_mt1 = [float(tokens[2]) for tokens in tokens_list]
ydata_ff1 = [float(tokens[3]) for tokens in tokens_list]
ydata_mt2 = [float(tokens[4]) for tokens in tokens_list]
ydata_ff2 = [float(tokens[5]) for tokens in tokens_list]
ydata_mt3 = [float(tokens[6]) for tokens in tokens_list]
ydata_ff3 = [float(tokens[7]) for tokens in tokens_list]

seq = [ydata_mt0[0], ydata_mt1[0], ydata_mt2[0], ydata_mt3[0]]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_niter[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_niter[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_niter[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_niter[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('completion time ({} particles)'.format(many_particles))
plt.legend(loc='upper right')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#speed up
figure_name = 'su_niter_niter_for_many_particles'
plt.figure(figure_name)

ydata_mt0 = [seq[0]/y for y in ydata_mt0]
ydata_ff0 = [seq[0]/y for y in ydata_ff0]
ydata_mt1 = [seq[1]/y for y in ydata_mt1]
ydata_ff1 = [seq[1]/y for y in ydata_ff1]
ydata_mt2 = [seq[2]/y for y in ydata_mt2]
ydata_ff2 = [seq[2]/y for y in ydata_ff2]
ydata_mt3 = [seq[3]/y for y in ydata_mt3]
ydata_ff3 = [seq[3]/y for y in ydata_ff3]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_niter[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_niter[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_niter[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_niter[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('speed up ({} particles)'.format(many_particles))
plt.legend(loc='upper left')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)

#efficiency
figure_name = 'ef_niter_niter_for_many_particles'
plt.figure(figure_name)

ydata_mt0 = [i / j for i, j in zip(ydata_mt0, nts)]
ydata_ff0 = [i / j for i, j in zip(ydata_ff0, nts)]
ydata_mt1 = [i / j for i, j in zip(ydata_mt1, nts)]
ydata_ff1 = [i / j for i, j in zip(ydata_ff1, nts)]
ydata_mt2 = [i / j for i, j in zip(ydata_mt2, nts)]
ydata_ff2 = [i / j for i, j in zip(ydata_ff2, nts)]
ydata_mt3 = [i / j for i, j in zip(ydata_mt3, nts)]
ydata_ff3 = [i / j for i, j in zip(ydata_ff3, nts)]

plt.plot(nts, ydata_mt0, c=cmap(1/8), label=labels_niter[0])
plt.plot(nts,ydata_ff0, c=cmap(1/8), dashes=dashes)
plt.plot(nts, ydata_mt1, c=cmap(3/8), label=labels_niter[1])
plt.plot(nts,ydata_ff1, c=cmap(3/8), dashes=dashes)
plt.plot(nts, ydata_mt2, c=cmap(5/8), label=labels_niter[2])
plt.plot(nts,ydata_ff2, c=cmap(5/8), dashes=dashes)
plt.plot(nts, ydata_mt3, c=cmap(7/8), label=labels_niter[3])
plt.plot(nts,ydata_ff3, c=cmap(7/8), dashes=dashes)

plt.title('efficiency ({} particles)'.format(many_particles))
plt.legend(loc='upper right')
plt.savefig('./figures/{}.png'.format(figure_name),dpi=200)
print(figure_name)