% Ivan Arias
% 2019/10/15

% This is a set of utilities to analyze time series for CHIVO

classdef chivo_timeSeries
    properties
        Hi
        Hq
        Vi
        Vq
        azimuth
        elevation
        PRT
    end
    
    methods
        function obj = chivo_timeSeries(filename)
            load(filename)
            obj.Hi = HI;
            obj.Hq = HQ;
            obj.Vi = VI;
            obj.Vq = VQ;
            L = length(HI);
            obj.azimuth = nan(1,L);
            obj.elevation = nan(1,L);
            obj.PRT = nan(1,L);
            %Get Azimuth and Elevation from the header
            for i = 1:L
                obj.azimuth(i) = str2double(header_info(i).iAz)*360/65536;
                obj.elevation(i) = str2double(header_info(i).iEl)*360/65536;
                obj.PRT(i) = str2double(header_info(i).iPrevPRT)/71.9502e6;
            end
        end
        
        function spectrum = computeSpectrum(obj, Azimuth, Elevation)
            Index = abs(obj.azimuth - Azimuth) < 0.25 & abs(obj.elevation - Elevation) < 0.25 ...
                & abs(obj.PRT - 0.001) < 0.0005;
            HI = obj.Hi(Index,:);
            HQ = obj.Hq(Index,:);
            x_n = complex(HI,HQ);
            [r,c] = size(x_n);
            Ns =  r;
            X_n = nan(r,c);
            for i = 1:c
                X_n(:,i) = fliplr(fftshift(fft(x_n(:,i).*blackman(r))));
            end
            spectrum = 1/Ns*X_n;            
        end
        
        function spectrum = computeSpectrum_Z(obj, Azimuth, Elevation, PRT, radarConstant)
            Index = abs(obj.azimuth - Azimuth) < 0.63 & abs(obj.elevation - Elevation) < 0.25 ...
                & abs(obj.PRT - PRT) < 0.0005;
            HI = obj.Hi(Index,:);
            HQ = obj.Hq(Index,:);
            x_n = complex(HI,HQ);
            [r,c] = size(x_n);
            Ns =  r;
            range = 150*(1:c);
            X_n = nan(r,c);
            for i = 1:c
                X_n(:,i) = fliplr(fftshift(fft(x_n(:,i).*blackman(r))));
            end
            spectrum = 20*log10(abs(PRT/Ns*X_n)) + 20*log10(range) + radarConstant;            
        end
        
        function spectrum = computeSpectrumZdr(obj, Azimuth, Elevation)
            Index = abs(obj.azimuth - Azimuth) < 0.63 & abs(obj.elevation - Elevation) < 0.25 ...
                & abs(obj.PRT - 0.001) < 0.0005;
            HI = obj.Hi(Index,:);
            HQ = obj.Hq(Index,:);
            VI = obj.Vi(Index,:);
            VQ = obj.Vq(Index,:);
            H_n = complex(HI,HQ);
            V_n = complex(VI,VQ);
            [r,c] = size(H_n);
            X_n = nan(r,c);
            Y_n = nan(r,c);
            for i = 1:c
                X_n(:,i) = fliplr(fftshift(fft(H_n(:,i).*blackman(r))));
                Y_n(:,i) = fliplr(fftshift(fft(V_n(:,i).*blackman(r))));
            end
            spectrum = abs(X_n)./abs(Y_n);        
      
        end
        
    end
    
end

