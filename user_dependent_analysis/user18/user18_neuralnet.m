%% input data
user18final = removevars(user18finalfile,{'VarName1'});
gt = user18final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user18final = removevars(user18final,{'groundtruth'});
user18final = table2array(user18final);
user18final = transpose(user18final);

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

user18_final_targets = [temp1 temp2];
user18_final_targets = transpose(user18_final_targets);
