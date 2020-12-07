import sys
import argparse
import os
import matplotlib
from plotters import plot_fhr, plot_thr
from multiprocessing import Process


matplotlib.use('pdf')
data_path = '/eos/project/a/alice-its-commissioning/OuterBarrel/verification/2nd_attempt'
eos_path = data_path + '/hitmaps'
run_list = [line.rstrip('\n') for line in open(data_path + '/reprocessing/20201203_stability_test/files_stability_obbot.dat')]




data_dirs = []


for run in run_list:
    data_dirs.append(run[-21:])

print(data_dirs)
# data_dirs = data_dirs[:20]

if __name__ == '__main__':
    p1 = Process(target=plot_thr, args = (data_dirs, eos_path))
    p1.start()
    p2 = Process(target=plot_fhr, args = (data_dirs, eos_path, False, 11.2*1000*100))
    p2.start()
    p1.join()
    p2.join()
