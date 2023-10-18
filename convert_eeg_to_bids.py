
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

bids_root = op.join('', 'derivative')

def convert_to_bids(raw, ica_component=None, ica_dict=None, bad_channel_dict=None, sub_id='06', ses='LittlePrince',
                    task='LittlePrince', run=1, description='preproc',  bids_root='derivative/preprocessed',
                    raw_extension='.fif', dataset_name='Novel Reading', dataset_type='derivative',
                    author='Xinyu Mou, Cuilin He, Liwei Tan', line_freq=50):
    '''
    :param raw: the pre-processed raw data which you want to save into BIDS format
    :param ica_component: The ICA components when you pre-process the data
    :param ica_dict: This is a dict containing information of the ICA components, It should
           satisfy the following format: {'shape': np.ndarray, 'exclude': list}
           The first value represents the shape of the ICA components: (n_components, time_length)
           The second value represents the excluded ICA components when pre-processing the data
    :param bad_channel_dict: a dict containing information of the marked bad channel when pre-processing
           the data. It should satisfy the following format: {'bad channel': list}
    :param sub_id: The id of the subject you are processing
    :param ses: The session of the current data
    :param run: the run of the current data
    :param description: The description after the 'desc-' when naming files. e.g. When naming the pre-processed data
           assign this value as 'preproc'
    :param bids_root: The root of your dataset
    :param raw_extension: The format you want to save for your EEG data. Some supported formats are '.fif', '.vhdr', '.edf'
    :param dataset_name: The name of the dataset, which will be saved in the dataset_description.json
    :param dataset_type: The type of the dataset, can be 'raw' or 'derivative', which will be saved in the dataset_description.json
    :param author: The author of the dataset, which will be saved in the dataset_description.json
    :param line_freq: line frequency of your raw data, normally 50 in China

    This function convert a raw eeg to BIDS format with some sidecar files. The EEG data will be
    saved as the format you assign in parameter raw_extension. Make sure that information in the
    data will not be lost when converting the data format. We strongly recommend you to assign the
    format as the original format of the raw data.

    The parameter ica_component, ica_dict, bad_channel_dict are optional.
    '''
    raw.info["line_freq"] = line_freq  # specify power line frequency as required by BIDS


    new_eeg_path = BIDSPath(subject=sub_id, session=ses, task=task, run=run, root=bids_root, description=description, suffix='eeg', extension=raw_extension,
                         datatype='eeg')
    new_eeg_filename = str(new_eeg_path.basename)
    new_eeg_path = str(new_eeg_path.fpath)
    eeg_suffix_and_extension = 'eeg' + raw_extension
    new_eeg_folder_path = new_eeg_path.replace('\\' + new_eeg_filename, '')
    ica_component_path = new_eeg_path.replace(eeg_suffix_and_extension, 'ica_component.npy')
    ica_json_path = new_eeg_path.replace(eeg_suffix_and_extension, 'ica_component.json')
    bad_channel_path = new_eeg_path.replace(eeg_suffix_and_extension, 'bad_channel.json')

    if not os.path.exists(new_eeg_folder_path):
        os.makedirs(new_eeg_folder_path)

    # save raw data
    raw.save(new_eeg_path, overwrite=True)

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


    # get events and save
    events, event_id = mne.events_from_annotations(raw)

    events_tsv_path = new_eeg_path.replace(eeg_suffix_and_extension, 'events.tsv')
    events_json_path = new_eeg_path.replace(eeg_suffix_and_extension, 'events.json')

    with open(events_tsv_path, 'w', newline='') as f:
        tsv_w = csv.writer(f, delimiter='\t')
        tsv_w.writerow(['onset', 'duration', 'event_id'])
        for i in range(events.shape[0]):
            tsv_w.writerow([str(j) for j in events[i, :]])


    events_json = json.dumps(event_id, sort_keys=False, indent=4, separators=(',', ': '))
    f = open(events_json_path, 'w')
    f.write(events_json)


    # omit the annotation of the data (This is due to the implementation detail of mne-bids and mne. When changing the format, the annotations
    # will cause some error due to different mechanism between formats.)
    raw.set_annotations(None)

    # save majority of files in need, including information about coordinate system, JSON of the eeg, channel information, ...
    bids_path = BIDSPath(subject=sub_id, session=ses, task=task, run=run, root=bids_root, description=description,
                         datatype='eeg')
    write_raw_bids(raw, bids_path, format='BrainVision', allow_preload=True, overwrite=True)

    # remove the BrainVision format files because it don't contain the correct annotations
    os.remove(new_eeg_path.replace(eeg_suffix_and_extension, 'eeg.vhdr'))
    os.remove(new_eeg_path.replace(eeg_suffix_and_extension, 'eeg.eeg'))
    os.remove(new_eeg_path.replace(eeg_suffix_and_extension, 'eeg.vmrk'))


    print_dir_tree(bids_root)


    readme = op.join(bids_root, "README")
    with open(readme, "r", encoding="utf-8-sig") as fid:
        text = fid.read()
    print(text)

    mne_bids.make_dataset_description(path=bids_root, name=dataset_name, dataset_type=dataset_type,
                                      authors=author, overwrite=True)



# convert_to_bids()
# mne_bids.make_dataset_description(path=bids_root, name='Novel Reading', dataset_type='derivative', authors='Xinyu Mou, Cuilin He, Liwei Tan', overwrite=True)
#
# # Finally let's get an overview of the events on the whole dataset
# counts = count_events(bids_root)
# counts






