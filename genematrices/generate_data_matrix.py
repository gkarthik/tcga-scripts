import csv
import os
import numpy as np
import pandas as pd

from numpy import genfromtxt

dir = "/home/skywalker/Documents/TCGA/data/"
dest = '/home/skywalker/Documents/TCGA/output/'

main_df = pd.DataFrame()
metadata = pd.DataFrame()

def appendToDataFrame(filepath, file, main_df, metadata):
    df = pd.read_table(filepath, sep='\t', header = 0)
    df = df.set_index('gene_id')
    sample_name = file.split('.')[2]
    tcga_barcode = metadata.loc[metadata['Extract Name'] == sample_name]['Comment [TCGA Barcode]'].iloc[0]
    df.rename(columns={'normalized_count': tcga_barcode}, inplace=True)
    main_df = main_df.join(df, how='outer')
    return main_df

def get_metadata(c_path):
    metadata_src = os.sep.join([c_path, 'metadata'])
    df = pd.DataFrame()
    for (dirpath, dirnames, filenames) in os.walk(metadata_src):
        if(len(filenames)>1):
            print('Too many metadata files. Exiting ... ')
            sys.exit(0)
        for file in filenames:
            df = pd.read_table(os.sep.join([dirpath, file]), sep='\t', header = 0)
    return df


if __name__ == '__main__':
    for cancer_dir in os.listdir(dir):
        c_path = os.sep.join([dir, cancer_dir])
        for temp_dir in os.listdir(c_path):
            metadata = get_metadata(c_path)
            for dirpath, dirnames, filenames in os.walk(c_path):
                print(dirpath)
                filepath = ''
                if(os.path.dirname(dirpath).endswith('normalized_data')):
                    for file in filenames:
                        filepath = os.path.join(dirpath, file)
                        main_df = appendToDataFrame(filepath, file, main_df, metadata)
                    output_path = os.sep.join([dest, cancer_dir])
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    tumor_type = os.path.basename(os.path.dirname(filepath))
                    output_path = os.sep.join([output_path, cancer_dir+'-'+tumor_type+'-matrix'])
                    print(output_path)
                    main_df = main_df.transpose()
                    main_df.to_csv(output_path, sep='\t')
                    main_df = pd.DataFrame()

#    print(main_df)



