% Purpose: Predict with machine learning model
% Author: Roshan Sundar

%% ---Get necessary files---
% --Get trained kNN model, trained in classification learner--
mdl = load('trainedModel.mat');
mdl = mdl.trainedModel;

% --Get patient data--
% Home
sheet = 'Sheet_1';
patient = 'Patient_E';
home = ['/N/dc2/scratch/rosundar/STEM2019/NIFTI/MRI/' sheet '/' patient '/'];
cd(home);
% Mask
Normal_ROIMask_path = [home 'ROI/' patient '_PRIMARY_normal_T1POST_ROImask.nii.gz'];
% Series
T1W_path = [home 'Registered_Primary/' patient '_primary_registered_T1W.nii.gz'];
T2W_path = [home 'Registered_Primary/' patient '_primary_registered_T2W.nii.gz'];
ADC_path = [home 'Registered_Primary/' patient '_primary_registered_ADC.nii.gz'];
FLAIR_path = [home 'Registered_Primary/' patient '_primary_registered_FLAIR.nii.gz'];
SW_mIP_path = [home 'Registered_Primary/' patient '_primary_registered_SW_mIP.nii.gz'];
cd([home 'Primary']);
for i=1:2
    d = ls;
    d = d(1:end-1);
    cd(d)
end
t = dir('*AX*T1*C*.nii.gz');
T1POST_path = [cd '/' t.name];

cd(home);

%% ---Preliminary processing and display---
Normal_ROIMask = niftiread(Normal_ROIMask_path);
Normal_ROIMask = double(Normal_ROIMask);

T1W = niftiread(T1W_path);
T1W = double(T1W);
%imshow3Dfull(T1W)

T2W = niftiread(T2W_path);
T2W = double(T2W);
%imshow3Dfull(T2W) 

ADC = niftiread(ADC_path);
ADC = double(ADC);
%imshow3Dfull(ADC)

FLAIR = niftiread(FLAIR_path);
FLAIR = double(FLAIR);
%imshow3Dfull(FLAIR)

SW_mIP = niftiread(SW_mIP_path);
SW_mIP = double(SW_mIP);
%imshow3Dfull(SW_mIP)

T1POST = niftiread(T1POST_path);
T1POST = double(T1POST);
%imshow3Dfull(T1POST)

%% ---Normalize ---
% --Get the average for each series--
T1W_average = 0;
T2W_average = 0;
ADC_average = 0;
FLAIR_average = 0;
SW_mIP_average = 0;
T1POST_average = 0;
voxelCount = 0;

for i = 1:numel(Normal_ROIMask)
    b = Normal_ROIMask(i);
    if b == 1
        T1W_average = T1W_average + T1W(i);
        T2W_average = T2W_average + T2W(i);
        ADC_average = ADC_average + ADC(i);
        FLAIR_average = FLAIR_average + FLAIR(i);
        SW_mIP_average = SW_mIP_average + SW_mIP(i);
        T1POST_average = T1POST_average + T1POST(i);
        voxelCount = voxelCount + 1;
    end
end

T1W_average = T1W_average/voxelCount;
T2W_average = T2W_average/voxelCount;
ADC_average = ADC_average/voxelCount;
FLAIR_average = FLAIR_average/voxelCount;
SW_mIP_average = SW_mIP_average/voxelCount;
T1POST_average = T1POST_average/voxelCount;

% --Divide each series by appropriate average--
T1W = T1W./T1W_average;
T2W = T2W./T2W_average;
ADC = ADC./ADC_average;
FLAIR = FLAIR./FLAIR_average;
SW_mIP = SW_mIP./SW_mIP_average;
T1POST = T1POST./T1POST_average;

%% ---Get recurred slice--- ** TAKE THIS OFF WHEN PREDICTING FOR WHOLE BRAIN
Recurred_ROIMask_path = [home 'ROI/' patient '_PRIMARY_recurred_T1POST_ROImask.nii.gz'];
Recurred_ROIMask = niftiread(Recurred_ROIMask_path);
Recurred_ROIMask_path = double(Recurred_ROIMask);
[X, Y, Z] = size(Recurred_ROIMask);

slice = 0;
for z = 1:Z
    for y = 1:Y
        for x = 1:X
            if Recurred_ROIMask(x, y, z) == 1
                slice = z;
                break
            end
        end
    end
end

%% ---Predict---
[Xlen, Ylen, Zlen] = size(T1POST);
predictionMat = zeros(Xlen, Ylen, Zlen);
scoreMat_recurrence = zeros(Xlen, Ylen, Zlen);
scoreMat_nonrecurrence = zeros(Xlen, Ylen, Zlen);
parfor z = slice % use 1:Zlen to go over whole brain % one slice above fsl slice
    mdl_ = mdl;
    for y = 1:Ylen
        for x = 1:Xlen
            if ADC(x,y,z) ~= 0
                % Predict
                predictor = [T1W(x,y,z) T2W(x,y,z) ADC(x,y,z) FLAIR(x,y,z) SW_mIP(x,y,z) T1POST(x,y,z)];
                [label, score] = predict(mdl_.ClassificationKNN, predictor);
                
                % Add results to relevant matrices
                predictionMat(x,y,z) = label;
                scoreMat_recurrence(x,y,z) = score(1, 2);
                scoreMat_nonrecurrence(x,y,z) = score(1,1);
            end
        end
    end
end

%% ---Save output---
cd Prediction

% Adjust a header to suit the matrices
header = niftiinfo(T1POST_path);
header.Datatype = 'double';
header.BitsPerPixel = 64;
header.raw.bitpix = 64;

% --Save matrices--
niftiwrite(predictionMat, [patient '_predmask.nii'], header);
niftiwrite(scoreMat_recurrence, [patient '_recurrence_scoremask.nii'], header);
niftiwrite(scoreMat_nonrecurrence, [patient '_nonrecurrence_scoremask.nii'], header);