eeglab;

sub_id = '07';
run_num = 7;
ses = 'LittlePrince';

for i=1:run_num
    if run_num < 10
        run = ['0', int2str(i)];
    else
        run = int2str(i);
    end
    save_eeg_to_set_format(sub_id, ses, run);
end
