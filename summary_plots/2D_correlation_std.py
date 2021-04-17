import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib
from hist import Hist
import hist


with open("../summary_data/fhr_summary.yaml", 'r') as stream:
    dic_fhr = yaml.load(stream)

with open("../summary_data/ciao/thr_summary.yaml", 'r') as stream:
    dic_thr = yaml.load(stream)

staves = list(dic_fhr.keys())[:-1]


test_type = ['tuned_fhr', 'tuned_fhr_masked']
output_string = ['Tuned FHR w/o masking', 'Tuned FHR w/ masking']



for test,output in zip(test_type, output_string):

    fhr_list = []
    thr_list = []
    for i,stave in enumerate(staves):
        mean_fhr_arr = np.array(dic_fhr[stave]['mean'][test])
        mask_fhr = mean_fhr_arr > 0
        mean_thr_arr = np.array(dic_thr[stave]['std'])
        mask_thr = mean_thr_arr > 0
        fhr_list.append(np.mean(np.log10(mean_fhr_arr[mask_fhr])))
        thr_list.append(np.mean(mean_thr_arr[mask_thr]))




    h = Hist(
        hist.axis.Regular(
            20, np.min(thr_list), np.max(thr_list), name="Average Threshold Scan (electrons)", label="", underflow=False, overflow=False
        ),
        hist.axis.Regular(
            15, -12, -5, name="Average Fake Hit Rate", label="", underflow=False, overflow=False
        ),
    )



    h.fill(thr_list, fhr_list)


    fig, ax = plt.subplots(figsize=(16, 9))
    w, x, y = h.to_numpy()
    mesh = ax.pcolormesh(x, y, w.T, cmap = 'viridis')

    ax.set_xlabel('Average RMS Threshold Scan (electrons)', fontsize=18)
    ax.set_ylabel('Average Fake Hit Rate (log)', fontsize=18)

    fig.colorbar(mesh)

    plt.text( 20, -11.5, f'Outer Barrel: {output}', fontsize = 20, color = 'white')


    plt.tight_layout()
    plt.savefig(f'../results/2D_corr_RMS_{test}.png')
plt.show()