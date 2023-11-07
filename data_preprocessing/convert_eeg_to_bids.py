
# %%
# We are importing everything we need for this example:
import os.path as op
import shutil
import csv
import os

import mne
import mne_bids

from mne_bids import write_raw_bids, BIDSPath, print_dir_tree
from mne_bids.stats import count_events
import json
import numpy as np
import matplotlib.pyplot as plt


def convert_to_bids(raw, ica_component=None, ica_topo_figs=None, ica_dict=None, bad_channel_dict=None, sub_id='06', ses='LittlePrince',
                    task='Reading', run=1, bids_root='derivative/preproc',
                    dataset_name='Novel Reading', dataset_type='derivative',
                    author='Xinyu Mou, Cuilin He, Liwei Tan', line_freq=50):
    '''
    :param raw: the pre-processed raw data which you want to save into BIDS format
    :param ica_component: The ICA components when you pre-process the data
    :param ica_topo_figs: Topography of ICA components
    :param ica_dict: This is a dict containing information of the ICA components, It should
           satisfy the following format: {'shape': np.ndarray, 'exclude': list}
           The first value represents the shape of the ICA components: (n_components, time_length)
           The second value represents the excluded ICA components when pre-processing the data
    :param bad_channel_dict: a dict containing information of the marked bad channel when pre-processing
           the data. It should satisfy the following format: {'bad channel': list}
    :param sub_id: The id of the subject you are processing
    :param ses: The session of the current data
    :param run: the run of the current data
    :param bids_root: The root of your dataset
    :param dataset_name: The name of the dataset, which will be saved in the dataset_description.json
    :param dataset_type: The type of the dataset, can be 'raw' or 'derivative', which will be saved in the dataset_description.json
    :param author: The author of the dataset, which will be saved in the dataset_description.json
    :param line_freq: line frequency of your raw data, normally 50 in China

    This function convert a raw eeg to BIDS format with some sidecar files. The EEG data will be
    saved following BrainVision format to satisfy the requirement of BIDS. Make sure that information in the
    data will not be lost when converting the data format.

    The parameter ica_component, ica_dict, bad_channel_dict are optional.
    '''
    raw.info["line_freq"] = line_freq  # specify power line frequency as required by BIDS

    # save files in need, including information about coordinate system, JSON of the eeg, channel information, ...
    bids_path = BIDSPath(subject=sub_id, session=ses, task=task, run=run, root=bids_root)
    basename = str(bids_path.basename)

    write_raw_bids(raw, bids_path, format='BrainVision', allow_preload=True, overwrite=True)

    fpath = bids_path.fpath
    eeg_file_directory = str(fpath.parent)

    ica_component_path = eeg_file_directory + '\\' + basename + '_ica_components.npy'
    ica_topo_path = eeg_file_directory + '\\' + basename + '_ica_components_topography'
    ica_json_path = eeg_file_directory + '\\' + basename + '_ica_components.json'
    bad_channel_path = eeg_file_directory + '\\' + basename + '_bad_channels.json'


    # save ICA components
    if ica_component is not None:
        np.save(ica_component_path, ica_component)

    # save ICA component JSON file
    if ica_dict is not None:
        ica_component_json = json.dumps(ica_dict, sort_keys=False, indent=4, separators=(',', ': '))
        f = open(ica_json_path, 'w')
        f.write(ica_component_json)

    # save bad channel record JSON file
    if bad_channel_dict is not None:
        bad_channel_json = json.dumps(bad_channel_dict, sort_keys=False, indent=4, separators=(',', ': '))
        f = open(bad_channel_path, 'w')
        f.write(bad_channel_json)

    if ica_topo_figs is not None:
        fig_num = 1
        if isinstance(ica_topo_figs, list):
            for topo in ica_topo_figs:
                if fig_num < 10:
                    fig_num_str = str(0) + str(fig_num)
                else:
                    fig_num_str = str(fig_num)
                topo.savefig(ica_topo_path + '_' + fig_num_str + '.png')
                fig_num += 1
        else:
            ica_topo_figs.savefig(ica_topo_path + '.png')



    print_dir_tree(bids_root)


    readme = op.join(bids_root, "README")
    with open(readme, "r", encoding="utf-8-sig") as fid:
        text = fid.read()
    print(text)

    mne_bids.make_dataset_description(path=bids_root, name=dataset_name, dataset_type=dataset_type,
                                      authors=author, overwrite=True)










