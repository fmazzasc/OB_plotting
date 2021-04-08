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


with open("../../fhr_summary.yaml", 'r') as stream:
    dic = yaml.load(stream)

with open("../../fhr_masked_summary.yaml", 'r') as stream:
    dic_masked = yaml.load(stream)


staves = list(dic.keys())[:-1]


test_type = ['tuned_fhr', 'tuned_fhr_masked']
output_string = ['Tuned FHR w/o masking', 'Tuned FHR w/ masking']




for test,output in zip(test_type, output_string):
    fhr_array_log = np.array([])
    fhr_array_log_aver = np.array([])
    stave_array = np.array([])
    
    for i,stave in enumerate(staves):

        if test == "tuned_fhr":
            mean_arr = np.array(dic[stave]['mean'][test])
        else:
            mean_arr = np.array(dic_masked[stave]['mean'])

        mask1 = mean_arr > 0
        fhr_array_log = np.append(fhr_array_log, np.log10(mean_arr[mask1]), axis=0)
        fhr_array_log_aver = np.append(fhr_array_log_aver, [np.log10(np.mean(mean_arr[mask1]))], axis=0)

        temp_arr = (i+0.5)*np.ones(len(mean_arr[mask1]))

        stave_array = np.append(stave_array, temp_arr, axis = 0)

    fhr_array = np.power(10,fhr_array_log_aver)
    mean = np.mean(fhr_array)
    std = np.std(fhr_array)
    print("Average:", mean, " RMS: ", std)
    # lim_sup = -4 if test=="tuned_fhr" else -10
    lim_sup=-4

    h = Hist(
        hist.axis.Regular(
            len(staves), 0, len(staves)-1, name="", label="", underflow=False, overflow=False
        ),
        hist.axis.Regular(
            20, -12, lim_sup, name="Average Fake Hit Rate", label="", underflow=False, overflow=False
        ),
    )


    h_distr = Hist(
        hist.axis.Regular(
            30, -11, -5, name="", label="Average FHR", underflow=False, overflow=False
        )
    )



    h.fill(stave_array, fhr_array_log)
    h_distr.fill(fhr_array_log_aver)


    fig, ax = plt.subplots(figsize=(20, 5))
    w, x, y = h.to_numpy()
    mesh = ax.pcolormesh(x, y, w.T, cmap = 'viridis', rasterized=True)
    ax.set_xticks(range(len(staves)))
    ax.set_xticklabels(staves)
    ax.set_xticklabels(staves, rotation='vertical', fontsize=13)
    ax.set_ylabel('Average Fake Hit Rate (log)', fontsize=18)
    loc = plticker.MultipleLocator(base=3.0) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    ax.tick_params(axis='y', which='major', labelsize=16)
    fig.colorbar(mesh)
    # text_sup = -5 if test=="tuned_fhr" else -10.2
    # text_inf = text_sup - 0.7 if test=="tuned_fhr" else text_sup - 0.2
    text_sup = -5
    text_inf = -5 - 0.7

    plt.text( 80, text_sup, f'Outer Barrel: {output}', fontsize = 20, color = 'white')
    if test!="tuned_fhr":
        round_app = 9 if test=="tuned_fhr" else 12
        exponent = 11
        exp_mean = mean*10**11
        exp_std  = np.std(fhr_array)/np.sqrt(len(fhr_array))*10**11
        exp_str = f"Average FHR: ({exp_mean:.4} $\pm$ {exp_std:.1}) x $10^{{-11}}$"
        plt.plot([0, np.max(stave_array)], [np.log10(mean), np.log10(mean)], 'w--', label=exp_str)
        round_app = 8 if test=="tuned_fhr" else 12
        plt.plot([0, np.max(stave_array)], [np.max(fhr_array_log), np.max(fhr_array_log)], 'r--', label=f"Maximum FHR: {np.round(10**11*np.power(10,np.max(fhr_array_log)), 1)} x $10^{{-11}}$")
    else:
        round_app = 9
        exp_mean = mean*10**8
        exp_std  = np.std(fhr_array)/np.sqrt(len(fhr_array))*10**8
        exp_str = f"Average FHR: ({np.round(exp_mean,0)} $\pm$ {np.round(exp_std,0)}) x $10^{{-8}}$"
        plt.plot([0, np.max(stave_array)], [np.log10(mean), np.log10(mean)], 'w--', label=exp_str)
        plt.plot([0, np.max(stave_array)], [ np.max(fhr_array_log), np.max(fhr_array_log)], 'r--', label=f"Maximum FHR: {np.round(10**7*np.power(10,np.max(fhr_array_log)), 1)} x $10^{{-7}}$")        
    leg = plt.legend(fontsize = 20, loc = "upper left")
    plt.setp(leg.get_texts(), color='w')


    plt.xlim((0, np.max(stave_array)-0.5))
    # plt.ylim((-12, -4))
    plt.tight_layout()
    plt.savefig(f'2D_{test}.png')
    plt.savefig(f'2D_{test}.pdf', bbox_inches='tight')



    # plt.figure()
    # fig, ax = plt.subplots(figsize=(12, 12))
    # if test != "tuned_fhr":
    #     ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    # mplhep.histplot(h_distr, ax=ax, yerr=False,histtype="fill", alpha=0.5, color="red")
    # mplhep.histplot(h_distr, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="red", linewidth=3)
    # text_x = -8.5 if test=="tuned_fhr" else -10.885
    # text_y = 20 if test=="tuned_fhr" else 30
    # ax.text(text_x, text_y, f'Outer Barrel: {output}', color="red", fontsize=20, fontweight="bold")
    # ax.text(text_x, text_y - 1, f'Average FHR : {np.round(mean, 12)}', color="red", fontsize=20, fontweight="bold")
    # plt.xlabel("Average FHR (log)")
    # plt.ylabel("Counts")
    # plt.tight_layout()
    # plt.savefig(f'distr_{test}.png')
    # plt.savefig(f'distr_{test}.pdf')
    # plt.close()
