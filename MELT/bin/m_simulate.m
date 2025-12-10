% m_simulate.m
% simulation of lifetime spectra based on Gaussian distributed exponential decays
% version 5.0, april 2021
% Danny Petschke, Department of Chemistry and Pharmacy, University Wuerzburg
%               Roentgenring 11, Würzburg Germany
% danny.petschke@uni-wuerzburg.de

rng(4234,'twister'); % 8374 

numberOfLifetimes = size(tau_mean_sim,2);

Y = zeros(stopdat,1);

% rough estimate where to place t-zero ...
x = (-25*(1./2.3548)*FWHM(1):psperchannel:(stopdat-1)*psperchannel - 25*(1./2.3548)*FWHM(1))';

all_tau = [];

for n=1:numberOfLifetimes
    y = zeros(stopdat,1);
    
    for k=1:sim_smoothness
        tau = lognrnd(tau_mean_sim(n),tau_stddev_sim(n)); % changed from normrnd
        all_tau(end+1) = tau;
        pd_exp = makedist('Exponential','mu',tau);
        
        y = y + pdf(pd_exp,x);
    end
    
    Y = Y + (y./sum(y)).*Int_mean_sim(n);
end
%figure;
%histogram(all_tau, 'Normalization', 'pdf', 'NumBins', 200);
%xlabel('\tau (ps)');
%ylabel('Estimated PDF');
%title('Histogram estimate of lognormal lifetime PDF');
%grid on;
%input("wait")
Y = Y./sum(Y);

pd_irf = makedist('Normal','mu',0.,'sigma',(1./2.3548)*FWHM(1));
    
y_irf = pdf(pd_irf,x);
y_irf = y_irf./sum(y_irf);

spectrum = real(ifft(fft(Y).*fft(y_irf)));
spectrum = (countsInSpectrum - stopdat*constBkgrd).*spectrum./sum(spectrum);
spectrum = spectrum + constBkgrd;

% make some noise ;)
for m=1:stopdat
    pd_noise = makedist('Normal','mu',0,'sigma',sqrt(spectrum(m))); % poisson noise
    spectrum(m) = spectrum(m) + random(pd_noise,1,1);
end