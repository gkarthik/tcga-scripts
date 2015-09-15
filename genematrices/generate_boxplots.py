import os
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import csv

src_dir = '/home/skywalker/Documents/TCGA/output/'
sample_type_path = '/home/skywalker/Documents/TCGA/sampleType.txt'
disease_study_path = '/home/skywalker/Documents/TCGA/diseaseStudy.txt'

def create_dict(path):
    sample_type_list = list(csv.reader(open(path, 'r'), delimiter='\t'))
    d = dict()
    for i, sample_type in enumerate(sample_type_list):
        if 1 != 0:
            key = sample_type[0]
            value = sample_type[1]
            d[key] = value
    return d

if __name__=='__main__':
    sample_type_dict = create_dict(sample_type_path)
    disease_study_dict = create_dict(disease_study_path)
    print(disease_study_dict)
    for dir in os.listdir(src_dir):
        cancer_dir = os.sep.join([src_dir, dir])
        for (dirpath, dirnames, filenames) in os.walk(cancer_dir):
            plt.clf()
            plt.figure()
            plot_df = pd.DataFrame()
            for index, file in enumerate(filenames):
                if file.endswith('-matrix'):
                    print('---------'+os.path.basename(dirpath)+'-------------')
                    df = pd.DataFrame()
                    df = pd.read_table(dirpath+'/'+file, sep='\t')
                    df = df.set_index('gene_id')
                    col = df.xs('SARS|6301')
                    count = col.count()
                    name = file.replace(os.path.basename(dirpath)+'-','').replace('-matrix','')
                    name = sample_type_dict[name[0:2]].replace(' ','\n')+'('+name[2:3]+')'+'\n(n='+str(count)+')'
                    col = col.reset_index(level=0, drop = True)
                    plot_df[name] = col
            ax = plot_df.plot(kind='box')
            ax.set_xlabel('Sample Type')
            ax.set_ylabel('Normalized expression value of SARS')
            plt.tight_layout()
            title = disease_study_dict[dir.upper()]
            plt.title(title)
            ax.figure.savefig('/home/skywalker/Documents/TCGA/boxplots_count_label/'+title+'('+dir+').png')
