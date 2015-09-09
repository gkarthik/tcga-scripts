import os
import pandas as pd
import numpy as np
import pylab
import matplotlib
import matplotlib.pyplot as plt

path = '/home/skywalker/Documents/TCGA/output/'

'''
df = pd.read_table('BRCA_DF', sep='\t', header = 0)
df = df.set_index('gene_id')
df1 = df.loc['SARS|6301']
df1.plot(kind='line', ax=axes[0])
df2 = df.loc['SARS2|54938']
df2.plot(kind='line', ax=axes[1])
pylab.show()
print(df2)
'''
if __name__=='__main__':
    for cancer_dir in os.listdir(path):
        print('Starting ',cancer_dir)
        c_path = os.sep.join([path, cancer_dir])
        dir_count = len(os.listdir(c_path))
        fig, axes = plt.subplots(nrows=dir_count, figsize=(25,25), sharey=True, squeeze = False)
        fig.suptitle(cancer_dir+" - SARS|6301 ", fontsize="x-large")
        fig.tight_layout()
        for dirpath, dirnames, filenames in os.walk(c_path):
            for index, file in enumerate(filenames):
                if file.endswith('-matrix'):
                    df = pd.DataFrame()
                    df = pd.read_table(os.sep.join([c_path, file]), sep='\t', header = 0)
                    df = df.set_index('gene_id')
                    np.ravel(axes)[index].set_title(file.split('-')[1])
                    df.loc['SARS|6301'].plot(linestyle='-', marker='o', ax=np.ravel(axes)[index])
        fig.savefig(os.sep.join([c_path, cancer_dir+'_SARS.png']))
        plt.close(fig)
        print('Completed ',cancer_dir)


