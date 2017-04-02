clear;
A=imread('unnamed.png');

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
                D(i,j)=255;
            else
                D(i,j)=0;
            end
        end
    end

    subplot(2,5,k+3)
    imshow(D)
    title(strcat('Bitslice - ',num2str(k)));
end

