clear;

fileID=fopen('Codes.txt','r');
SEQ=textscan(fileID,'%d');
SEQ=SEQ{1};
fclose(fileID);

[txtRow txtCol]=size(SEQ);

for imgNo=1:txtRow
    A=imread(strcat('image',num2str(imgNo),'.png'));

    %Convert to B/W
    B=rgb2gray(A);

    T=2^SEQ(imgNo);
    [row,col]=size(B);
    for i=1:row
        for j=1:col
            if(bitand(B(i,j),uint8(T))==uint8(T))
                D(i,j)=255;
            else
                D(i,j)=0;
            end
        end
    end

    subplot(1,txtRow,imgNo)
    imshow(D)
end


