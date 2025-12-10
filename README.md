# PALS_10_585
## Class project for [10.585 at MIT](https://cheme.mit.edu/wp-content/uploads/2025/08/F25-10.585-ad-flyer.pdf)
### Abstract:
The analysis of angstrom-scale free volume elements (FVEs) is important to understanding the separation performance of polymer membranes. Positron annihilation lifetime spectroscopy (PALS) is a powerful experimental technique to determine a polymer’s free volume distribution (FVD), however its utility is hampered by significant difficulties in fitting experimental PALS spectra. Joo et al. (*J. Mater. Chem. A.*, 2023) determined a bimodal FVD for the archetypal microporous organic polymer (MOP), PIM-1, by using the PALS*fit*3 discrete fitting procedure and peak broadening via uncertainty analysis. In this work, I reanalyze the distribution of Joo et al. by convoluting the distribution back to the PALS spectra and reanalyzing with the MELT continuous fitting procedure. The FVD data of Joo et al. was converted into a positron lifetime distribution using the Tao–Eldrup model. The lifetime distribution was fit to both unimodal and log-normal distributions to regenerate PALS spectra. MELT was able to regenerate the bimodal spectrum with a “risky” initial regularization weight, however, the bimodal spectrum collapsed into a single dominant peak as the initial regularization weight was increased. MELT was able to regenerate the unimodal spectrum with a “safe” initial regularization weight, however, the unimodal distribution separated into a bimodal distribution with as the initial regularization weight was decreased. Nevertheless, regardless of regularization, MELT was able to peak up the dominant features of both spectra. These results highlight the necessity of analyzing the spectra over multiple regularization weights and the importance of not overinterpreting results from PALS spectra.
### How to reproduce the analysis:
All data can be reproduced. To do so, Python and Matlab are required. The steps to reproduce the data are stated below. All references are relative to the PALS_10_585 path.
1.	Gather discrete raw data
	
Submit ```./raw_data/Joo_et_al_Figure10a.png``` to [WebPlotDigitizer](https://apps.automeris.io/wpd4/). The used digitized data can be found in ```./raw_data/raw_data.csv```.

2.	Fit unimodal and bimodal log-normal distributions

Run ```./pipeline/pipeline.py```. This program fits the data of Joo et al. to bimodal and unimodal log-normal distributions using the helper scripts ```./pipeline/fitting.py``` and ```./pipeline/tau_eldrup.py```.

3.	Determine continuous PALS distributions with MELT

Open ```./MELT/bin/m_input.m``` and uncomment the ```tau_mean_sim```, ```tau_stddev_sim```, and ```Int_mean_sim``` variables for either the bimodal or unimodal case (lines 54–61).

Run ```./MELT/bin/looper.m```.

To visualize the results of looper.m, run ```./MELT/bin/plotter.m```.
The plots shown within this paper are available in [Origin](https://www.originlab.com/) format at ```./PALS_10_585.opju```.
### Generative AI Statement:
Brandon C. Tapia states the use of [ChatGPT 5.1](https://chatgpt.com/) for the generation of MATLAB code to automate MELT to multiple optimizations in sequel and for help with the settings required to generate the contour plots shown in Figure 4. ChatGPT generated code was checked for accuracy and approved by Brandon C. Tapia. The use of ChatGPT for this use case is allowed per 10.585 class policy (see “LLM (Artificial Intelligence) Policy” in the class syllabus).