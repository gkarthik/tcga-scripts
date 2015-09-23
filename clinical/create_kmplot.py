from lifelines import KaplanMeierFitter
import pandas as pd
import matplotlib.pyplot as plt
import os

src_dir = '/home/optimus/Documents/TCGA/clinical_matrices/'
result_dir = '/home/optimus/Documents/TCGA/kmplots/'

def plot_km(df, ax, lbl):
    T = df['duration']
    event_obs = []
    for row in df['vital_status']:
        if row == 'Alive':
            event_obs.append(1)
        elif row == 'Dead':
            event_obs.append(0)
        else:
            print(row) 
    df['event_obs'] = event_obs
    E = df['event_obs']
    kmf.fit(T, event_observed=E, label=lbl)
    kmf.plot(ax = ax, ci_show=False)

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
    avg = sum(lst)/len(lst)
    df1 = df[df['SARS']<avg]
    df2 = df[df['SARS']>=avg]
    plot_km(df1, ax, '<'+str(avg))
    plot_km(df2, ax, '>='+str(avg))
    ax.get_figure().savefig(result_dir+file+'_kmplot.png')


if __name__=='__main__':
    for (dirpaths, dirnames, filenames) in os.walk(src_dir):
        for file in filenames:
            kmf = KaplanMeierFitter()
            ax = plt.subplot(111)
            print(file)
            df = pd.read_table(src_dir+file, sep=',', header = 1)
            process_df(df, file, ax)
            plt.clf()
