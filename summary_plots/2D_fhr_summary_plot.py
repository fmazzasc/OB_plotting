import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib
from hist import Hist
import hist
import mplhep

# Quick construction, no other imports needed:
matplotlib.use("pdf")


with open("../../stability_plots/fhr_summary.yaml", 'r') as stream:
    dic = yaml.load(stream)


staves = list(dic.keys())[:-1]


test_type = ['tuned_fhr', 'tuned_fhr_masked']
output_string = ['Tuned FHR w/o masking', 'Tuned FHR w/ masking']




for test,output in zip(test_type, output_string):
    fhr_array_log = np.array([])
    fhr_array_log_aver = np.array([])
    stave_array = np.array([])
    
    for i,stave in enumerate(staves):
        mean_arr = np.array(dic[stave]['mean'][test])
        mask1 = mean_arr > 0
        fhr_array_log = np.append(fhr_array_log, np.log10(mean_arr[mask1]), axis=0)
        fhr_array_log_aver = np.append(fhr_array_log_aver, [np.log10(np.mean(mean_arr[mask1]))], axis=0)

        temp_arr = (i+0.5)*np.ones(len(mean_arr[mask1]))

        stave_array = np.append(stave_array, temp_arr, axis = 0)

    fhr_array = np.power(10,fhr_array_log)
    mean = np.median(fhr_array)
    std = np.std(fhr_array)
    print("Average:", mean, " RMS: ", std)

    h = Hist(
        hist.axis.Regular(
            len(staves), 0, len(staves)-1, name="", label="", underflow=False, overflow=False
        ),
        hist.axis.Regular(
            20, -13, -4, name="Average Fake Hit Rate", label="", underflow=False, overflow=False
        ),
    )


    h_distr = Hist(
        hist.axis.Regular(
            15, np.min(fhr_array_log_aver), np.max(fhr_array_log_aver), name="", label="Average FHR", underflow=False, overflow=False
        )
    )



    h.fill(stave_array, fhr_array_log)
    h_distr.fill(fhr_array_log_aver)


    fig, ax = plt.subplots(figsize=(20, 5))
    w, x, y = h.to_numpy()
    mesh = ax.pcolormesh(x, y, w.T, cmap = 'viridis')
    ax.set_xticks(range(len(staves)))
    ax.set_xticklabels(staves)
    ax.set_xticklabels(staves, rotation='vertical', fontsize=13)
    ax.set_ylabel('Average Fake Hit Rate (log)', fontsize=18)
    loc = plticker.MultipleLocator(base=3.0) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    fig.colorbar(mesh)
    plt.text( 80, -5., f'Outer Barrel: {output}', fontsize = 20, color = 'white')
    plt.text( 80, -5.7, f'Average FHR : {np.round(mean, 12)}', fontsize = 20, color = 'white')
    plt.plot([0, np.max(stave_array)], [np.log10(mean), np.log10(mean)], 'w--')
    plt.xlim((0, np.max(stave_array)-0.5))
    # plt.ylim((-12, -4))
    plt.tight_layout()
    plt.savefig(f'2D_{test}.png')


    matplotlib.style.use(mplhep.style.ALICE)

    fig, ax = plt.subplots(figsize=(12, 12))
    mplhep.histplot(h_distr, ax=ax, yerr=False,histtype="fill", alpha=0.5, color="red")
    mplhep.histplot(h_distr, ax=ax, yerr=False, histtype="step", alpha=1, linestyle = "--", color="red", linewidth=3)

    plt.text( -8.5, 20, "Outer Barrel Staves", color="red", fontsize=35, fontweight="bold")
    plt.xlabel("Average FHR (log)")
    plt.ylabel("Counts")
    plt.tight_layout()
    plt.savefig(f'distr_fhr_{test}.png')
    plt.savefig(f'distr_fhr_{test}.pdf')
