import numpy as np
import matplotlib.pyplot as plt
import allantools

f_frequ = 'data/201019_2_Frequ.txt'         # Data frequency

# Load files with data
data_frequ = np.genfromtxt(f_frequ,delimiter=(17,2,20,9,9),
dtype='|S17,i2,a25,i2,f8',skip_header=2,skip_footer=1)

data_phase = np.genfromtxt(f_phase,delimiter=(17,2,25,9,9),
dtype='|S17,i2,a25',skip_header=1)

# Arrays for all the data
phase = []
frequ = []

for ii in data_frequ:
    frequ.append(float(ii[2]))

for ii in data_phase:
    phase.append(float(ii[2]))

frequ_arr = np.array(frequ)
phase_arr = np.array(phase)

frequ_ave = np.convolve(frequ_arr, np.ones((5,))/5, mode='valid')
m = np.mean(frequ_arr)
# Some plots

fig = plt.figure(1,figsize=(9,6))
ax = fig.add_subplot(111)
ax.plot(frequ_arr*1e-6,'o',linewidth=2)
ax.plot(frequ_ave*1e-6,'--',linewidth=2)
ax.set_xlabel(r'Time (s)',fontsize=14)
ax.set_ylabel(r'Frequency (MHz)',fontsize=14)
ax.set_ylim((m-5000)*1e-6,(m+5000)*1e-6)
ax.grid(linestyle='--')
fig.tight_layout()
plt.show(block=False)
plt.savefig('figures/frequency_timeline.png')

fig = plt.figure(2,figsize=(9,6))
ax = fig.add_subplot(111)
ax.plot(phase_arr,'o',linewidth=2)
ax.set_xlabel(r'Time (s)',fontsize=14)
ax.set_ylabel(r'$\Phi$ (t)',fontsize=14)
ax.grid(linestyle='--')
fig.tight_layout()
plt.show(block=False)
plt.savefig('figures/phase_timeline.png')


# Playing with allan deviation
y = np.diff(phase_arr)/2/np.pi/m
y_mean = np.diff(phase_arr)/2/np.pi/m
y_inst = np.diff(phase_arr)/2/np.pi/phase_arr[1:]

phase_dev = allantools.adev(y)
phase_dev_mean = allantools.adev(y_mean)
phase_dev_inst = allantools.adev(y_inst)

fig = plt.figure(3,figsize=(9,6))
ax = fig.add_subplot(111)
ax.loglog(phase_dev[0],phase_dev[1],'-o',markersize=8,linewidth=2)
ax.set_xlabel(r'Time (s)',fontsize=14)
ax.set_ylabel(r'$\sigma (\tau)$',fontsize=14)
ax.grid(linestyle='--')
fig.tight_layout()
plt.show(block=False)
