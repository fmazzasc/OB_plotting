import argparse
import sys
import os
import yaml
sys.path.append("CRU_ITS/software/py/")
from stave_plotter import FHRateStavePlotter, THScanStavePlotter
from collections import defaultdict
from gc import get_objects
import gc

def plot_thr(data_dirs=None, eos_path='', overwrite_runs=False, max_charge=30, injections=21, skipped_rows=51):

    output_path = '/eos/project/a/alice-its-commissioning/OuterBarrel/verification/2nd_attempt/stability_plots'

    bad_run_dict = {'bad_runs': []}

    yaml_filename = output_path + '/thr_summary.yaml'
    is_yaml = os.path.exists(yaml_filename)

    if(overwrite_runs==False and is_yaml==True):
        thr_dict = yaml.full_load(open(yaml_filename, 'r'))
    else:
        thr_dict = {}
    

    if data_dirs==None:
        data_dirs = [data for data in os.listdir() if data[0]=="L"]

    for data_dir in data_dirs:

        out_dir = output_path + "/Plots_" + data_dir
        if not os.path.exists(out_dir):
                os.makedirs(out_dir)
        
        stave_name = data_dir[0:5]

        if(stave_name not in thr_dict.keys()):
            thr_dict[stave_name] = {'mean': [], 'std' : []}
        
        data_dir_raw = data_dir
        data_dir = eos_path + '/' + data_dir

        item_list = os.listdir(data_dir)
        middle_layer = int(data_dir_raw[1])<5 
        test_list = ["tuned_thr"]



        for test in test_list:

            filenames = [data_dir + "/" + item for item in item_list if test in item]

            if len(filenames)<2:
                continue
            plot_name = test + "_" + data_dir_raw + "_"

            if overwrite_runs==False:
                plot_dir = os.listdir(out_dir)
                if any(test in plot for plot in plot_dir):
                    continue
                    

            # analyse
            plotter = THScanStavePlotter(filename=filenames[0],
                                            filename2=filenames[1],
                                            middle_layer=middle_layer,
                                            injections=injections,
                                            max_charge=max_charge,
                                            skipped_rows=skipped_rows,
                                            plot_extension="png",
                                            plot_name=out_dir + "/" + plot_name,
                                            stave_name=filenames[0][:4])

            if plotter.complete_run == False:
                bad_run_dict['bad_runs'].append(plot_name)
                update_yaml(yaml_filename, thr_dict, bad_run_dict)
                continue

            res = plotter.plot_chips()
            thr_dict[stave_name]['mean'].append(res[0])
            thr_dict[stave_name]['std'].append(res[1])
            plotter.plot_stack()
            plotter.plot_stave()
            del plotter
            gc.collect()
            update_yaml(yaml_filename, thr_dict, bad_run_dict)


def plot_fhr(data_dirs=None, eos_path='', overwrite_runs=False, n_events=3360000):

    output_path = '/eos/project/a/alice-its-commissioning/OuterBarrel/verification/2nd_attempt/stability_plots'

    bad_run_dict = {'bad_runs': []}
    yaml_filename = output_path + '/fhr_summary.yaml'
    is_yaml = os.path.exists(yaml_filename)

    if(overwrite_runs==False and is_yaml==True):
        fhr_dict = yaml.full_load(open(yaml_filename, 'r'))
    else:
        fhr_dict = {}

    if data_dirs==None:
        data_dirs = [data for data in os.listdir() if data[0]=="L"]   
    

    for data_dir in data_dirs:

        
        stave_name = data_dir[0:5]

        out_dir = output_path + "/Plots_" + data_dir
        if not os.path.exists(out_dir):
                os.makedirs(out_dir)
        
        data_dir_raw = data_dir
        data_dir = eos_path + '/' + data_dir
        item_list = os.listdir(data_dir)

        middle_layer = int(data_dir_raw[1])<5

        plot_extension = "png"
        output_file_name = "test"
        internal_yaml_filename = "nameless"
        no_rewrite_masks = True


        test_list = ["simple_readout_20", "simple_readout_tuned", "tuned_fhr"]
        name_list = ["fhr", "tuned_fhr", "tuned_fhr_masked"]

        if(stave_name not in fhr_dict.keys()):
            fhr_dict[stave_name] = {'mean': {}, 'std' : {}}
            for name in name_list:
                fhr_dict[stave_name]['mean'][name] = []
                fhr_dict[stave_name]['std'][name] = []

        for name, test in zip(name_list, test_list):


            filenames = [data_dir + "/" + item for item in item_list if test in item]
            if len(filenames)<2:
                continue
            

            plot_name = name + "_" + data_dir_raw + "_"

            if overwrite_runs==False:
                plot_dir = os.listdir(out_dir)
                if any(name in plot for plot in plot_dir):
                    continue
            


            # analyse
            plotter = FHRateStavePlotter(filename=filenames[0],
                                        filename2=filenames[1],
                                        middle_layer=middle_layer,
                                        plot_extension=plot_extension,
                                        plot_name=out_dir + "/" + plot_name,
                                        yaml_filename=internal_yaml_filename,
                                        no_rewrite_masks=no_rewrite_masks, n_events=n_events)
            
            if plotter.complete_run == False:
                bad_run_dict['bad_runs'].append(plot_name)
                update_yaml(yaml_filename, fhr_dict, bad_run_dict)
                continue
            


            res = plotter.plot_chips()
            fhr_dict[stave_name]['mean'][name].append(res[0])
            fhr_dict[stave_name]['std'][name].append(res[1])
            plotter.plot_stave(force_binary=True)
            plotter.plot_stack(force_binary=True)
            del plotter
            gc.collect()
            
            update_yaml(yaml_filename, fhr_dict, bad_run_dict)





def update_yaml(yaml_filename, res_dict, bad_run_dict):
    with open(yaml_filename, 'w') as outfile:
        yaml.dump(res_dict, outfile, default_flow_style=False)
        yaml.dump(bad_run_dict, outfile, default_flow_style=False)
        outfile.close()
