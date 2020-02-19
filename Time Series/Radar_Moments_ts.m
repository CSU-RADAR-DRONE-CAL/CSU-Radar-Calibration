%% Script to read CHIVO time series data. Use python script (TS_Extractor_RVP900.py to read CHIVO timeseries data
   %The reader spits out a .matlab file which contains:
   %Object: chivito -> Contains IQ data, Az, EL, prt
   %filename
   %lambda
   %range
   
%% Organizing object data into local variables

%Horizontal IQ data
% Hi = chivito.Hi;
% Hq = chivito.Hq;
% H_s = complex(Hi,Hq);
% %Vertical IQ data
% Vi = chivito.Vi;
% Vq = chivito.Vq;
% V_s = complex(Vi,Vq)
%Calculation recieved power
for i = i:length(H_s


