clear;

fileID=fopen('Codes.txt','r');
SEQ=textscan(fileID,'%d');
SEQ=SEQ{1};
fclose(fileID);

[txtRow txtCol]=size(SEQ);

for imgNo=1:txtRow
    % This is the file to be manipulated
    A=imread('image.jpg');

    % This is the text that is to be added
    AX=imread(strcat('textHidden',num2str(imgNo),'.png'));

    planeToBeModified=SEQ(imgNo)+1;

    %Convert to B/W
    B=rgb2gray(A);

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
    end


    %Convert to B/W
    BX=rgb2gray(AX);
    
    TX=100;
    [row,col]=size(BX);
    for i=1:row
        for j=1:col
            if(BX(i,j)>=TX)
                D(planeToBeModified,i,j)=255;
            else
                D(planeToBeModified,i,j)=0;
            end
        end
    end

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

    % This is the final file
    imwrite(FIN,strcat('F:\OneDrive\Projects\Proj Github\Matlab Codes\Encryption through Images\image',num2str(imgNo),'.png'));
end

disp('Images generated! Send Codes.txt and all imageX.png. Here X will go from 1 to no of codes')