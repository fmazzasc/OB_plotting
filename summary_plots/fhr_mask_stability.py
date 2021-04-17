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

with open("../summary_data/fhr_masked_summary.yaml", 'r') as stream:
    dic_masked = yaml.load(stream)


staves = list(dic_masked.keys())[:-1]


fhr_array_log_aver = np.array([])
fhr_array_log_aver_masked = np.array([])


for i,stave in enumerate(staves):
    mean_arr_masked = np.array(dic_masked[stave]['mean'])
    mask_filter = mean_arr_masked > 0
    fhr_array_log_aver_masked = np.append(fhr_array_log_aver_masked, [np.log10(np.mean(mean_arr_masked[mask_filter]))], axis=0)

mean_masked = np.mean(np.power(10,fhr_array_log_aver_masked))
std_masked = np.std(np.power(10,fhr_array_log_aver_masked))/np.sqrt(len(fhr_array_log_aver_masked))

########read dat files with mask stability fhrs
x = np.loadtxt("../summary_data/summary_fhr_mask_stab.dat", usecols=(3,4)) # mask only common pixel, mask pixel common in 80% of the runs
common_masking_fhr = x[:,0]
common_80_masking_fhr = x[:,1]
mean_common_masking = np.mean(common_masking_fhr)
mean_common_80_masking = np.mean(common_80_masking_fhr)
std_common_masking = np.std(common_masking_fhr)
std_common_80_masking = np.std(common_80_masking_fhr)
#############################################àà


h_distr_masked = Hist(
    hist.axis.Regular(
        20, -11, -8, name="", label="FHR w/ masking", underflow=False, overflow=False
    )
)

h_distr_common_masking = Hist(
    hist.axis.Regular(
        20, -11, -8, name="", label="FHR w/ common masking", underflow=False, overflow=False
    )
)

h_distr_common_80_masking = Hist(
    hist.axis.Regular(
        20, -11, -8, name="", label="FHR w/ common 80% masking", underflow=False, overflow=False
    )
)

h_distr_masked.fill(fhr_array_log_aver_masked)
h_distr_common_masking.fill(np.log10(common_masking_fhr))
h_distr_common_80_masking.fill(np.log10(common_80_masking_fhr))



plt.figure()
fig, ax = plt.subplots(figsize=(12, 12))

mplhep.histplot(h_distr_masked, ax=ax, yerr=False,histtype="fill", alpha=0.5, color="blue", label="Full software masking")
mplhep.histplot(h_distr_common_80_masking, ax=ax, yerr=False,histtype="fill", alpha=0.5, color="green", label="Mask bad pixel common to at least 80% of runs")
mplhep.histplot(h_distr_common_masking, ax=ax, yerr=False,histtype="fill", alpha=0.5, color="red", label="Mask bad pixel common to all runs")

# mplhep.histplot(h_distr_masked, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="blue", linewidth=3)
# mplhep.histplot(h_distr_common_masking, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="red", linewidth=3)
# mplhep.histplot(h_distr_common_80_masking, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="green", linewidth=3)



text_y = 80
# ax.text(text_x, text_y, f'Outer Barrel', color="black", fontsize=40, fontweight="bold")
exp_str1 = f'Average FHR : {mean_masked*10**11:.2} x $10^{{-11}}$'
exp_str2 = f'Average FHR : {mean_common_80_masking*10**10:.2} x $10^{{-10}}$'
exp_str3 = f'Average FHR : {mean_common_masking*10**9:.2} x $10^{{-9}}$'
ax.text(-10.6, text_y - 45, exp_str1, color="blue", fontsize=22)
ax.text(-10.6, text_y - 53, exp_str2, color="green", fontsize=22)
ax.text(-10.6, text_y - 59, exp_str3, color="red", fontsize=22)


ax.legend(loc = "upper center", fontsize=22, bbox_to_anchor=(0.55,0.94))
plt.xlabel("Average FHR (log)")
plt.ylabel("Counts")
plt.yscale("log")
plt.savefig(f'../results/mask_stability.png')
plt.savefig(f'../results/mask_stability.pdf')
plt.close()