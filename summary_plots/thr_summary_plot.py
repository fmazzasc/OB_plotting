import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib

# matplotlib.use('pdf')
matplotlib.style.use('seaborn')

with open("../../ciao/thr_summary.yaml", 'r') as stream:
    dic = yaml.load(stream)


staves = list(dic.keys())[:-1]

mean_thr = []
std_thr = []
dispersion_mean = []
dispersion_std = []

for stave in staves:
    mean_arr = np.array(dic[stave]['mean'])
    std_arr = np.array(dic[stave]['std'])
    mask = mean_arr > 0
    mean_thr.append(np.mean(mean_arr[mask]))
    dispersion_mean.append((np.max(mean_arr[mask]) - np.min(mean_arr[mask]))/2)
    std_thr.append(np.mean(std_arr[mask]))
    dispersion_std.append((np.max(std_arr[mask]) - np.min(std_arr[mask]))/2)


fig, ax = plt.subplots(figsize=(16,6))

ax.errorbar(staves, mean_thr, dispersion_mean, fmt = '.', color = 'b', markersize = 8)
plt.xticks(range(len(staves)), staves, rotation=90)
plt.tick_params(axis='x', which='major', labelsize=13)



loc = plticker.MultipleLocator(base=2.0) # this locator puts ticks at regular intervals
ax.xaxis.set_major_locator(loc)

plt.ylim((60,130))
plt.xlim((-1,len(staves)+1))
plt.ylabel('Average Threshold (electrons)', fontsize = 20   )
plt.text( 10, 70, 'Outer Barrel', fontsize = 25, color = 'b')
plt.tight_layout()
plt.savefig('thr_aver.png')
# plt.show()



fig, ax = plt.subplots(figsize=(14,6))
ax.errorbar(staves, std_thr, dispersion_std, fmt = '.', color = 'b', markersize = 8)
plt.xticks(range(len(staves)), staves, rotation=90)
plt.tick_params(axis='x', which='major', labelsize=13)


loc = plticker.MultipleLocator(base=2.0) # this locator puts ticks at regular intervals
ax.xaxis.set_major_locator(loc)


plt.ylabel('Threshold RMS (electrons)', fontsize = 20)
plt.text( 4, 35, 'Outer Barrel', fontsize = 25, color = 'b')
plt.tight_layout()
plt.savefig('thr_std.png')
plt.show()