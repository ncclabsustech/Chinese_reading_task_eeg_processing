import os.path as op
import numpy as np
import mne
from mne.datasets import eegbci, fetch_fsaverage
import csv
from utils import read_eeg_brainvision
import argparse


def forward_solution(eeg_path, save_fwd_path):
    #####################  Download template MRI data #####################
    # Download fsaverage files
    fs_dir = fetch_fsaverage(verbose=True)

    # The files live in:
    subject = "fsaverage"
    trans = "fsaverage"  # MNE has a built-in fsaverage transformation
    src = op.join(fs_dir, "bem", "fsaverage-ico-5-src.fif")
    bem = op.join(fs_dir, "bem", "fsaverage-5120-5120-5120-bem-sol.fif")

    ##################### Load EEG data #####################
    raw, _, _ = read_eeg_brainvision(eeg_path)
    raw.set_eeg_reference(projection=True)



    fwd = mne.make_forward_solution(
        raw.info, trans=trans, src=src, bem=bem, eeg=True, mindist=5.0, n_jobs=None
    )
    print(fwd)

    mne.write_forward_solution(save_fwd_path, fwd)

    return fwd



parser = argparse.ArgumentParser(description='Parameters that can be changed in this experiment')
parser.add_argument('--eeg_path', type=str, default=r'example_eeg.fif')
parser.add_argument('--save_fwd_path', type=str, default=r'example_eeg-fwd.fif')

args = parser.parse_args()

fwd = forward_solution(eeg_path=args.eeg_path,
                       save_fwd_path=args.save_fwd_path)





