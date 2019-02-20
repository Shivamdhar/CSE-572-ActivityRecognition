%% input data
user17final = removevars(user17finalfile,{'VarName1'});
gt = user17final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user17final = removevars(user17final,{'groundtruth'});
user17final = table2array(user17final);
user17final = transpose(user17final);

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

user17_final_targets = [temp1 temp2];
user17_final_targets = transpose(user17_final_targets);
