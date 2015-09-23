import pandas as pd
import os

path = '/home/optimus/Documents/TCGA/data_matrices/'
result_dir = '/home/optimus/Documents/TCGA/main_matrices/'

if __name__=='__main__':
    for dir in os.listdir(path):
        cancer_dir = os.sep.join([path, dir])
        for (dirpath, dirnames, filenames) in os.walk(cancer_dir):
            plot_df = pd.DataFrame()
            print(dirpath)
            for file in filenames:
                if len(file.split('-')) < 2:
                    continue
                if int(file.split('-')[1][0:2]) <= 9:
                    df = pd.DataFrame()
                    df = pd.read_table(os.sep.join([dirpath, file]), sep='\t')
                    df = df.set_index('gene_id')
                    plot_df = plot_df.join(df, how='outer')
#                plot_df = plot_df.set_index('gene_id')
            print(plot_df)
            plot_df.to_csv(result_dir+'/'+dir+'_main_matrix')
