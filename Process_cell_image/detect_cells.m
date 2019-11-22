% detect_cells.m (c) Prasanth "Prash" Ganesan
% author email: prasganesan.pg@gmail.com

% Read the rgb image
I = imread('original.jpg');
figure;imshow(I)

% Convert RGB to gray
I_gray = rgb2gray(I);
figure; imshow(I_gray);

% Detecting the cells
I_copy=I_gray;
[N,edges] = histcounts(double(I_copy(:)),10);
[~,ind] = max(N);
threshold = edges(ind-1);
I_copy=I_copy<threshold;
figure; imshow(I_copy);

[B,L] = bwboundaries(I_copy,'noholes');
hold on
areamat=[];
for k = 1:length(B)
   boundary = B{k};
   areamat(k) = polyarea(boundary(:,2), boundary(:,1));
   plot(boundary(:,2), boundary(:,1), 'r', 'LineWidth', 2)
   if areamat(k)>2500 % hardcoded because the cell size doesnt change much
       plot(boundary(:,2), boundary(:,1), 'g', 'LineWidth', 2)
   end
end

