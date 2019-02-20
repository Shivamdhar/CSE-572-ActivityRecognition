%% input data
user13final = removevars(user13finalfile,{'VarName1'});
gt = user13final(:,{'groundtruth'});
array = table2array(gt);
gt_new = cellstr(array);
gt_class_labels = grp2idx(gt_new);
user13final = removevars(user13final,{'groundtruth'});
user13final = table2array(user13final);
user13final = transpose(user13final);

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

user13_final_targets = [temp1 temp2];
user13_final_targets = transpose(user13_final_targets);
