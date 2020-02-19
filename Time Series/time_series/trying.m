l = length(HI);
Pr = 10*log10(sum((HI.^2+HQ.^2)/l,2));
%dat = chivo_timeSeries('13512.mat');
polar(dat.azimuth, Pr.')



