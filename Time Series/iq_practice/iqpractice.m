dat = dlmread('iqdat.txt', '\t', 2);
in_q = dat(:,3);
in_i = dat(:,4);
fin_q = fft(in_q);
fin_i = fft(in_i);
nnz(isnan(fin_q))          %gives 0 -- none of the values are nan
nnz(isnan(fin_i))          %gives 0 -- none of the values are nan
subplot(1,2,1); plot(abs(fin_q)); title('abs fft of in_q');
subplot(1,2,2); plot(abs(fin_i)); title('abs fft of in_i');

datobj = chivo_timeSeries('13512)