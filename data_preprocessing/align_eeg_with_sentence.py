import mne
import numpy as np
import openpyxl

def align_eeg_with_sentence(eeg_path, novel_path, containPreface=False, ):
    '''

    :param eeg_path: BrainVision
    :param novel_path:
    :param containPreface:
    :return:
    '''

    #eeg = mne.io.read_raw_brainvision(eeg_path)

    wb = openpyxl.load_workbook(novel_path)
    wsheet = wb.active
    texts = []

    for i in range(2, wsheet.max_row + 1):  # 从2开始，第一行为title
        texts.append((wsheet.cell(row=i, column=1)).value)


    if containPreface == False:
        index = texts.index('1')
        texts = texts[index:]









align_eeg_with_sentence(eeg_path='', novel_path='segmented_Chinense_novel.xlsx', containPreface=False, )