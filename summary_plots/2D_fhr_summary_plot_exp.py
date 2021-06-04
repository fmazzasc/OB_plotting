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

mode_comparison = False

matplotlib.use("pdf")
from matplotlib.ticker import FormatStrFormatter


with open("../summary_data/fhr_summary.yaml", 'r') as stream:
    dic = yaml.full_load(stream)

with open("../summary_data/fhr_masked_2_summary.yaml", 'r') as stream:
    dic_masked = yaml.full_load(stream)


staves = list(dic.keys())[:-1]


test_type = ['tuned_fhr', 'tuned_fhr_masked']
output_string = [r'$\bf{FHR \: w/o \: masking}$: preliminary charge threshold tuning to 100e$^{-}$', r'$\bf{FHR \: w/ \: masking}$: preliminary charge threshold tuning to 100e$^{-}$']




for test,output in zip(test_type, output_string):
    fhr_array = np.array([])
    fhr_array_aver = np.array([])
    stave_array = np.array([])
    weigths_array = np.array([])
    
    for i,stave in enumerate(staves):

        if test == "tuned_fhr":
            mean_arr = np.unique(np.array(dic[stave]['mean'][test]))
        else:
            mean_arr = np.unique(np.array(dic_masked[stave]['mean']))

        mask1 = mean_arr > 0
        fhr_array = np.append(fhr_array, mean_arr[mask1], axis=0)
        fhr_array_aver = np.append(fhr_array_aver, [np.mean(mean_arr[mask1])], axis=0)

        temp_arr = (i+0.5)*np.ones(len(mean_arr[mask1]))
        weigths_array = np.append(weigths_array, (1/len(mean_arr[mask1]))*np.ones(len(mean_arr[mask1])))


        stave_array = np.append(stave_array, temp_arr, axis = 0)

        # print(stave_array)

    # fhr_array = np.power(10,fhr_array_log_aver)
    mean = np.mean(fhr_array_aver)
    std = np.std(fhr_array_aver)
    print("Average:", mean, " RMS: ", std)


    x_bins = np.arange(0, len(staves))
    lim_sup = 5e-4 if test=="tuned_fhr" or mode_comparison==True else 8e-10
    y_bins = np.geomspace(10**(-12), lim_sup)
    # h.fill(stave_array, fhr_array_log)

    # print(y_bins)
    w, x_bins, y_bins = np.histogram2d(stave_array, fhr_array, weights=weigths_array, bins=(x_bins, y_bins))

    fig, ax = plt.subplots(figsize=(20, 5))
    
    w[w==0] = np.nan
    # print(w)
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("white")
    mesh = ax.pcolormesh(x_bins, y_bins, w.T, cmap = cmap, rasterized=True)
    ax.set_xticks(range(len(staves)))
    ax.set_ylabel('Fake Hit Rate (hits/event/pixel)', fontsize=24, loc="center")
    ax.set_xlabel('Stave ID', fontsize=26, loc="center")
    loc = plticker.MultipleLocator(base=10.0) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)

    ax.tick_params(axis='y', which='major', labelsize=18)
    ax.tick_params(axis='x', which='major', labelsize=18)

    bar = fig.colorbar(mesh, pad=0.02)
    bar.set_label("Fraction of runs", fontsize=24, rotation=270, labelpad=45, y=0.2)
    bar.ax.tick_params(labelsize=18)
    

    text_sup = 4e-5 if test=="tuned_fhr" or mode_comparison==True else 3.5e-10

    plt.text(5, text_sup, r'$\bf{ITS \: Outer \: Barrel}$: 192 staves, 12.4 x $10^{9}$ pixels           ' + f"{output}", fontsize = 20)
    # plt.text( 10, text_sup - 5, f'Outer Barrel: ', fontsize = 20)

    if test!="tuned_fhr":
        round_app = 9 if test=="tuned_fhr" else 12
        exponent = 11
        exp_mean = np.round(mean*10**11,2)
        exp_std  = np.round(np.std(fhr_array_aver*10**(11)),2)
        exp_str = r"$\bf{Average}$: " + f"{exp_mean:.2}" + r" x $10^{{-11}}$, $\bf{RMS}$:" + f" {exp_std:.2} x $10^{{-11}}$ (hits/event/pixel)"
        plt.plot([0, np.max(stave_array)], [mean, mean], '--', color="red",  label=exp_str, linewidth=2)
        round_app = 8 if test=="tuned_fhr" else 12
        # plt.plot([0, np.max(stave_array)], [np.max(fhr_array_log), np.max(fhr_array_log)], 'r--', label=f"Maximum FHR: {np.round(10**11*np.power(10,np.max(fhr_array_log)), 1)} x $10^{{-11}}$ hits/event/pixel", linewidth=2)
    else:
        round_app = 9
        exp_mean = np.round(mean*10**8,2)
        exp_std  = np.round(np.std(fhr_array_aver)*10**8,2)
        exp_str = r"$\bf{Average}$: " + f"{exp_mean:.2}" + r" x $10^{{-8}}$, $\bf{RMS}$:" + f" {exp_std:.3} x $10^{{-8}}$ (hits/event/pixel)"
        # print(exp_str)
        plt.plot([0, np.max(stave_array)], [mean, mean], 'r--', label=exp_str, linewidth=2)
        # plt.plot([0, np.max(stave_array)], [ np.max(fhr_array_log), np.max(fhr_array_log)], 'r--', label=f"Maximum FHR: {np.round(10**7*np.power(10,np.max(fhr_array_log)), 1)} x $10^{{-7}}$ hits/event/pixel", linewidth=2)        
    leg = plt.legend(fontsize = 20, loc = "center left", bbox_to_anchor=(0.02, 0.79))
    # plt.setp(leg.get_texts(), color='r')


    plt.xlim((0, np.max(stave_array)-0.5))
    ax.set_yscale("log")
    y_major = matplotlib.ticker.LogLocator(base = 10.0, numticks = 10)
    ax.yaxis.set_major_locator(y_major)
    y_minor = matplotlib.ticker.LogLocator(base = 10.0, subs = np.arange(1.0, 10.0) * 0.1, numticks = 10)
    ax.yaxis.set_minor_locator(y_minor)
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

    ax.tick_params(axis='y', which='minor', length=5)
    ax.tick_params(axis='x', which='minor', length=5)

    if test=="tuned_fhr" or mode_comparison==True:
        for label in ax.yaxis.get_ticklabels()[::2]:
            label.set_visible(False)

    for label in ax.xaxis.get_ticklabels()[::2]:
        label.set_visible(False)


    plt.tight_layout()

    plt.savefig(f'../results/2D_{test}.png', bbox_inches = 'tight', pad_inches = 0.2)
    plt.savefig(f'../results/2D_{test}.pdf', pad_inches = 0.2, bbox_inches = 'tight')

