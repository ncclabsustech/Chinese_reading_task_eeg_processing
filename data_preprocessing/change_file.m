% This script converts all the .mff files to correct structure in one
% subject
eeglab;
sub_id = '04';
run_num = 7;
ses = 'LittlePrince';

for i=1:run_num
    if run_num < 10
        run = ['0', int2str(i)];
    else
        run = int2str(i);
    end
    save_eeg_file(sub_id, ses, run);
end
