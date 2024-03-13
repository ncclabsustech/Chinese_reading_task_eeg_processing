import mne
import numpy as np
import openpyxl
import csv
import argparse


def read_eeg_brainvision(eeg_path, montage_name='GSN-HydroCel-128'):
    eeg = mne.io.read_raw_brainvision(eeg_path)
    events = []
    event_id = {}

    events_path = eeg_path.replace('eeg.vhdr', 'events.tsv')

    with open(events_path) as events_file:
        csv_reader = csv.reader(events_file, delimiter='\t')  # use csv.reader to read file
        header = next(csv_reader)        # read the titles in the first row
        for row in csv_reader:  # save data
            events.append([int(row[4]), 0, int(row[3])])  # select a column and add to data
            if row[2] not in event_id.keys():
                event_id[row[2]] = int(row[3])

    events = np.array(events)

    annotations = mne.annotations_from_events(events, eeg.info['sfreq'], event_id)
    eeg.set_annotations(annotations)

    montage = mne.channels.make_standard_montage(montage_name)
    eeg.set_montage(montage)


    return eeg, events, event_id