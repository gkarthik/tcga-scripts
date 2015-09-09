import tarfile, os

path = '/home/skywalker/Documents/TCGA/data/'
 
def untar(fname, dirpath):
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname)
        tar.extractall(path=dirpath)
        tar.close()
        print("Extracted in ", fname)
    else:
        print("Not a tar.gz file")
 
if __name__ == '__main__':
    list_of_files = {}
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            list_of_files[filename] = os.sep.join([dirpath, filename])
            untar(list_of_files[filename], dirpath)

    print(len(list_of_files))

#    untar(sys.argv[1])
