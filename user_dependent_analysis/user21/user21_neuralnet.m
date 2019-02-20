%% input data
user21final = removevars(user21finalfile,{'VarName1'});
gt = user21final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user21final = removevars(user21final,{'groundtruth'});
user21final = table2array(user21final);
user21final = transpose(user21final);

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

user21_final_targets = [temp1 temp2];
user21_final_targets = transpose(user21_final_targets);
