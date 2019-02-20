%% input data
user22final = removevars(user22finalfile,{'VarName1'});
gt = user22final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user22final = removevars(user22final,{'groundtruth'});
user22final = table2array(user22final);
user22final = transpose(user22final);

%% target data

x = size(gt_cl
ass_labels);
temp1 = zeros(x(1),1);
temp2 = zeros(x(1),1);

for k=1:x(1)
    if gt_class_labels(k) == 1
        temp1(k) = 1;
    else
        temp2(k) = 1;
    end
end

user22_final_targets = [temp1 temp2];
user22_final_targets = transpose(user22_final_targets);
