%% input data
user9final = removevars(user9finalfile,{'VarName1'});
gt = user9final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user9final = removevars(user9final,{'groundtruth'});
user9final = table2array(user9final);
user9final = transpose(user9final);

%% target data

x = size(gt_class_labels);
temp1 = zeros(x(1),1);
temp2 = zeros(x(1),1);

for k=1:x(1)
    if gt_class_labels(k) == 1
        temp1(k) = 1;
    else
        temp2(k) = 1;
    end
end

user9_final_targets = [temp1 temp2];
user9_final_targets = transpose(user9_final_targets);
