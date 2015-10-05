import pandas as pd
import os

src_path = '/home/optimus/Documents/TCGA/clinical_matrices/'
dest_path = '/home/optimus/Documents/TCGA/clinical_matrices_R/'

for dir in os.listdir(src_path):
    for (dirname, dirpath, filenames) in os.walk(src_path+dir):
        for file in filenames:
            df = pd.read_table(dirname+'/'+file, sep='\t')
            df = df.transpose()
            df.columns = df.iloc[0]
            print(df.columns)
            dest_dir = dest_path+os.path.split(dirname)[1]+'/'
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            print(dest_dir)
            
            df.to_csv(dest_dir+file, sep='\t', header=False)
