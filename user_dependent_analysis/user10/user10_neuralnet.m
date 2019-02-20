%% input data
user10final = removevars(user10finalfile,{'VarName1'});
gt = user10final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user10final = removevars(user10final,{'groundtruth'});
user10final = table2array(user10final);
user10final = transpose(user10final);

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

user10_final_targets = [temp1 temp2];
user10_final_targets = transpose(user10_final_targets);
