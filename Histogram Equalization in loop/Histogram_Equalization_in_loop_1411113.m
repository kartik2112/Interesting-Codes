clear;

noOfIterations=5;

mainImg=imread('landscape-9.jpg');
figure(1);
subplot(1,2+noOfIterations,1)
imshow(mainImg);
title('Input image');

% Convert rgb image into B/W image
bwImg=rgb2gray(mainImg);
[row,col]=size(bwImg);

figure(1);
subplot(1,2+noOfIterations,2)
imshow(bwImg);
title('B/W image');


for iterationNo=1:noOfIterations
    % initialize histogram, pdf, cdf arrays
    index=0:255;
    origHistogram=zeros(1,256);  % histogram of input B/W image
    pdf=zeros(1,256);            % Normalized input histogram
    cdf=zeros(1,256);            % Cumulative Distribution Function
    equalizedHistogram=zeros(1,256); % Output histogram
    outputMap=zeros(1,256); % Output histogram

    % Read B/W imagr and count no of pixels having corresponding gray value
    % i.e. generate input histogram
    for i=1:row
        for j=1:col
            origHistogram(bwImg(i,j)+1)=origHistogram(bwImg(i,j)+1)+1; % This will add 1 to gray level bwImg(i,j) in origHistogram
            % Here +1 is done because range of gray levels is 0-255 but MATLAB
            % array index starts from 1
        end
    end

    noOfPixels=row*col;

    % Calculate pdf, cdf and output values
    for i=1:256
        pdf(i)=origHistogram(i)/noOfPixels;
        if(i==1)
            cdf(i)=pdf(i);
        else
            cdf(i)=cdf(i-1)+pdf(i);
        end
        outputMap(i)=round(cdf(i)*255,0);
    end


    figure(1+iterationNo);
    subplot(2,3,1)
    stem(index,origHistogram);
    title('I/P Histogram');

    figure(1+iterationNo);
    subplot(2,3,2)
    plot(index,pdf);
    title('PDF');

    figure(1+iterationNo);
    subplot(2,3,3)
    plot(index,cdf);
    title('CDF');

    figure(1+iterationNo);
    subplot(2,3,4)
    plot(index,outputMap);
    title('s v/s r');


    % Calculate output histogram
    for i=1:256
        equalizedHistogram(outputMap(i)+1)=equalizedHistogram(outputMap(i)+1)+origHistogram(outputMap(i)+1);
    end

    figure(1+iterationNo);
    subplot(2,3,5)
    stem(index,equalizedHistogram);
    title('Equalized Histogram');

    for i=1:row
        for j=1:col
            OPImage(i,j)=outputMap(bwImg(i,j)+1);
        end
    end

    figure(1);
    OPImage=uint8(OPImage);
    subplot(1,2+noOfIterations,2+iterationNo)
    imshow(OPImage);
    title('Equalized image');
    
    bwImg=OPImage;

end




