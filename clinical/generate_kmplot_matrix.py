import pandas as pd
import os
import string

src_path = '/home/optimus/Documents/TCGA/main_matrices/'
clinical_path = string.Template('/home/optimus/Documents/TCGA/clinical_data/nationwidechildrens.org_clinical_patient_${c_abbv}.txt')
result_path = '/home/optimus/Documents/TCGA/clinical_matrices/'

def create_kmpot_matrix(src_path, clinical_path,  result_path, c):
    clinical_df = pd.DataFrame()
    print(clinical_path)
    clinical_df = pd.read_table(clinical_path, sep='\t', encoding='iso8859_15')
    clinical_df = clinical_df.set_index('bcr_patient_barcode')
    gene_df = pd.read_table(src_path, sep=',')
    gene_df = gene_df.set_index('gene_id')
    header = []
    for row in list(gene_df.columns.values):
        header.append(row[0:12])
    gene_df.columns = (header)
#    print(gene_df.loc['SARS|6301']['TCGA-AC-A6IX'].tolist())
    error_list = []
    col = []
    outliers = []
    for i, index in enumerate(clinical_df.index):
        if index in list(gene_df.columns.values):
            cell = gene_df.loc['SARS|6301'][index].tolist()
            value = cell
            if isinstance(cell, list):
                outliers.append(index)
                value = cell[0]
            col.append(float(value))
        elif i == 0:
            col.append('SARS')
        else:
            col.append(float('nan'))
#            outliers.append(index)
    clinical_df['SARS'] = col
    print(clinical_df['SARS'])
    print(outliers)
    clinical_df.to_csv(result_path+c+'_matrix')

if __name__=='__main__':
    for (dirpath, dirnames, filenames) in os.walk(src_path):
        for file in filenames:
            c = file.replace('_main_matrix','')
            create_kmpot_matrix(src_path+file, clinical_path.substitute({'c_abbv': c}), result_path, c)



