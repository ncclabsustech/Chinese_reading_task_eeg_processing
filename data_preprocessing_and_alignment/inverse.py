import matplotlib.pyplot as plt
import numpy as np
import os.path as op

import mne
from mne.datasets import sample
from mne.minimum_norm import make_inverse_operator, apply_inverse_raw
from mne.minimum_norm import write_inverse_operator
from mne.datasets import eegbci, fetch_fsaverage
from utils import read_eeg_brainvision
import argparse



def inverse_solution(eeg_path, fname_fwd, inverse_method="dSPM", snr=3.0, hemi="lh", save_inverse_operator_path="eeg-inv.fif", clim=[2, 3, 5], inverse_operator_loose=0.2, inverse_operator_depth=0.8):
    '''

    :param eeg_path:
    :param fname_fwd: -fwd.fif
    :param save_inverse_operator_path: end with -inv.fif
    :param hemi: "lh" or "rh", refering to left hemisphere or right hemisphere
    :param clim: [low, middle, high] for the colorbar
    :return:
    '''
    raw, _, _ = read_eeg_brainvision(eeg_path)
    raw.set_eeg_reference(projection=True)

    noise_cov = mne.compute_raw_covariance(raw, method='empirical', method_params=None,
                               rank=None, verbose=None)


    fwd = mne.read_forward_solution(fname_fwd)


    inverse_operator = make_inverse_operator(
        raw.info, fwd, noise_cov, loose=inverse_operator_loose, depth=inverse_operator_depth
    )
    del fwd



    write_inverse_operator(
        save_inverse_operator_path,
        inverse_operator, overwrite=True
    )


    method = inverse_method
    snr = snr
    lambda2 = 1.0 / snr**2


    stc = apply_inverse_raw(
        raw, inverse_operator, lambda2, method, pick_ori=None
    )



    vertno_max_lh, time_max_lh = stc.get_peak(hemi='lh')
    vertno_max_rh, time_max_rh = stc.get_peak(hemi='rh')

    fs_dir = fetch_fsaverage(verbose=True)
    subjects_dir = op.dirname(fs_dir)


    if hemi == "lh":
        initial_time = vertno_max_lh
    else:
        initial_time = vertno_max_rh

    surfer_kwargs = dict(
        hemi=hemi,
        subjects_dir=subjects_dir,
        clim=dict(kind="value", lims=clim),
        background=(1, 1, 1),   # 背景颜色: (1, 1, 1)为纯白
        initial_time=initial_time,
        time_unit="s",
        size=(800, 800),
        smoothing_steps=10,
        surface='white',  # 指定是否呈现沟壑
        views='lateral',
        colormap='mne'
    )



    brain = stc.plot(**surfer_kwargs)
    brain.add_foci(
        initial_time,
        coords_as_verts=True,
        hemi=hemi,
        color="blue",
        scale_factor=0.6,
        alpha=0.5,
    )
    brain.add_text(
        0.1, 0.9, inverse_method + " (plus location of maximal activation)", "title", font_size=14
    )



    peak_stc_lh = stc.lh_data[vertno_max_lh, :]

    peak_stc_rh = stc.rh_data[vertno_max_rh, :]

    data = stc.data[:10, :].T
    fig, ax = plt.subplots()
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']

    for i in range(10):
        ax.plot(stc.times, data[:, i] + i * 3, color=colors[i])  # 偏移每个通道以便可视化

    ax.plot(stc.times, peak_stc_lh + 30, color='cornflowerblue', label='lh')
    ax.plot(stc.times, peak_stc_rh + 33, color='firebrick', label='rh')
    ax.set(xlabel="time (s)", ylabel="%s value" % method)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.show()



parser = argparse.ArgumentParser(description='Parameters that can be changed in this experiment')
parser.add_argument('--eeg_path', type=str, default=r'example_eeg.fif')
parser.add_argument('--fname_fwd', type=str, default=r'example_eeg-fwd.fif')
parser.add_argument('--inverse_method', type=str, default=r'dSPM')
parser.add_argument('--snr', type=float, default=3.0)
parser.add_argument('--hemi', type=str, default=r'lh')
parser.add_argument('--save_inverse_operator_path', type=str, default=r'example_eeg-inv.fif')
parser.add_argument('--clim', type=list, default=[2, 3, 5])
parser.add_argument('--inverse_operator_loose', type=float, default=0.2)
parser.add_argument('--inverse_operator_depth', type=float, default=0.8)


args = parser.parse_args()


inverse_solution(args.eeg_path, args.fname_fwd, inverse_method=args.inverse_method, snr=args.snr,
        hemi=args.hemi,
        save_inverse_operator_path=args.save_inverse_operator_path,
        clim=args.clim, inverse_operator_loose=args.inverse_operator_loose,
        inverse_operator_depth=args.inverse_operator_depth)

