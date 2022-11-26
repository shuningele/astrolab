from bs4 import BeautifulSoup
from datetime import date
import numpy as np
import urllib3
import pandas as pd
import os
telescopes = ['La Palma','east-16', 'far-east-20','west-14']
astrolab = "http://astro.dur.ac.uk/~ams/astrolab/"
tele_urls = ['pt5m/pt5m_2022', 'east_16/east-16_2022', 'far_east_20/far-east-20_2022','west-14_2022']
#user input, date in the format of 22_month_day
last_updated = input("The date from which you want to load into the observing database?")
#extract the date and month when the database is last updated
last_updated_d = int(last_updated.split('_')[-1])
last_updated_m = int(last_updated.split('_')[-2])
today = date.today()
today_f = "22_{}_{}".format(today.month, today.day)
objects = ['sn2022vqz', 'sn2022wpy', 'sn2022wgj', 'sn2022xau', 'at2022xoe', 'sn2022xoe', 'sn2022xou', 'at2022xou']
if today.month == last_updated_m:
    date_range = ["2022_{}_0{}".format(today.month, d) if d<10 else "2022_{}_{}".format(today.month, d) for d in range(last_updated_d, today.day+1)]
else:
    date_range1 = ["2022_{}_0{}".format(last_updated_m, d) if d<10 else "2022_{}_{}".format(last_updated_m, d) for d in range(last_updated_d,32)]
    date_range2 = ["2022_{}_0{}".format(today.month, d) if d<10 else "2022_{}_{}".format(today.month, d) for d in range(1,today.day+1)]
    date_range = date_range1 + date_range2

df = pd.DataFrame(columns = ['Object', 'Date', 'Filter', 'Telescope', 'Start ID : End ID', 'Time (UTC)', 'Mean FWHM', 'Std FWHM'])

for d in date_range:
    for i, telescope in enumerate(telescopes):
        http = urllib3.PoolManager()
        url = astrolab+tele_urls[i]+"/"+d+".html"
        response = http.request('GET',url, headers={"User-Agent": "Mozilla/5.0"})
        file = response.data
        try:
            data = pd.DataFrame(pd.read_html(file, header=1)[0]).iloc[:-1][:]
            data.dropna(inplace=True)
            row_mask = [obj.lower() in objects for obj in data['Object']]
            data = data.loc[row_mask][:]
            for supernova in data['Object'].unique():
                subdata = data.loc[data['Object']==supernova][:]
                a = 1
                for filter in subdata['Filter'].unique():
                    if a==1 and subdata.iloc[0,-1]!= subdata.iloc[1,-1]:
                        remove_first = True
                    a+=1
                    subsub = subdata.loc[subdata['Filter']==filter][:]
                    start_id = min([int(id) for id in subsub['#Run(.fits)']])
                    end_id = max([int(id) for id in subsub['#Run(.fits)']])
                    end_time = subsub.iloc[-1, 5]
                    fwhms = [float(f) for f in subsub.iloc[:,-1]]
                    if remove_first:
                        start_id+=1
                        fwhms = fwhms[1:]
                        remove_first = False
                    fwhm = np.round(np.average(fwhms), 2)
                    std_fwhm = np.round(np.std(fwhms), 2)
                    new_row = pd.Series({'Object': supernova.lower(),'Date': '/'.join(d.split('_')), 'Filter': filter, 'Telescope': telescope, 'Start ID : End ID': "{} : {}".format(start_id, end_id), 'Time (UTC)': end_time, 'Mean FWHM': fwhm, 'Std FWHM': std_fwhm})
                    df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
        except:
            continue
a_w = input("Overwrite or append? ('a' for append, 'w' for overwrite)")
with open('observations_database.csv', a_w) as storage:
    to_write = df.to_csv(index=False)
    storage.write(to_write)



