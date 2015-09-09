import os
import pandas as pd
import matplotlib.pyplot as plt
import itertools

src_dir = '/home/skywalker/Documents/TCGA/output/'

if __name__=='__main__':
    for dir in os.listdir(src_dir):
        cancer_dir = os.sep.join([src_dir, dir])
        for (dirpath, dirnames, filenames) in os.walk(cancer_dir):
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
                    name = file.replace(os.path.basename(dirpath)+'-','').replace('-matrix','')+'(n='+str(count)+')'
                    col = col.reset_index(level=0, drop = True)
                    plot_df[name] = col
            plot_df.plot(kind='box').figure.savefig('/home/skywalker/Documents/TCGA/boxplots_count/'+dir+'_boxplot.png')

