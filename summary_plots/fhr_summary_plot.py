import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib

# matplotlib.use('pdf')
matplotlib.style.use('seaborn')

with open("../../ciao/fhr_summary.yaml", 'r') as stream:
    dic = yaml.load(stream)


staves = list(dic.keys())[:-1]


mean_fhr = {'tuned_fhr': [], 'tuned_fhr_masked' : [] }
dispersion_fhr = {'tuned_fhr': [], 'tuned_fhr_masked' : [] }   
test_list = ['tuned_fhr', 'tuned_fhr_masked']

for test in test_list:
    for stave in staves:
        mean_arr = np.array(dic[stave]['mean'][test])
        mask = mean_arr > 0
        mean_fhr[test].append(np.mean(mean_arr[mask]))
        dispersion_fhr[test].append((np.max(mean_arr[mask]) - np.min(mean_arr[mask]))/2)


fig, ax = plt.subplots(figsize=(18,6))

ax.errorbar(staves, mean_fhr['tuned_fhr'], dispersion_fhr['tuned_fhr'], fmt = '.', color = 'b', markersize = 8, label='Tuned FHR w/o masking')
ax.errorbar(staves, mean_fhr['tuned_fhr_masked'], dispersion_fhr['tuned_fhr_masked'], fmt = '.', color = 'r', markersize = 8, label='Tuned FHR w/ masking')
plt.xticks(range(len(staves)), staves, rotation=90)
plt.tick_params(axis='x', which='major', labelsize=13)



loc = plticker.MultipleLocator(base=2.0) # this locator puts ticks at regular intervals
ax.xaxis.set_major_locator(loc)

leg = plt.legend(title = 'Outer Barrel', title_fontsize = 25, fontsize = 15)
leg._legend_title_box._text.set_color('green')
plt.xlim((-1,len(staves)+1))
plt.yscale('log')
plt.ylabel('Average Fake HIt Rate)', fontsize = 20   )
# plt.text( 10, 1e-7, 'Outer Barrel', fontsize = 25, color = 'b')
plt.tight_layout()
plt.savefig('fhr_aver.png')
plt.show()
