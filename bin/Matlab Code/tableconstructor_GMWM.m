% Purpose: Create machine learning training dataset 
%          for the GM WM method
% Author: Roshan Sundar

%% ---Start clean---
clear all, close all,  clc;

%% ---Main loop---
sheet = 'Sheet_1';
patientList = {'Patient_E', 'Patient_I', 'Patient_O', 'Patient_R'};
totaltable = [];
for p = patientList
    patient = p{1};
    % === Get paths ===
    home = ['/N/dc2/scratch/rosundar/STEM2019/NIFTI/MRI/' sheet '/' patient '/'];
    cd(home)
    % --Masks--
    Recurred_ROIMask_path = [home 'ROI/' patient '_PRIMARY_recurred_T1POST_ROImask.nii.gz'];
    Nonrecurred_ROIMask_path = [home 'ROI/' patient '_PRIMARY_non_recurred_LARGE_T1POST_ROImask.nii.gz'];
    Normal_ROIMask_path = [home 'ROI/' patient '_PRIMARY_normal_T1POST_ROImask.nii.gz'];
    % --Series--
    T1W_path = [home 'Registered_Primary/' patient '_primary_registered_T1W.nii.gz'];
    T2W_path = [home 'Registered_Primary/' patient '_primary_registered_T2W.nii.gz'];
    ADC_path = [home 'Registered_Primary/' patient '_primary_registered_ADC.nii.gz'];
    FLAIR_path = [home 'Registered_Primary/' patient '_primary_registered_FLAIR.nii.gz'];
    SW_mIP_path = [home 'Registered_Primary/' patient '_primary_registered_SW_mIP.nii.gz'];
    % --Tissue maps--
    GM_map_path = [home 'Segmented/' patient '_segmented_pve_1.nii.gz'];
    WM_map_path = [home 'Segmented/' patient '_segmented_pve_2.nii.gz'];
    cd([home 'Primary']);
    for i=1:2
        d = ls;
        d = d(1:end-1);
        cd(d)
    end
    t = dir('*AX*T1*C*.nii.gz');
    T1POST_path = [cd '/' t.name];

    cd(home);
    
    % === Preliminary processing and display ===
    % --Load everything in--
    Recurred_ROIMask = niftiread(Recurred_ROIMask_path);
    Recurred_ROIMask = double(Recurred_ROIMask);

    Nonrecurred_ROIMask = niftiread(Nonrecurred_ROIMask_path);
    Nonrecurred_ROIMask = double(Nonrecurred_ROIMask);

    Normal_ROIMask = niftiread(Normal_ROIMask_path);
    Normal_ROIMask = double(Normal_ROIMask);

    T1W = niftiread(T1W_path);
    T1W = double(T1W);

    T2W = niftiread(T2W_path);
    T2W = double(T2W);

    ADC = niftiread(ADC_path);
    ADC = double(ADC);

    FLAIR = niftiread(FLAIR_path);
    FLAIR = double(FLAIR);

    SW_mIP = niftiread(SW_mIP_path);
    SW_mIP = double(SW_mIP);

    T1POST = niftiread(T1POST_path);
    T1POST = double(T1POST);
    
    GM = niftiread(GM_map_path);
    GM = double(GM);
    
    WM = niftiread(WM_map_path);
    WM = double(WM);

    % --Apply gaussian smooth to series--
    header = niftiinfo(T1POST_path);
    resolution = header.PixelDimensions;
    sigma = 1/resolution(1);

    T1W = imgaussfilt(T1W, sigma);
    T2W = imgaussfilt(T2W, sigma);
    ADC = imgaussfilt(ADC, sigma);
    FLAIR = imgaussfilt(FLAIR, sigma);
    SW_mIP = imgaussfilt(SW_mIP, sigma);
    T1POST = imgaussfilt(T1POST, sigma);

    % --Optional Display--
    %imshow3Dfull(Recurred_ROIMask)
    %imshow3Dfull(Nonrecurred_ROIMask)
    %imshow3Dfull(Normal_ROIMask)
    %imshow3Dfull(T1W)
    %imshow3Dfull(T2W)
    %imshow3Dfull(ADC)
    %imshow3Dfull(FLAIR)
    %imshow3Dfull(SW_mIP)
    %imshow3Dfull(T1POST)
    %imshow3Dfull(GM)
    %imshow3Dfull(WM)
    
    % === Put data in table ===
    table = [];
    
    % --Get recurred rows--
    recc_rows = [];
    for i = 1:numel(Recurred_ROIMask)
        b = Recurred_ROIMask(i);
        if b == 1
            response = 9;
            if WM(i) > 0.5
                response = 3;
            end
            
            if GM(i) > 0.5
                response = 4;
            end
            
            if response ~= 9
                newrow = [T1W(i) T2W(i) ADC(i) FLAIR(i) SW_mIP(i) T1POST(i) response 0];
                recc_rows = [recc_rows;newrow];
            end
        end
    end
    
    % --Get nonrecurred rows--
    nonrecc_rows = [];
    for i = 1:numel(Nonrecurred_ROIMask)
        b = Nonrecurred_ROIMask(i);
        if b == 1
            response = 9;
            if WM(i) > 0.5
                response = 1;
            end
            
            if GM(i) > 0.5
                response = 2;
            end
            
            if response ~= 9
                newrow = [T1W(i) T2W(i) ADC(i) FLAIR(i) SW_mIP(i) T1POST(i) response 0];
                nonrecc_rows = [nonrecc_rows;newrow];
            end
        end
    end
    
    table = [table;recc_rows];
    % downsample
    %nonrecc_rows = datasample(nonrecc_rows, length(recc_rows));
    table = [table;nonrecc_rows];
    
    % --Add a flag to indicate a new patient--
    % Shouldnt affect ML 
    table(1, 8) = 1;
    
    % === Normalize the table ===
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

    % --Divide each column (series) by appropriate average--
    table(:,1) = table(:,1)./T1W_average;
    table(:,2) = table(:,2)./T2W_average;
    table(:,3) = table(:,3)./ADC_average;
    table(:,4) = table(:,4)./FLAIR_average;
    table(:,5) = table(:,5)./SW_mIP_average;
    table(:,6) = table(:,6)./T1POST_average;
    
    % === Add table to total table ===
    totaltable = [totaltable; table];
end

%% ---Add data to saved table---
cd /N/u/rosundar/Carbonate/bin;
setname = 'set.mat';
set = load(setname);
set = [set.set; totaltable];
save(setname, 'set');