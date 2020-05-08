load('/home/straydog/Documents/senior_design/python_scripts/commits/CSU-Radar-Calibration/Time Series/time_series/13512.mat')


l = length(HI);
Pr = 10*log10(sum((HI.^2+HQ.^2)/2,2));
Prm = 10*log10(sum((HI.^2+HQ.^2)/2));
%plot(Prm);
%plot(Pr);

dat = chivo_timeSeries('13512.mat');
%polar((dat.azimuth*pi)/180, Pr.');
Range = [1:200].*.01;
Az = (dat.azimuth*pi)/180;
X = (Range'.*cos(Az));
Y = (Range'.*sin(Az));
PrmH = 10*log10((HI.^2+HQ.^2)/2);
PrmV = 10*log10((VI.^2+VQ.^2)/2);
PrHV = 10*log10(((HI.^2+HQ.^2).*(VI.^2+VQ.^2))/2);
PrZ = PrmH-PrmV;

%figure(1)
%pcolor(Y,X,PrmH');
%ylim([0 1])
%shading flat
%colorbar

figure(2)
pcolor(Y,X,PrmH');
ylim([0 1])
shading flat
colorbar

figure(3)
pcolor(Y,X,PrmV');
ylim([0 1])
shading flat
colorbar

figure(4)
pcolor(Y,X,PrHV');
ylim([0 1])
shading flat
colorbar

figure(5)
pcolor(Y,X,PrZ');
ylim([0 1])
shading flat
colorbar

%figure(5)
%plot(PrmV([2080:8016],[7:11]));
%shading flat
%legend

