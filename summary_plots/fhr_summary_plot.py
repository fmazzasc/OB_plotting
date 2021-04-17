import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib
from hist import Hist
import hist
import mplhep
matplotlib.style.use(mplhep.style.ALICE)
# Quick construction, no other imports needed:
matplotlib.use("pdf")
from matplotlib.ticker import FormatStrFormatter


with open("../summary_data/fhr_summary.yaml", 'r') as stream:
    dic = yaml.load(stream)

with open("../summary_data/fhr_masked_summary.yaml", 'r') as stream:
    dic_masked = yaml.load(stream)


staves = list(dic.keys())[:-1]

output_string = ['Tuned FHR w/o masking', 'Tuned FHR w/ masking']




fhr_array_log_aver = np.array([])
fhr_array_log_aver_masked = np.array([])


for i,stave in enumerate(staves):

    mean_arr = np.array(dic[stave]['mean']["tuned_fhr"])
    mean_arr_masked = np.array(dic_masked[stave]['mean'])

    filter_1 = mean_arr > 0
    filter_2 = mean_arr_masked > 0
    fhr_array_log_aver = np.append(fhr_array_log_aver, [np.log10(np.mean(mean_arr[filter_1]))], axis=0)
    fhr_array_log_aver_masked = np.append(fhr_array_log_aver_masked, [np.log10(np.mean(mean_arr_masked[filter_2]))], axis=0)


mean = np.mean(np.power(10,fhr_array_log_aver))
std = np.std(np.power(10,fhr_array_log_aver))/np.sqrt(len(fhr_array_log_aver))
mean_masked = np.mean(np.power(10,fhr_array_log_aver_masked))
std_masked = np.std(np.power(10,fhr_array_log_aver_masked))/np.sqrt(len(fhr_array_log_aver_masked))


h_distr = Hist(
    hist.axis.Regular(
        20, -11, -5.5, name="", label="FHR w/o masking", underflow=False, overflow=False
    )
)

h_distr_masked = Hist(
    hist.axis.Regular(
        20, -11, -5.5, name="", label="FHR w/ masking", underflow=False, overflow=False
    )
)

h_distr.fill(fhr_array_log_aver)
h_distr_masked.fill(fhr_array_log_aver_masked)


plt.figure()
fig, ax = plt.subplots(figsize=(12, 12))

mplhep.histplot(h_distr, ax=ax, yerr=False,histtype="fill", alpha=0.5, color="red", label="FHR w/o masking")
mplhep.histplot(h_distr, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="red", linewidth=3)
mplhep.histplot(h_distr_masked, ax=ax, yerr=False,histtype="fill", alpha=0.5, color="blue", label="FHR w/ masking")
mplhep.histplot(h_distr_masked, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="blue", linewidth=3)
text_x = -10.4
text_y = 100
ax.text(text_x, text_y, f'Outer Barrel', color="black", fontsize=40, fontweight="bold")
exp_str1 = f'Average FHR w/o masking : ({np.round(mean*10**8,0)} $\pm$ {np.round(std*10**8,0)}) x $10^{{-8}}$'
exp_str2 = f'Average FHR w/ masking : ({mean_masked*10**11:.4} $\pm$ {std_masked*10**11:.1}) x $10^{{-11}}$'
ax.text(text_x + 0.7, text_y - 45, exp_str1, color="red", fontsize=20)
ax.text(text_x + 0.7, text_y - 55, exp_str2, color="blue", fontsize=20)

ax.legend()
plt.xlabel("Average FHR (log)")
plt.ylabel("Counts")
plt.yscale("log")
plt.savefig(f'distr_comparison.png')
plt.savefig(f'distr_comparison.pdf')
plt.close()