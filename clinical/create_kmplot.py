from lifelines import KaplanMeierFitter
from lifelines.utils import datetimes_to_durations
from lifelines.statistics import logrank_test
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import csv
import sys,getopt

src_dir = '/home/optimus/Documents/TCGA/clinical_matrices/'
survival_matrices_dir = '/home/optimus/Documents/TCGA/survival_matrices/'
tumor__km_dir = '/home/optimus/Documents/TCGA/kmplots_tumor/'
result_dir = '/home/optimus/Documents/TCGA/kmplots_test/'
disease_study_path = '/home/optimus/Documents/TCGA/diseaseStudy.txt'


def create_dict(path):
    sample_type_list = list(csv.reader(open(path, 'r'), delimiter='\t'))
    d = dict()
    for i, sample_type in enumerate(sample_type_list):
        if 1 != 0:
            key = sample_type[0]
            value = sample_type[1]
            d[key] = value
    return d

def check_value(pvalue):
    if pvalue < 0.05:
        return True

def run_logrank(df1, df2, df3, f, cohorts):
    check = False
    title = '\n('
    if cohorts > 2:
        results = logrank_test(df1['duration'], df2['duration'], df1['event_obs'], df2['event_obs'], alpha=.99)
        f.write('__ p-value ___|__ test statistic __|____ test result ____|__ is significant __\n')
        f.write(str(results.p_value) + ' | ' + str(results.test_statistic)+' | '+str(results.test_result)+ ' | '+str(results.is_significant)+'\n')
        check = check_value(results.p_value)
        title += str(round(results.p_value, 4))
        title += ','
        results = logrank_test(df2['duration'], df3['duration'], df2['event_obs'], df3['event_obs'], alpha=.99)
        f.write('__ p-value ___|__ test statistic __|____ test result ____|__ is significant __\n')
        f.write(str(results.p_value) + ' | ' + str(results.test_statistic)+' | '+str(results.test_result)+ ' | '+str(results.is_significant)+'\n')
        check = check_value(results.p_value)
        title += str(round(results.p_value, 4))
        title += ','
        results = logrank_test(df1['duration'], df3['duration'], df1['event_obs'], df3['event_obs'], alpha=.99)
        f.write('__ p-value ___|__ test statistic __|____ test result ____|__ is significant __\n')
        f.write(str(results.p_value) + ' | ' + str(results.test_statistic)+' | '+str(results.test_result)+ ' | '+str(results.is_significant)+'\n')
        check = check_value(results.p_value)
        title += str(round(results.p_value, 4))
        title += ')'
    else:
        results = logrank_test(df1['duration'], df2['duration'], df1['event_obs'], df2['event_obs'], alpha=.99)
        f.write('__ p-value ___|__ test statistic __|____ test result ____|__ is significant __\n')
        f.write(str(results.p_value) + ' | ' + str(results.test_statistic)+' | '+str(results.test_result)+ ' | '+str(results.is_significant)+'\n')
        check = check_value(results.p_value)
        title += str(round(results.p_value, 4))
        title += ')'
    if check:
        title += "*"
    return title

def plot_km(df, ax, lbl, c_name, percentile):
    km_df = pd.DataFrame()
    df = df.sort_index(by=['duration'], ascending=[True])
    T = df['duration']
    event_obs = []
    for row in df['vital_status']:
        if row == 'Alive':
            event_obs.append(0)
        elif row == 'Dead':
            event_obs.append(1)
        else:
            print(row) 
    df['event_obs'] = event_obs
#    df[['duration', 'event_obs', 'SARS' ]].to_csv(survival_matrices_dir+file+'_'+percentile+'_survival.csv')
    E = df['event_obs']
    kmf.fit(T, event_observed=E, label=lbl)
    kmf.plot(ax = ax, ci_show = False)
    return df

def process_df(df, file, ax, f, cohorts):
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
            vital_status.append('Alive')
        else:
            vital_status.append(row)
    df['vital_status'] = vital_status
    df['SARS'] = df['SARS'].dropna()
    df = df[pd.notnull(df['duration'])]
    df = df[pd.notnull(df['SARS'])]
    df = df[pd.notnull(df['vital_status'])]
    lst = df['SARS'].tolist()
    f.write('\n\n'+disease_study_dict[file.replace('_matrix', '').upper()]+'\n')
    if cohorts > 2:
        q1 = np.percentile(lst, 33.33)
        q2 = np.percentile(lst,66.66)
        q1 = round(q1)
        q2 = round(q2)
        df1 = df[df['SARS']<=q1]
        df2 = df[(df['SARS']>q1) & (df['SARS'] <= q2)]
        df3 = df[df['SARS']>q2]
        df1 = plot_km(df1, ax, '<'+str(q1)+'('+str(len(df1.index))+')', file, "q1")
        df2 = plot_km(df2, ax, '>='+str(q1)+' & <'+str(q2)+'('+str(len(df2.index))+')', file, "q2")
        df3 = plot_km(df3, ax, '>'+str(q2)+'('+str(len(df3.index))+')', file, "q3")
        significance = run_logrank(df1, df2, df3, f, cohorts)
    else:
        q1 = np.percentile(lst, 50.00)
        q1 = round(q1)
        df1 = df[df['SARS']<=q1]
        df2 = df[df['SARS']>q1]
        df1 = plot_km(df1, ax, '<'+str(q1)+'('+str(len(df1.index))+')', file, "q1")
        df2 = plot_km(df2, ax, '>='+str(q1)+'('+str(len(df2.index))+')', file, "q2")
        significance = run_logrank(df1, df2, None, f, cohorts)
    plt.title(disease_study_dict[file.replace('_matrix', '').upper()]+'(n='+str(len(df.index))+')'+significance)
    check = ''
    if '*' in significance:
        check = '*'
    ax.get_figure().savefig(result_dir+disease_study_dict[file.replace('_matrix', '').upper()]+'(n='+str(len(df.index))+')'+check+'.png')


def main(argv):
    cohorts = 2
    try:
        opts, args = getopt.getopt(argv,"hn:",["cohorts"])
    except getopt.GetoptError:
        print('tcreate_kmplot.py -n <number of cohorts>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('create_kmplot.py -n <number of cohorts>')
            sys.exit()
        elif opt in ("-i", "--cohorts"):
            cohorts = arg
    return cohorts

if __name__=='__main__':
    cohorts = main(sys.argv[1:])
    disease_study_dict = create_dict(disease_study_path)
    f = open(result_dir+'result_summary.txt', 'a')
    for (dirpaths, dirnames, filenames) in os.walk(src_dir):
        for file in filenames:
            kmf = KaplanMeierFitter()
            ax = plt.subplot(111)
            print(file)
            df = pd.read_table(src_dir+file, sep=',', header = 1)
            process_df(df, file, ax, f, cohorts)
            plt.clf()
