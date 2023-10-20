function save_eeg__to_set_format(sub_id, ses, run)
    %[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
    current_path = pwd;
    EEG_root = [pwd, '\\subject_', sub_id, '\\', ses, '\\eegdata\\'];
    EEG_filename = ['subject_', sub_id, '_eeg_', run, '.mff'];
    save_EEG_filename = ['subject_', sub_id, '_eeg_', run, '.set'];

   
    movefile([EEG_root, EEG_filename], [EEG_root, '_', EEG_filename]);

    EEG_filename_inside = dir([EEG_root, '_', EEG_filename, '\\', '*.mff']);
    
    movefile([EEG_root, '_', EEG_filename, '\\', EEG_filename_inside(1).name], [EEG_root, EEG_filename]);  
    rmdir([EEG_root, '_', EEG_filename])
    


    EEG = pop_mffimport({[EEG_root, EEG_filename]},{'code'},0,0);
    %[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0,'gui','off'); 
    EEG = pop_saveset( EEG, 'filename', save_EEG_filename, 'filepath', EEG_root);
    %[ALLEEG, EEG, CURRENTSET] = eeg_store(ALLEEG, EEG, CURRENTSET);
    %eeglab redraw;
