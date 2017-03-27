clear;
% This is the file to be manipulated
A=imread('image.jpg');

subplot(2,5,1)
imshow(A)
title('Original Image')

%Convert to B/W
B=rgb2gray(A);
subplot(2,5,2)
imshow(B)
title('B/W Image')

for k=0:7
    T=2^k;
    [row,col]=size(B);
    for i=1:row
        for j=1:col
            if(bitand(B(i,j),T)==T)
                D(k+1,i,j)=255;
            else
                D(k+1,i,j)=0;
            end
        end
    end
    E=squeeze(D(k+1,:,:));
    subplot(2,5,k+3)
    imshow(E)
    title(strcat('Bitslice - ',num2str(k)));
end


% This is the text that is to be added
AX=imread('textHidden.png');

subplot(2,3,1)
imshow(AX)
title('Original Image')

%Convert to B/W
BX=rgb2gray(AX);
subplot(2,3,2)
imshow(BX)
title('B/W Image')

TX=100;
[row,col]=size(BX);
for i=1:row
    for j=1:col
        if(BX(i,j)>=TX)
            D(2,i,j)=255;
        else
            D(2,i,j)=0;
        end
    end
end

subplot(2,3,4)
imshow(squeeze(D(8,:,:)))
title('Threshold Image')

[row,col]=size(B);
FIN=zeros(size(B));
for k=0:7
    T=2^k;    
    for i=1:row
        for j=1:col
            if(D(k+1,i,j)==255)
                FIN(i,j)=FIN(i,j)+T;
            end
        end
    end
end

FIN=uint8(FIN);

FIN=cat(3,FIN,FIN,FIN);

subplot(2,3,5)
imshow(FIN)

% This is the final file
imwrite(FIN,'textHiddenMergedImg.png');

