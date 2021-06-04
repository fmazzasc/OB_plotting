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

###read full masked data  

with open("../summary_data/fhr_summary.yaml", 'r') as stream:
    dic = yaml.full_load(stream)

with open("../summary_data/fhr_masked_2_summary.yaml", 'r') as stream:
    dic_masked = yaml.full_load(stream)


staves = list(dic_masked.keys())[:-1]


fhr_array_aver = np.array([])
fhr_array_aver_masked = np.array([])


for i,stave in enumerate(staves):
    mean_arr = np.array(dic[stave]['mean']["tuned_fhr"])
    mean_arr_masked = np.array(dic_masked[stave]['mean'])
    filter_1 = mean_arr > 0
    mask_filter = mean_arr_masked > 0
    fhr_array_aver = np.append(fhr_array_aver, [np.mean(mean_arr[filter_1])], axis=0)
    fhr_array_aver_masked = np.append(fhr_array_aver_masked, [np.mean(mean_arr_masked[mask_filter])], axis=0)


mean_masked = np.mean(fhr_array_aver_masked)
std_masked = np.std(fhr_array_aver_masked)/np.sqrt(len(fhr_array_aver_masked))

########read dat files with mask stability fhrs
x = np.loadtxt("../summary_data/summary_fhr_mask_stab_5e05.dat", usecols=(3,4,5)) # mask only common pixel, mask pixel common in 80% of the runs
common_masking_fhr = x[:,0]
common_80_masking_fhr = x[:,1]
common_20_masking_fhr = x[:,2]
mean_common_masking = np.mean(common_masking_fhr)
mean_common_80_masking = np.mean(common_80_masking_fhr)
mean_common_20_masking = np.mean(common_20_masking_fhr)
std_common_masking = np.std(common_masking_fhr)
std_common_20_masking = np.std(common_20_masking_fhr)
#############################################àà


bins = np.geomspace(1e-11, 1e-6, 20)

h_distr = np.histogram(fhr_array_aver, bins=bins)
h_distr_masked = np.histogram(fhr_array_aver_masked, bins=bins)
h_distr_common_masking = np.histogram(common_masking_fhr, bins=bins)
h_distr_common_80_masking = np.histogram(common_80_masking_fhr, bins=bins)
h_distr_common_20_masking = np.histogram(common_20_masking_fhr, bins=bins)




plt.figure()
fig, ax = plt.subplots(figsize=(12, 12))

mplhep.histplot(h_distr, ax=ax, yerr=False,histtype="fill", linewidth=2, alpha=0.2, color="grey", label="No masking")
mplhep.histplot(h_distr_masked, ax=ax, yerr=False,histtype="fill", linewidth=2, alpha=0.1, color="blue", label="Full software masking")
mplhep.histplot(h_distr_common_80_masking, ax=ax, yerr=False,histtype="step", linewidth=2, alpha=1, color="green", label="Mask bad pixel common to at least 80% of runs")
mplhep.histplot(h_distr_common_20_masking, ax=ax, yerr=False,histtype="step", linewidth=2, alpha=1, color="red", label="Mask bad pixel common to at least 20% of runs")
mplhep.histplot(h_distr_common_masking, ax=ax, yerr=False,histtype="step", linewidth=2,  alpha=1, color="orange", label="Mask bad pixel common to all runs")

# mplhep.histplot(h_distr_masked, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="blue", linewidth=3)
# mplhep.histplot(h_distr_common_masking, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="red", linewidth=3)
# mplhep.histplot(h_distr_common_80_masking, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="green", linewidth=3)


text_x = 2.2e-10
text_y = 72
ax.text(text_x, text_y, f'ITS Outer Barrel', color="black", fontsize=40, fontweight="bold")
ax.text(text_x, text_y - 10, 'Max sample: 20 runs/stave', color="black", fontsize=20, fontstyle="italic")

exp_str1 = f'Average FHR : {mean_masked*10**11:.2} x $10^{{-11}}$ hits/event/pixel'
exp_str2 = f'Average FHR : {mean_common_80_masking*10**10:.2} x $10^{{-10}}$ hits/event/pixel'
exp_str3 = f'Average FHR : {mean_common_masking*10**9:.2} x $10^{{-9}}$ hits/event/pixel'
# ax.text(text_x, text_y - 45, exp_str1, color="blue", fontsize=22)
# ax.text(text_x, text_y - 53, exp_str2, color="green", fontsize=22)
# ax.text(text_x, text_y - 59, exp_str3, color="red", fontsize=22)


ax.legend(loc = "lower left", bbox_to_anchor=(0.27, 0.67), fontsize=18)
plt.xlabel("Fake Hit Rate (hits/event/pixel)")
plt.ylabel("Counts")
plt.yscale("log")
plt.xscale("log")

ax.tick_params(axis='x', which='major', pad=10)


plt.savefig(f'../results/mask_stability.png', bbox_inches = 'tight',
    pad_inches = 0.2)
plt.savefig(f'../results/mask_stability.pdf', bbox_inches = 'tight',
    pad_inches = 0.2)
plt.close()