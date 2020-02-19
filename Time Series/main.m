% Ivan Arias
% 2019/10/15

% compute spectrum for CHIVO
%addpath /net/denali/storage2/radar2/tmp/Ivan/radartoolbox
%addpath(genpath('/home/sdruiz/Documets/Thesis_Work/Matlab_Scripts/RadarToolBox'))

filename = '13512.mat';

%filename = '/net/denali/storage2/radar2/tmp/Ivan/CSU/tookits/RVP9_timeSeries/res/20190125/col-radar.20190125.210857.164.REL_RHI30.1.H+V.149.mat';
%'/net/denali/storage2/radar2/tmp/Ivan/CSU/tookits/RVP9_timeSeries/res/20190125/col-radar.20190125.210914.523.REL_RHI30.2.H+V.149.mat';
%'/net/denali/storage2/radar2/tmp/Ivan/CSU/tookits/RVP9_timeSeries/res/20190125/col-radar.20190125.210932.921.REL_RHI30.3.H+V.149.mat'; 
%'/net/denali/storage2/radar2/tmp/Ivan/CSU/tookits/RVP9_timeSeries/res/20190125/col-radar.20190125.210914.523.REL_RHI30.2.H+V.149.mat';

PRT1 = 0.0011;
PRT2 = 0.0017;
lambda = 0.05;
chivito = chivo_timeSeries(filename);
%spectrum = chivito.computeSpectrumZdr(285,10);
%spectrum = chivito.computeSpectrum(285,33.7);
spectrum = chivito.computeSpectrum(220,1.3);
spectrum = conv2(spectrum, [1 1 1], 'same');
[r, c] = size(spectrum);

Ts = PRT1;
M = r;
range = 150*(1:c)/1e3; % range in km
vel=velocityaxis(lambda,Ts,M)-0.6;

%%

%spectrum_toPlot = 10*log10(abs(spectrum)); %10*log10(Ts/M*abs(spectrum));
spectrum_toPlot = 10*log10(Ts/M*abs(spectrum));
spectrum_toPlot(spectrum_toPlot < -65) = nan;
height = range*sind(33.7);
figure
pcolor(vel, height, spectrum_toPlot')
shading flat
colormap jet
colorbar
xlabel v(m/s)
ylabel Hight(km)
ylim([0 20])

%%
