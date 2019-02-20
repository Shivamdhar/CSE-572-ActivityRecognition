combinedfinal = removevars(trainuserindependent,{'VarName1'});
combinedfinal_test = removevars(testuserindependent,{'VarName1'});
gt = combinedfinal(:,{'groundtruth'});
gt_test = combinedfinal_test(:,{'groundtruth'});
array = table2array(gt);
array_test = table2array(gt_test);
gt_new = cellstr(array);
gt_new_test = cellstr(array_test);
gt_class_labels = grp2idx(gt_new);
gt_class_labels_test = grp2idx(gt_new_test);
combinedfinal = removevars(combinedfinal,{'groundtruth'});
combinedfinal_test = removevars(combinedfinal_test,{'groundtruth'});
X_train = combinedfinal(:,:);
Y_train = gt_class_labels(:,:);
X_test = combinedfinal_test(:,:);
Y_test = gt_class_labels_test(:,:);

c = cvpartition(Y_train, 'k', 5)

X_train = table2array(X_train);
X_test = table2array(X_test);

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
[xi, yi] = meshgrid([XLIMs(1):0.01:XLIMs(2)], [YLIMs(1):0.01:YLIMs(2)]);
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

%% generate confusion matrix
ConfMtx = confusionmat(Y_test, predict(mdl, X_test_w_best_features));

%% accuracy 
precision = @(ConfMtx) diag(ConfMtx)./sum(ConfMtx, 2);
recall = @(ConfMtx) diag(ConfMtx)./sum(ConfMtx, 1)';