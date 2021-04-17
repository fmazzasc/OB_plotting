import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib
from hist import Hist
import hist
import mplhep

matplotlib.style.use(mplhep.style.ALICE)
matplotlib.use("pdf")
# Quick construction, no other imports needed:


with open("../summary_data/thr_summary.yaml", 'r') as stream:
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
mesh = ax.pcolormesh(x, y, w.T, cmap = 'viridis', rasterized=True)
ax.set_xticks(range(len(staves)))
ax.set_xticklabels(staves)
ax.set_xticklabels(staves, rotation='vertical', fontsize=13)
ax.set_ylabel('Average Threshold Scan (electrons)', fontsize=18)
loc = plticker.MultipleLocator(base=3.0) # this locator puts ticks at regular intervals
ax.xaxis.set_major_locator(loc)
ax.set_xticklabels(staves)
ax.set_xticklabels(staves, rotation='vertical', fontsize=13)
ax.tick_params(axis='y', which='major', labelsize=16)
fig.colorbar(mesh)

plt.text( 70, 110, f'Outer Barrel: Threshold Scan', fontsize = 20, color = 'white')




plt.plot([0, np.max(stave_array)], [np.mean(thr_array), np.mean(thr_array)], 'w--', label = f"Average Threshold: {np.round(mean,2)} $\pm$ {np.round(np.std(thr_array)/np.sqrt(len(thr_array)),2)}")
leg = plt.legend(fontsize=20,loc='upper right', bbox_to_anchor=(0.84, 0.88))
plt.setp(leg.get_texts(), color='w')

plt.xlim((0, np.max(stave_array)-0.5))

plt.tight_layout()
plt.savefig(f'../results/2D_thr.png')
plt.savefig(f'../results/2D_thr.pdf')
plt.show()