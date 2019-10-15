% Purpose: Rigorous testing of machine learning model
% Author: Roshan Sundar

cd /N/u/rosundar/Carbonate/bin;
setname = 'set.mat';
set = load(setname);
set = set.set;

% Get where col values change
patient_col = set(:, 8);
patient_col_change = diff(patient_col);
patient_col_change = [patient_col_change; 0];

% pick out the starting and ending row number for each patient
startRows = [1];
endRows = [];
for i = 1:length(patient_col)
    if patient_col_change(i) == 1
        endRows = [endRows i];
        startRows = [startRows i+1];
    end
end
endRows = [endRows length(patient_col)];

% Separate each patient's data
AllPatientData = cell(length(startRows), 1);
for i = 1:length(startRows)
    patientData = set(startRows(i):endRows(i), :);
    AllPatientData{i} = patientData;
end

% Leave one out
accuracyList = zeros(length(AllPatientData), 1);
sensitivityList = zeros(length(AllPatientData), 1);
specificityList = zeros(length(AllPatientData), 1);
precisionList = zeros(length(AllPatientData), 1);
confmatData = cell(length(AllPatientData), 1);

for i = 1:length(AllPatientData)
    patientTrainData = [];
    patientTestData = AllPatientData{i};
    
    % Get training data, all data except for the current patient's
    for k = 1:length(AllPatientData)
        if ~isequal(patientTestData, AllPatientData{k})
            patientTrainData = [patientTrainData; AllPatientData{k}];
        end
    end
    
    % Train knn
    input = patientTrainData(:, 1:6);
    output = patientTrainData(:, 7);
    mdl = fitcknn(input, output,'NumNeighbors', 10, 'Standardize', 1);
    
    % Test knn
    predictor = patientTestData(:, 1:6);
    prediction = predict(mdl, predictor);
    
    % Calculate accuracy
    actual = patientTestData(:, 7);
    sum = 0;
    for k = 1:length(prediction)
        if prediction(k) == actual(k)
            sum = sum + 1;
        end
    end
    
    accuracy = (sum / length(prediction)) * 100;
    accuracyList(i, 1) = accuracy;
    
    % Create confusion matrix
    confusionMat =  confusionmat(actual, prediction);
    confmatData{i} = confusionMat;
    
    % Calculate other metics
    sensitivity = (confusionMat(2, 2)/(confusionMat(2, 2) + confusionMat(2, 1))) * 100;
    sensitivityList(i, 1) = sensitivity;
    
    specificity = (confusionMat(1, 1)/(confusionMat(1, 1) + confusionMat(1, 2))) * 100;
    specificityList(i, 1) = specificity;
    
    precision = (confusionMat(2, 2)/(confusionMat(2, 2) +  confusionMat(1, 2))) * 100;
    precisionList(i, 1) = precision;
end

% Get the average & total confusion matrix
avg_accuracy = mean(accuracyList);

totalconfMat = zeros(length(confusionMat), length(confusionMat));
for i = 1:length(confmatData)
    totalconfMat = totalconfMat + confmatData{i};
end

% Get overall metrics
sensitivity = (totalconfMat(2, 2)/(totalconfMat(2, 2) + totalconfMat(2, 1))) * 100;
    
specificity = (totalconfMat(1, 1)/(totalconfMat(1, 1) + totalconfMat(1, 2))) * 100;
    
precision = (totalconfMat(2, 2)/(totalconfMat(2, 2) +  totalconfMat(1, 2))) * 100;

% Display
avg_accuracy
sensitivity
specificity
precision
totalconfMat