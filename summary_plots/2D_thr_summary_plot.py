import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib
from hist import Hist
import hist

# Quick construction, no other imports needed:


with open("thr_summary.yaml", 'r') as stream:
    dic = yaml.load(stream)


staves = list(dic.keys())[:-1]




thr_array = np.array([])
stave_array = np.array([])

for i,stave in enumerate(staves):
    mean_arr = np.array(dic[stave]['mean'])
    mask1 = mean_arr > 0
    thr_array = np.append(thr_array,mean_arr[mask1], axis=0)
    temp_arr = (i+0.5)*np.ones(len(mean_arr[mask1]))
    stave_array = np.append(stave_array, temp_arr, axis = 0)



h = Hist(
    hist.axis.Regular(
        len(staves), 0, len(staves)-1, name="", label="", underflow=False, overflow=False
    ),
    hist.axis.Regular(
        20, np.min(thr_array), np.max(thr_array), name="Average Fake Hit Rate", label="", underflow=False, overflow=False
    ),
)


mean = np.mean(thr_array)


h.fill(stave_array, thr_array)


fig, ax = plt.subplots(figsize=(20, 6))
w, x, y = h.to_numpy()
mesh = ax.pcolormesh(x, y, w.T, cmap = 'viridis')
ax.set_xticks(range(len(staves)))
ax.set_xticklabels(staves)
ax.set_xticklabels(staves, rotation='vertical', fontsize=13)
ax.set_ylabel('Average Threshold Scan (electrons)', fontsize=18)
loc = plticker.MultipleLocator(base=3.0) # this locator puts ticks at regular intervals
ax.xaxis.set_major_locator(loc)
fig.colorbar(mesh)

plt.text( 80, 110, f'Outer Barrel, Average THR : {np.round(mean, 2)}', fontsize = 20, color = 'white')



plt.plot([0, np.max(stave_array)], [np.mean(thr_array), np.mean(thr_array)], 'w--')
plt.xlim((0, np.max(stave_array)-0.5))

plt.tight_layout()
plt.savefig(f'2D_thr.png')
plt.show()