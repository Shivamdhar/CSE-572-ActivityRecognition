%% input data
user11final = removevars(user11finalfile,{'VarName1'});
gt = user11final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user11final = removevars(user11final,{'groundtruth'});
user11final = table2array(user11final);
user11final = transpose(user11final);

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

user11_final_targets = [temp1 temp2];
user11_final_targets = transpose(user11_final_targets);
