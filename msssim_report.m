% This program finds msssim between images in two folders (one folder with
% ground truth images and other with predictions)

clear
path = ['C:\Users\gpras\Documents\MATLAB\Shiva\pras_ensemble\pras_ensemble_looping'];
files1 = dir([path filesep 'ae']); 
k=1;
for imgs = 1:length(files1)
    current = files1(imgs).name;
    if length(current)<5
        continue
    end
    if ~strcmp(current(end-2:end),'png')
        continue
    end
    imgt = imread([path filesep 'gt' filesep current]);
    impr = imread([path filesep 'ae' filesep current]);
    outputsheet{k,1} = current;
    result = multissim(imgt,impr);
    outputsheet{k,2} = result;
    k=k+1;
end

out=cell2table(outputsheet,'VariableNames',{'Image Name','MSSSIM'}); 
writetable(out,[path filesep 'outable1.csv']);

