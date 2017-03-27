clear;

noOfIterations=5;

mainImg=imread('landscape-9.jpg');
figure(1);
subplot(1,3,1)
imshow(mainImg);
title('Input image');

[row,col,dim]=size(mainImg);

% initialize histogram, pdf, cdf arrays
index=0:255;
origHistogram=zeros(3,256);  % histogram of input B/W image
pdf=zeros(3,256);            % Normalized input histogram
cdf=zeros(3,256);            % Cumulative Distribution Function
equalizedHistogram=zeros(3,256); % Output histogram
outputMap=zeros(3,256); % Output histogram

% Read B/W imagr and count no of pixels having corresponding gray value
% i.e. generate input histogram
for dim=1:3
    for i=1:row
        for j=1:col
            origHistogram(dim,mainImg(i,j,dim)+1)=origHistogram(dim,mainImg(i,j,dim)+1)+1; % This will add 1 to gray level bwImg(i,j) in origHistogram
            % Here +1 is done because range of gray levels is 0-255 but MATLAB
            % array index starts from 1
        end
    end
end


noOfPixels=row*col;

% Calculate pdf, cdf and output values
for dim=1:3
    for i=1:256
        pdf(dim,i)=origHistogram(dim,i)/noOfPixels;
        if(i==1)
            cdf(dim,i)=pdf(dim,i);
        else
            cdf(dim,i)=cdf(dim,i-1)+pdf(dim,i);
        end
        outputMap(dim,i)=round(cdf(dim,i)*255,0);
    end
end

figure(2);
subplot(2,3,1)
stem(index,origHistogram(1,:));
title('I/P Histogram');

figure(2);
subplot(2,3,2)
plot(index,pdf(1,:));
title('PDF');

figure(2);
subplot(2,3,3)
plot(index,cdf(1,:));
title('CDF');

figure(2);
subplot(2,3,4)
plot(index,outputMap(1,:));
title('s v/s r');


% Calculate output histogram
for dim=1:3
    for i=1:256
        equalizedHistogram(dim,outputMap(dim,i)+1)=equalizedHistogram(dim,outputMap(dim,i)+1)+origHistogram(dim,outputMap(dim,i)+1);
    end
end

figure(2);
subplot(2,3,5)
stem(index,equalizedHistogram(1,:));
title('Equalized Histogram');

for dim=1:3
    for i=1:row
        for j=1:col
            OPImage(i,j,dim)=outputMap(dim,mainImg(i,j,dim)+1);
        end
    end
end

figure(1);
OPImage=uint8(OPImage);
subplot(1,3,3)
imshow(OPImage);
title('Equalized image');

