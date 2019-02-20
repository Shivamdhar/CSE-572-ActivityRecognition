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

%% clean
X_train = table2array(X_train);
X_test = table2array(X_test);

%% model building
c = cvpartition(Y_train, 'k', 5)
opts = statset('display', 'iter');
fun = @(train_data, train_labels, test_data, test_labels)sum(predict(fitcsvm(train_data, train_labels, 'KernelFunction', 'rbf'), test_data) ~= test_labels);
[fs,history] = sequentialfs(fun, X_train, Y_train, 'cv', c, 'options', opts, 'nfeatures', 2);
X_train_w_best_features = X_train(:,fs);
mdl = fitctree(X_train,Y_train,'OptimizeHyperparameters','auto')

%% test - accuracy, precison and recall
% X_test = table2array(X_test);
predict(mdl, X_test);
view(mdl,'Mode','graph');
acc = sum(predict(mdl, X_test) == Y_test) / length(Y_test) * 100;
ConfMtx = confusionmat(Y_test, predict(mdl, X_test));
precision = @(ConfMtx) diag(ConfMtx)./sum(ConfMtx, 2);
recall = @(ConfMtx) diag(ConfMtx)./sum(ConfMtx, 1)';
precision(ConfMtx) %gives precision for both the classes 
recall(ConfMtx) %gives recall for both the classes
mean(precision(ConfMtx))
mean(recall(ConfMtx))

%% Plot predictor estimates
imp = predictorImportance(mdl);

figure;
bar(imp);
title('Predictor Importance Estimates');
ylabel('Estimates');
xlabel('Predictors');
h = gca;
h.XTickLabel = mdl.PredictorNames;
h.XTickLabelRotation = 45;
h.TickLabelInterpreter = 'none';


%{
    ans =

    0.9263
    0.9097


ans =

    0.9054
    0.9297


ans =

    0.9180


ans =

    0.9175

acc

acc =

   91.7686


%}