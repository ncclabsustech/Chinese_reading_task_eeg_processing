import mne
from mne.preprocessing import ICA
import numpy as np
import argparse
from convert_eeg_to_bids import convert_to_bids


def cut_eeg(raw, start_chapter='CH01', remaining_time_at_beginning=10):

    annotations_onset = raw.annotations.onset
    annotations_description = raw.annotations.description
    rows_indexes = np.where(annotations_description == start_chapter)
    start_index = rows_indexes[0][0]
    start_time = annotations_onset[start_index] - remaining_time_at_beginning

    raw.crop(tmin=start_time)

    return raw, start_time


def read_mff_file(eeg_path, montage_name='GSN-HydroCel-128', preload=False):
    '''
    Read .mff file, set annotations and pick 128 channels, set montage
    '''
    raw = mne.io.read_raw_egi(eeg_path)
    events = mne.find_events(raw, )

    event_id = raw.event_id
    event_desc = {value: key for key, value in event_id.items()}

    annotations = mne.annotations_from_events(events, sfreq=raw.info['sfreq'], event_desc=event_desc)

    raw.set_annotations(annotations)

    raw.pick_types(eeg=True)
    raw.drop_channels(['VREF'])

    montage = mne.channels.make_standard_montage(montage_name)
    raw.set_montage(montage)

    if preload == True:
        raw = raw.load_data()

    return raw

def create_new_raw(raw, crop_time_at_beginning, montage_name='GSN-HydroCel-128', preload=False):
    '''
    create a raw object which can be saved as BrainVision format without losing annotation information

    :param crop_time_at_beginning: the time of the crop point
    '''

    # get raw data, annotations
    data = raw.get_data()
    annotations = raw.annotations
    onset = annotations.onset
    # create new annotations
    new_onset = onset - crop_time_at_beginning
    new_annotations = mne.Annotations(onset=new_onset, duration=annotations.duration, description=annotations.description)
    # create new raw
    new_raw = mne.io.RawArray(data, raw.info)
    new_raw.set_annotations(new_annotations)

    montage = mne.channels.make_standard_montage(montage_name)
    new_raw.set_montage(montage)

    if preload == True:
        new_raw = new_raw.load_data()

    return new_raw

def process_single_eeg(eeg_path=None, sub_id='06', ses='LittlePrince',
                       task='LittlePrince', run=1, raw_data_root='dataset',
                       filtered_data_root='dataset/derivatives/filtered',
                       processed_data_root='dataset/derivatives/preproc',
                       dataset_name='Novel Reading',
                       author='Xinyu Mou, Cuilin He, Liwei Tan', line_freq=50,
                       start_chapter='CH01', low_pass_freq=0.5,
                       high_pass_freq=80, resample_freq=256,
                       remaining_time_at_beginning=10, bad_channels=[], montage_name='GSN-HydroCel-128',
                       ica_method='infomax', ica_n_components=15, rereference='average'):
    '''
    :param eeg_path: data path of the unprocessed eeg.
    :param sub_id: a string of the id of the subject. Pad 0 if the id has only one digit.
    :param ses: a string describing the session of the current data. It will be contained in the file name when saving
                the file.
    :param task: a string describing the task of the current data. It will be contained in the file name when saving
                the file.
    :param run: an integer standing for the run number of the data.
    :param raw_data_root: the path of your raw data, which is also the root of the whole dataset.
    :param filtered_data_root: the path of your filtered data.
    :param processed_data_root: the path of your pre-processed data.
    :param raw_extension: the file extension when saving the data, can be '.fif', '.edf', '.set'
    :param dataset_name: name of the dataset, which will be saved in the dataset_description.json.
    :param author: author of the dataset.
    :param line_freq: line frequency of the data. This is needed when saving the data into BIDS format.
                      Default to be 50.
    :param start_chapter: a string which is the eeg mark of the first chapter in current eeg data
                          e.g. if your eeg starts with chapter 1, then the argument should be 'CH01'.
    :param low_pass_freq: the low pass frequency of the filter.
    :param high_pass_freq: the high pass frequency of the filter.
    :param resample_freq: the resample frequency of the filter.
    :param remaining_time_at_beginning: the remaining time before the start of the valid eeg segment.
    :param bad_channels: bad channels which should be interpolated at beginning.
    :param montage_name: the montage of the eeg.
    :param ica_method: which ica_method you want to use. See mne tutorial for more information.
    :param ica_n_components: how many ICA components you want to use. See mne tutorial for more information.
    :param rereference: re-reference method you want to use.
    '''

    raw = read_mff_file(eeg_path=eeg_path, montage_name=montage_name, preload=True)

    convert_to_bids(raw, ica_component=None, ica_topo_figs=None, ica_dict=None, bad_channel_dict=None, sub_id=sub_id, ses=ses,
                    task=task, run=run, bids_root=raw_data_root, dataset_name=dataset_name,
                    dataset_type='raw', author=author, line_freq=line_freq)

    #raw = read_mff_file(eeg_path=eeg_path, montage_name=montage_name, preload=True)

    raw.info["bads"].extend(bad_channels)
    raw = raw.interpolate_bads()

    # cut data
    raw, crop_start_time = cut_eeg(raw=raw, start_chapter=start_chapter, remaining_time_at_beginning=remaining_time_at_beginning)

    print('-------------------- raw cut --------------------')



    # dowmsample
    raw.resample(resample_freq)

    print('-------------------- raw resampled --------------------')


    # notch filter
    raw = raw.notch_filter(freqs=(50))

    print('-------------------- notch filter finished --------------------')

    # band pass filter
    raw = raw.filter(l_freq=low_pass_freq, h_freq=high_pass_freq)

    filt_raw = create_new_raw(raw=raw, crop_time_at_beginning=crop_start_time, montage_name='GSN-HydroCel-128',
                                 preload=False)

    convert_to_bids(filt_raw, ica_component=None, ica_topo_figs=None, ica_dict=None,
                    bad_channel_dict=None, sub_id=sub_id, ses=ses,
                    task=task, run=run, bids_root=filtered_data_root,
                    dataset_name=dataset_name, dataset_type='derivative',
                    author=author, line_freq=line_freq)


    print('-------------------- filter finished --------------------')

    # mark bad electrodes and bad part of the data
    raw.plot(block=True)

    bad_channels = raw.info['bads']
    print('bad_channels: ', bad_channels)

    bad_channel_dict = {'bad channels': bad_channels}

    # bad channel interpolation
    raw = raw.interpolate_bads()


    print('-------------------- bad channels interpolated --------------------')

    # ICA
    ica = ICA(n_components=ica_n_components, max_iter='auto', method=ica_method, random_state=97)
    # raw_for_ica = raw.copy().filter(l_freq=1, h_freq=None)
    ica.fit(raw, reject_by_annotation=True)

    ica_components = ica.get_sources(raw)
    ica_components = ica_components.get_data()


    ica.plot_sources(raw, show_scrollbars=False, block=True)

    ica_topo_figs = ica.plot_components()



    print('exclude ICA components: ', ica.exclude)

    ica_dict = {'shape':ica_components.shape, 'exclude':ica.exclude}

    ica.apply(raw)

    print('-------------------- ICA finished --------------------')

    # re-reference
    raw.set_eeg_reference(ref_channels=rereference)

    print('-------------------- rereference finished --------------------')


    # plot final data
    raw.plot(block=True)

    preproc_raw = create_new_raw(raw=raw, crop_time_at_beginning=crop_start_time, montage_name='GSN-HydroCel-128', preload=False)

    convert_to_bids(preproc_raw, ica_component=ica_components, ica_topo_figs=ica_topo_figs, ica_dict=ica_dict, bad_channel_dict=bad_channel_dict, sub_id=sub_id, ses=ses,
                    task=task, run=run, bids_root=processed_data_root,
                    dataset_name=dataset_name, dataset_type='derivative',
                    author=author, line_freq=line_freq)


