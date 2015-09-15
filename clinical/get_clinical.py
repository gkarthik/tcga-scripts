import csv

path = '/home/skywalker/Downloads/nationwidechildrens.org_clinical_patient_brca.txt'
file = list(csv.reader(open(path, 'r'), delimiter='\t'))
print(len(file))
for attr in file[0]:
    print(attr)
