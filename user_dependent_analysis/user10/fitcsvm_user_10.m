%% clean file and create database
head(user10finalfile, 5)

%% remove the first column from the table
user10final = removevars(user10finalfile,{'VarName1'});

%% create the groundtruth table with a single column as the groundtruth labels
gt = user10final(:,{'groundtruth'});

%% convert table to array
array = table2array(gt);

%% convert array to cells
gt_new = cellstr(array);

%% create index vector from grouping variable
gt_class_labels = grp2idx(gt_new);

%% remove the last groundtruth column from the main table
user10final_clean = removevars(user10final,{'groundtruth'});

%% randomly generate permutations
random_num = randperm(87);

%% create the final dataset as X, Y, X_train, Y_train, X_test, Y_test with 80% train and 20% test
X = user10final_clean(:,:);
X_train = X(random_num(1:69), :);
Y = gt_class_labels(:,:);
Y_train = Y(random_num(1:69),:);
X_test = X(random_num(70:end),:);
Y_test = Y(random_num(70:end),:);

%% feature selection
opts = statset('display', 'iter');
fun = @(train_data, train_labels, test_data, test_labels)sum(predict(fitcsvm(train_data, train_labels, 'KernelFunction', 'rbf'), test_data) ~= test_labels);
[fs,history] = sequentialfs(fun, X_train, Y_train, 'cv', c, 'options', opts, 'nfeatures', 2);
X_train_w_best_features = X_train(:,fs);
mdl = fitcsvm(X_train_w_best_features, Y_train, 'KernelFunction', 'rbf', 'OptimizeHyperparameters', 'auto', 'HyperparameterOptimizationOptions', struct('AcquisitionFunctionName', 'expected-improvement-plus', 'ShowPlots', true));

%% test
X_test_w_best_features = X_test(:,fs);
predict(mdl, X_test_w_best_features);
acc = sum(predict(mdl, X_test_w_best_features) == Y_test) / length(Y_test) * 100;

%% hyperplane
figure;
hgscatter = gscatter(X_train_w_best_features(:,1), X_train_w_best_features(:,2), Y_train);
hold on;
h_sv = plot(mdl.SupportVectors(:,1), mdl.SupportVectors(:,2), 'ko', 'markersize', 8);

%% test set data
gscatter(X_test_w_best_features(:,1), X_test_w_best_features(:,2), Y_test, 'rb', 'xx')

%% decision plane
XLIMs = get(gca, 'xlim');
YLIMs = get(gca, 'ylim');
[xi, yi] = meshgrid([XLIMs(1):0.01:XLIMs(2)], [YLIMs(1):0.01:YLIMS(2)]);
dd = [xi(:), yi(:)];
pred_mesh = predict(mdl, dd);
redcolor = [1, 0.8, 0.8];
bluecolor = [0.8, 0.8, 1];
pos = find(pred_mesh == 1);
h1 = plot(dd(pos,1), dd(pos,2),'s','color',redcolor,'Markersize',5,'MarkerEdgeColor',redcolor,'MarkerFaceColor',redcolor);
pos = find(pred_mesh == 2);
h2 = plot(dd(pos,1), dd(pos,2),'s','color',bluecolor,'Markersize',5,'MarkerEdgeColor',bluecolor,'MarkerFaceColor',bluecolor);
uistack(h1,'bottom');
uistack(h2,'bottom');
legend([hgscatter;h_sv],{'eating','non-eating','support vectors'})

%% accuracy 
precision = @(ConfMtx) diag(ConfMtx)./sum(ConfMtx, 2);
recall = @(ConfMtx) diag(ConfMtx)./sum(ConfMtx, 1)';
