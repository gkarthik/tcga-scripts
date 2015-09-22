import pandas as pd
import os

path = '/home/prime/Documents/TCGA/data_matrices/'

if __name__=='__main__':
    for dir in os.listdir(path):
        cancer_dir = os.sep.join([path, dir])
        for (dirpath, dirnames, filenames) in os.walk(cancer_dir):
            plot_df = pd.DataFrame()
            print(dirpath)
            for file in filenames:
                df = pd.DataFrame()
                df = pd.read_table(os.sep.join([dirpath, file]), sep='\t')
                plot_df = plot_df.append(df)
            print(plot_df)
            plot_df.to_csv(dirpath+'/main_matrix')
