import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from astropy.time import Time
#filename = input("filename containing the magnitude data to be plotted (single object, single filter):")
#hdr = input("which row [0-indexed] contains the column headers? ('n' for none)")
#fil_name = input("Which filter is the magnitudes for?")
#try:
#    hdr = int(hdr)
#except:
#    hdr = None
    
df_V = pd.read_csv("vqz_V_med.csv", header=0)
df_B = pd.read_csv("vqz_B_med.csv", header=0)
#always assume the leading columns to be provided in the order of date, time, magnitude and error.
#assume the format of date is year/month/date
date_Vs = df_V.iloc[:,0]
date_Bs = df_B.iloc[:,0]
#utc_times = df_V.iloc[:,1]
mag_Vs = df_V.iloc[:,2]
mag_Bs = df_B.iloc[:,2]
#date_B_max = df_B[df_B["magnitude"]==min(df_B["magnitude"]),"date"]
#print(date_B_max)
V_errs = df_V.iloc[:,3]
B_errs = df_B.iloc[:,3]
tels_V = df_V.iloc[:,4]
tels_B = df_B.iloc[:,4]
tot = df_B.merge(df_V, how="inner", on=["date", "telescope"],suffixes=('_B', '_V'))
color = 0.2
mjd_B_max = Time(df_B.iloc[4,0])
mjd_B_max.format = "mjd"
for telescope in tot["telescope"].unique():
    sub = tot.loc[tot["telescope"]==telescope]
    B_V = sub["magnitude_B"]-sub["magnitude_V"]
    B_V_err = sub["mag_err_B"]+sub["mag_err_V"]
    times = [Time(date) for date in sub["date"]]
    for time in times:
        time.format = "mjd"
    plt.errorbar(x=[int(time.value)-mjd_B_max.value for time in times], y=B_V, yerr= B_V_err, color=str(color),fmt='.', capthick=1, capsize = 2, label=telescope)
    color+=0.3
    plt.xlabel("JD – "+str(int(mjd_B_max.value)))
    plt.ylabel("B – V")
plt.legend()
plt.show()
#hrs = [int(utc_t.split(':')[0]) for utc_t in utc_times]
#unmod_times = [Time(date+' '+time, scale='utc').mjd for date, time in zip(dates, utc_times)]
#mod_times  = [t+1 if hrs[i]>=0 and hrs[i]<=6 else t for i, t in enumerate(unmod_times)]
#fig, ax = plt.subplots()
#ax.set_ylim((max(mags)+0.2, min(mags)-0.2))
#ax.errorbar(unmod_times, mags, yerr = errs, fmt='.', capthick=1, capsize = 2)
#ax.set_xlabel("Date")
#ax.set_ylabel("Magnitude (V)")
#ax.set_title(filename)
##ax.set_xticklabels(labels = np.around(times, 2), rotation=25)
#fig.tight_layout()
#plt.show()
#with open('sn2022vqz.txt',"a+") as vqz:
#    vqz.write("filter "+fil_name+'\n')
#    for i in range(len(unmod_times)):
#        text = " ".join([str(unmod_times[i]),str(mags[i]), str(errs[i])])+'\n'
#        vqz.write(text)
