import os
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import csv

src_dir = '/home/optimus/Documents/TCGA/data_matrices/'
sample_type_path = '/home/optimus/Documents/TCGA/sampleType.txt'
disease_study_path = '/home/optimus/Documents/TCGA/diseaseStudy.txt'
result_dir = '/home/optimus/Documents/TCGA/TumorNormal_Matched_Boxplots/'

def create_dict(path):
    sample_type_list = list(csv.reader(open(path, 'r'), delimiter='\t'))
    d = dict()
    for i, sample_type in enumerate(sample_type_list):
        if 1 != 0:
            key = sample_type[0]
            value = sample_type[1]
            d[key] = value
    return d

def get_gene_row(gene, path):
    df = pd.DataFrame()
    df = pd.read_table(path)#(dirpath+'/'+file, sep='\t')
    df = df.set_index('gene_id')
    col = df.xs(gene)
    new_index = []
    for index, i in enumerate(col.index):
        new_index.append(i[0:12])#patient identifier
    col.index = new_index
    return col

def get_col_name(dirpath, file):
    name = file.replace(os.path.basename(dirpath)+'-','').replace('-matrix','')
    name = sample_type_dict[name[0:2]].replace(' ','\n')+'('+name[2:3]+')'
    return name

if __name__=='__main__':
    sample_type_dict = create_dict(sample_type_path)
    disease_study_dict = create_dict(disease_study_path)
    sample_count_df = pd.DataFrame()
    print(disease_study_dict)
    for dir in os.listdir(src_dir):
        cancer_dir = os.sep.join([src_dir, dir])
        for (dirpath, dirnames, filenames) in os.walk(cancer_dir):
            for index0, file0 in enumerate(filenames):
                col0 = get_gene_row('SARS|6301', dirpath+'/'+file0)
                name0 = get_col_name(dirpath, file0)
                df0 = pd.DataFrame()
                df0[name0] = col0
#                print(plot_df)
                result_cancer_dir= result_dir+disease_study_dict[dir.upper()]
                if not os.path.exists(result_cancer_dir):
                    os.makedirs(result_cancer_dir)
                for index, file in enumerate(filenames):
                    plt.clf()
                    plt.figure()
                    plot_df = pd.DataFrame()
                    if index > index0:
                        df = pd.DataFrame()
                        title = get_col_name(dirpath,file0)+'_'+get_col_name(dirpath, file)
                        print('---------'+os.path.basename(dirpath)+'_'+title+'-------------')
                        col = get_gene_row('SARS|6301', dirpath+'/'+file)
                        name = get_col_name(dirpath, file)
                        df[name] = col
                        plot_df = df0.join(df, how='inner')
                        print('Count: '+str(len(plot_df.index)))
                        sample_count_df[os.path.basename(dirpath)+file0+'-'+file] = len(plot_df.index)
                        print(plot_df)
                        if len(plot_df.index) > 0:
                            ax = plot_df.plot(kind='box')
                            ax.set_xlabel('Sample Type')
                            ax.set_ylabel('Normalized expression value of SARS')
                            plt.tight_layout()
                            title = title+'(count='+str(len(plot_df.index))+')'
                            plt.title(title)
                            ax.figure.savefig(result_cancer_dir+'/'+title+'.png')
#    print(sample_count_df)
 #   sample_count_df.to_csv('/home/optimus/Documents/TCGA/sample_count.csv')

