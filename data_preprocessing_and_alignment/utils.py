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
        csv_reader = csv.reader(events_file, delimiter='\t')  # 使用csv.reader读取csvfile中的文件
        header = next(csv_reader)        # 读取第一行每一列的标题
        for row in csv_reader:  # 将csv 文件中的数据保存到data中
            events.append([int(row[4]), 0, int(row[3])])  # 选择某一列加入到data数组中
            if row[2] not in event_id.keys():
                event_id[row[2]] = int(row[3])

    events = np.array(events)

    montage = mne.channels.make_standard_montage(montage_name)
    eeg.set_montage(montage)

    return eeg, events, event_id