parser = argparse.ArgumentParser(description='Parameters that can be changed in this experiment')
parser.add_argument('--eeg_path', type=str, default='subject_07\LittlePrince\eegdata\subject_07_eeg_01.mff')
parser.add_argument('--sub_id', type=str, default='07')
parser.add_argument('--ses', type=str, default='LittlePrince')
parser.add_argument('--task', type=str, default='reading')
parser.add_argument('--run', type=int, default=1)
parser.add_argument('--raw_data_root', type=str, default='test_dataset')
parser.add_argument('--filtered_data_root', type=str, default='test_dataset/derivatives/filtered')
parser.add_argument('--processed_data_root', type=str, default='test_dataset/derivatives/preproc')
parser.add_argument('--dataset_name', type=str, default='Novel Reading')
parser.add_argument('--author', type=str, default='Xinyu Mou, Cuilin He, Liwei Tan')
parser.add_argument('--line_freq', type=float, default=50)
parser.add_argument('--start_chapter', type=str, default='CH01')
parser.add_argument('--low_pass_freq', type=float, default=0.5)
parser.add_argument('--high_pass_freq', type=float, default=80)
parser.add_argument('--resample_freq', type=float, default=256)
parser.add_argument('--remaining_time_at_beginning', type=float, default=10)
parser.add_argument('--bad_channels', type=list, default=[])  # e.g. ['E1', 'E2']
parser.add_argument('--montage_name', type=str, default='GSN-HydroCel-128')
parser.add_argument('--ica_method', type=str, default='infomax')
parser.add_argument('--ica_n_components', type=int, default=20)
parser.add_argument('--rereference', type=str, default='average')

args = parser.parse_args()

process_single_eeg(eeg_path=args.eeg_path, sub_id=args.sub_id, ses=args.ses,
                       task=args.task, run=args.run, raw_data_root=args.raw_data_root,
                       filtered_data_root=args.filtered_data_root,
                       processed_data_root=args.processed_data_root,
                       dataset_name=args.dataset_name,
                       author=args.author, line_freq=args.line_freq,
                       start_chapter=args.start_chapter, low_pass_freq=args.low_pass_freq,
                       high_pass_freq=args.high_pass_freq, resample_freq=args.resample_freq,
                       bad_channels=args.bad_channels,
                       remaining_time_at_beginning=args.remaining_time_at_beginning, montage_name=args.montage_name,
                       ica_method=args.ica_method, ica_n_components=args.ica_n_components, rereference=args.rereference)

