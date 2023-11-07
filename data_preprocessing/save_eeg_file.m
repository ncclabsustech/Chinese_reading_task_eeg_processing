function save_eeg_file(sub_id, ses, run)
    % This function convert the two-layer .mff files to 
    % one-layer.
    EEG_root = [pwd, '\\subject_', sub_id, '\\', ses, '\\eegdata\\'];
    EEG_filename = ['subject_', sub_id, '_eeg_', run, '.mff'];
  

    movefile([EEG_root, EEG_filename], [EEG_root, '_', EEG_filename]);

    EEG_filename_inside = dir([EEG_root, '_', EEG_filename, '\\', '*.mff']);
    
    movefile([EEG_root, '_', EEG_filename, '\\', EEG_filename_inside(1).name], [EEG_root, EEG_filename]);  
    rmdir([EEG_root, '_', EEG_filename])
    
