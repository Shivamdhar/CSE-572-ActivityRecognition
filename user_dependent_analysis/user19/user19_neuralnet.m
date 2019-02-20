%% input data
user19final = removevars(user19finalfile,{'VarName1'});
gt = user19final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user19final = removevars(user19final,{'groundtruth'});
user19final = table2array(user19final);
user19final = transpose(user19final);

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

user19_final_targets = [temp1 temp2];
user19_final_targets = transpose(user19_final_targets);
