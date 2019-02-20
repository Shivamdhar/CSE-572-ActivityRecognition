%% input data
combinedfinal = removevars(combinedentireindependent,{'VarName1'});
gt = combinedfinal(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
combinedfinal = removevars(combinedfinal,{'groundtruth'});
combinedfinal = table2array(combinedfinal);
combinedfinal = transpose(combinedfinal);

%% target data

x = size(gt_class_labels)
temp1 = zeros(x(1),1);
temp2 = zeros(x(1),1);

for k=1:x(1)
    if gt_class_labels(k) == 1
        temp1(k) = 1;
    else
        temp2(k) = 1;
    end
end

combined_final_targets = [temp1 temp2];
combined_final_targets = transpose(combined_final_targets);

