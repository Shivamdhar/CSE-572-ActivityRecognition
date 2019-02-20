%% input data
user12final = removevars(user12finalfile,{'VarName1'});
gt = user12final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user12final = removevars(user12final,{'groundtruth'});
user12final = table2array(user12final);
user12final = transpose(user12final);

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

user12_final_targets = [temp1 temp2];
user12_final_targets = transpose(user12_final_targets);
