import sys
import argparse
import os
import matplotlib
from plotters import plot_fhr, plot_thr
from multiprocessing import Process


matplotlib.use('pdf')
data_path = '/eos/project/a/alice-its-commissioning/OuterBarrel/verification/2nd_attempt'
eos_path = data_path + '/hitmaps'
run_list = [line.rstrip('\n') for line in open(data_path + '/reprocessing/20201203_stability_test/files_stability_fullob.dat')]




data_dirs = []


for run in run_list:
    data_dirs.append(run[-21:])


print('Number of files: ' , len(data_dirs))


plot_thr(data_dirs, eos_path)
