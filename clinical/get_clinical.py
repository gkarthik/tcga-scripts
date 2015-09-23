import csv
import pandas as pd

path = '/home/optimus/Downloads/nationwidechildrens.org_clinical_patient_brca.txt'
df = pd.DataFrame()
df = pd.read_table(path, sep='\t')
print(df)

