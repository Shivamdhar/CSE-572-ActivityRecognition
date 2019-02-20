%% input data
user14final = removevars(user14finalfile,{'VarName1'});
gt = user14final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user14final = removevars(user14final,{'groundtruth'});
user14final = table2array(user14final);
user14final = transpose(user14final);

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

user14_final_targets = [temp1 temp2];
user14_final_targets = transpose(user14_final_targets);
