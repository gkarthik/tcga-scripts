import os
import shutil

path='/home/skywalker/Documents/TCGA/data/'

if __name__== '__main__':
    list_of_files = {}
    sdrf_count = 0
    normalized_count = 0
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            src = os.sep.join([dirpath, filename])
            dest = os.path.dirname(dirpath)
            print('Copying ',src)
            if filename.endswith('.genes.normalized_results'):
                if not os.path.exists(dest+'/normalized_data/'):
                    os.makedirs(dest+'/normalized_data/')
                shutil.copyfile(src, dest+'/normalized_data/'+filename)
                normalized_count+=1
            elif filename.endswith('.sdrf.txt'):
                if not os.path.exists(dest+'/metadata/'):
                    os.makedirs(dest+'/metadata/')
                shutil.copyfile(src, dest+'/metadata/'+filename)
                sdrf_count+=1
