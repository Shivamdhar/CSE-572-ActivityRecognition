%% input data
user16final = removevars(user16finalfile,{'VarName1'});
gt = user16final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user16final = removevars(user16final,{'groundtruth'});
user16final = table2array(user16final);
user16final = transpose(user16final);

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

user16_final_targets = [temp1 temp2];
user16_final_targets = transpose(user16_final_targets);
