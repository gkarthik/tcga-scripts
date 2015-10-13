from lifelines import KaplanMeierFitter
from lifelines.utils import datetimes_to_durations
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

src_dir = '/home/optimus/Documents/TCGA/clinical_matrices/'
survival_matrices_dir = '/home/optimus/Documents/TCGA/survival_matrices/'
tumor__km_dir = '/home/optimus/Documents/TCGA/kmplots_tumor/'
result_dir = '/home/optimus/Documents/TCGA/kmplots_3div/'



def plot_km(df, ax, lbl, c_name, percentile):
    km_df = pd.DataFrame()
    df = df.sort_index(by=['duration'], ascending=[True])
    duration_diff = []
#    print(min)
    for i,row in enumerate(df['duration']):
        if i < (len(df.index)-1):
            duration_diff.append(df['duration'][df.index[i+1]] - row)
        else:
            duration_diff.append(1)
    df['duration_diff'] = duration_diff
    T = df['duration']
#    print(T)
    event_obs = []
    for row in df['vital_status']:
        if row == 'Alive':
            event_obs.append(0)
        elif row == 'Dead':
            event_obs.append(1)
        else:
            print(row) 
    df['event_obs'] = event_obs
    #df[['duration', 'event_obs', 'SARS' ]].to_csv(survival_matrices_dir+file+'_'+percentile+'_survival.csv')
    E = df['event_obs']
    kmf.fit(T, event_observed=E, label=lbl)
    kmf.plot(ax = ax, ci_show = False)

def process_df(df, file, ax):
    duration_val = []
    for index, row in enumerate(df['days_to_death']):
        if row == '[Not Applicable]':
            duration_val.append(df['days_to_last_followup'][index])
        else:
            duration_val.append(row)
    df['duration'] = duration_val
    df['duration'] = df['duration'].convert_objects(convert_numeric = True).dropna()
    vital_status = []
    for row in df['vital_status']:
        if row not in ['Alive', 'Dead']:
            vital_status.append(None)
        else:
            vital_status.append(row)
    df['vital_status'] = vital_status
    df['SARS'] = df['SARS'].dropna()
    df = df[pd.notnull(df['duration'])]
    df = df[pd.notnull(df['SARS'])]
    df = df[pd.notnull(df['vital_status'])]
    lst = df['SARS'].tolist()
    q1 = np.percentile(lst, 33.33)
    q2 = np.percentile(lst,66.66)
    df1 = df[df['SARS']<=q1]
    df2 = df[(df['SARS']>q1) & (df['SARS'] <= q2)]
    df3 = df[df['SARS']>q2]
    plot_km(df, ax, '', file, "q1")
    ax.get_figure().savefig(result_dir+file+'_kmplot(samples='+str(len(df.index))+').png')



if __name__=='__main__':
    for (dirpaths, dirnames, filenames) in os.walk(src_dir):
        for file in filenames:
            kmf = KaplanMeierFitter()
            ax = plt.subplot(111)
            print(file)
            df = pd.read_table(src_dir+file, sep=',', header = 1)
            process_df(df, file, ax)
            plt.clf()
