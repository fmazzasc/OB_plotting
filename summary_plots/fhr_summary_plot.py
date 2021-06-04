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
    dic = yaml.full_load(stream)

with open("../summary_data/fhr_masked_2_summary.yaml", 'r') as stream:
    dic_masked = yaml.full_load(stream)


staves = list(dic.keys())[:-1]

output_string = ['Tuned FHR w/o masking', 'Tuned FHR w/ masking']




fhr_array_aver = np.array([])
fhr_array_aver_masked = np.array([])


for i,stave in enumerate(staves):

    mean_arr = np.array(dic[stave]['mean']["tuned_fhr"])
    mean_arr_masked = np.array(dic_masked[stave]['mean'])

    filter_1 = mean_arr > 0
    filter_2 = mean_arr_masked > 0
    fhr_array_aver = np.append(fhr_array_aver, [np.mean(mean_arr[filter_1])], axis=0)
    fhr_array_aver_masked = np.append(fhr_array_aver_masked, [np.mean(mean_arr_masked[filter_2])], axis=0)


mean = np.mean(fhr_array_aver)
std = np.std(fhr_array_aver)
mean_masked = np.mean(fhr_array_aver_masked)
std_masked = np.std(fhr_array_aver_masked)

bins = np.geomspace(1e-11, 5e-5, 20)
h_distr = np.histogram(fhr_array_aver, bins=bins)
h_distr_masked = np.histogram(fhr_array_aver_masked, bins=bins)


plt.figure()
fig, ax = plt.subplots(figsize=(12, 12))

mplhep.histplot(h_distr, ax=ax, yerr=False,histtype="fill", alpha=0.5, color="red", label="FHR w/o masking")
mplhep.histplot(h_distr, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="red", linewidth=3)
mplhep.histplot(h_distr_masked, ax=ax, yerr=False,histtype="fill", alpha=0.5, color="blue", label="FHR w/ offline masking")
mplhep.histplot(h_distr_masked, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="blue", linewidth=3)
text_x = 3e-11
text_y = 83
ax.text(text_x, text_y, f'Outer Barrel', color="black", fontsize=35, fontweight="bold")
exp_mean = np.round(mean*10**8,2)
exp_std = np.round(std*10**8,2)
exp_mean_masked = np.round(mean_masked*10**11,2)
exp_std_masked = np.round(std_masked*10**11,2)

exp_str1 = f'Average: {exp_mean:.2} x $10^{{-8}}$, RMS: {exp_std:.3} x $10^{{-8}}$'
exp_str2 = f'Average: {exp_mean_masked:.2} x $10^{{-11}}$, RMS: {exp_std_masked:.2} x $10^{{-11}}$'
ax.text(text_x + 1e-10 , text_y - 35, exp_str1, color="red", fontsize=24)
ax.text(text_x + 1e-10 , text_y - 45, exp_str2, color="blue", fontsize=24)

ax.legend()

ax.tick_params(axis='x', which='major', pad=10)
plt.xlabel("Fake Hit Rate (hits/event/pixel)")
plt.ylabel("Counts")
plt.yscale("log")
plt.xscale("log")


plt.savefig(f'../results/distr_comparison.png', bbox_inches = 'tight', pad_inches = 0.2)
plt.savefig(f'../results/distr_comparison.pdf', pad_inches = 0.2, bbox_inches = 'tight')
plt.close()