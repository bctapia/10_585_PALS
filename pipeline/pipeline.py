
import tau_eldrup
import fitting
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path

file_path = Path(__file__).resolve()
data_path = file_path.parent.parent / "raw_data" / "raw_data.csv"

# data from Joo et al. [given as average free volume element diameter (A), relative intensity (%)]
avg_fve_diam, rel_int_percent = np.genfromtxt(data_path, delimiter=',', unpack=True)
rel_int_frac = rel_int_percent/100  # convert intensity to fraction

# convert the free volume distribution to o-Ps lifetime (ns) using the Tau-Eldrup model
avg_fve_lifetime = tau_eldrup.fvd_to_tau(avg_fve_diam)

# fit a bimodal log-normal distribution to the data
params_opt = fitting.perform_fit(0.05, np.log(2), 0.4, 0.15, np.log(8), 0.4, avg_fve_lifetime, rel_int_frac)

# convert lifetimes to ps
avg_fve_lifetime_ps = avg_fve_lifetime * 1000

# convert the parameters to coincide with the data in ps
params_opt_ps = fitting.convert_timescale(params_opt, 1000)

# find area under the each log-normal distribution
area_1 = fitting.area_under_lognormal(params_opt_ps[0],params_opt_ps[2])
area_2 = fitting.area_under_lognormal(params_opt_ps[3],params_opt_ps[5])
total_area = area_1 + area_2

# for equivalent area using a unimodal log-normal, c and sigma now are constrained to 1 DOF
c_mono = 600  # arbitrary but gives good unimodal approximation
sigma_mono = total_area/(np.sqrt(2*np.pi)*c_mono)
params_mono_ps = [c_mono, 8.4, sigma_mono]  # 8.4 is arbitrary but gives good unimodal approximation
area_mono = fitting.area_under_lognormal(params_mono_ps[0],params_mono_ps[2])  # this will equal total_area from above

double_lognormal_ps = fitting.double_lognormal(avg_fve_lifetime_ps, params_opt_ps)  # get the bimodal PDF
single_lognormal_ps = fitting.single_lognormal(avg_fve_lifetime_ps, params_mono_ps)  # get the unimodal PDF

c_1, mu_1, sigma_1, c_2, mu_2, sigma_2 = params_opt_ps  # unpack vars
c_mono, mu_mono, sigma_mono = params_mono_ps  # unpack vars


def print_statistics():
    """
    Run this to get all of the important data from above that we will use later on
    """
    print("=========================DATA FITTING========================")
    print("For the double log-normal distribution:")
    print(f"c_1={c_1:.3f}, mu_1={mu_1:.3f}, sigma_1={sigma_1:.3f}, c_2={c_2:.3f}, mu_2={mu_2:.3f}, sigma_2={sigma_2:.3f}")
    print(f"AUC_1={area_1:.3f}, AUC_2={area_2:.3f}, AUC_total={total_area:.3f}")
    print(f"AUC_1/(AUC_total)={area_1/total_area:.3f}, AUC_2/(AUC_1_total)={area_2/total_area:.3f}")

    print("\nFor the single log-normal distribution:")
    print(f"c_1={c_mono:.3f}, mu_1={mu_mono:.3f}, sigma_1={sigma_mono:.3f}")
    print(f"AUC_1={area_mono:.3f}")
    print(f"AUC_1/(AUC_total)={area_mono/area_mono:.3f}")

    print("\nData to supply for the spectra")
    print("For the double log-normal distribution:")
    print(f"tau_mean_sim = [{np.log(120):.3f} {np.log(380):.3f} {mu_1:.3f} {mu_2:.3f}]")
    print(f"tau_stddev_sim = [0.1 0.1 {sigma_1:.3f} {sigma_2:.3f}]")
    print(f"Int_mean_sim = [0.5 0.1 {(1-0.5-0.1)*(area_1/total_area):.3f} {(1-0.5-0.1)*(area_2/total_area):.3f}]")

    print("\nFor the single log-normal distribution:")
    print(f"tau_mean_sim = [{np.log(120):.3f} {np.log(380):.3f} {mu_mono:.3f}]")
    print(f"tau_stddev_sim = [0.1 0.1 {sigma_mono:.3f}]")
    print(f"Int_mean_sim = [0.5 0.1 {(1-0.5-0.1):.3f}]")
    print("=========================END DATA FITTING========================")


def display_plots():
    """
    Print data plots if interested
    """
    plt.semilogx(avg_fve_lifetime_ps, rel_int_frac)
    plt.semilogx(avg_fve_lifetime_ps, double_lognormal_ps)
    plt.semilogx(avg_fve_lifetime_ps, single_lognormal_ps)
    plt.show()


def print_for_plot():
    """
    Print tabular data that we can use to plot in other softwares
    """
    print("============================lifetime (ps)============================")
    for i, val in enumerate(avg_fve_diam):
        print(val, rel_int_frac[i], avg_fve_lifetime_ps[i], double_lognormal_ps[i], single_lognormal_ps[i])


print_statistics()
#display_plots()
#print_for_plot()