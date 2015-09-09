import requests
import string
import os

from bs4 import BeautifulSoup
from distutils.version import LooseVersion, StrictVersion

download_url_tmpl = string.Template('https://tcga-data.nci.nih.gov/tcgafiles/ftp_auth/distro_ftpusers/anonymous/tumor/${cancer_abbv}cgcc/unc.edu/illuminahiseq_rnaseqv2/rnaseqv2/')
cancer_list_url = 'https://tcga-data.nci.nih.gov/tcgafiles/ftp_auth/distro_ftpusers/anonymous/tumor/'
root_directory = '/home/skywalker/Documents/TCGA/data/'

def get_all_archives(c):
    print(download_url_tmpl.substitute({'cancer_abbv':c}))
    r = requests.get(download_url_tmpl.substitute({'cancer_abbv':c}))
    if r.status_code == 404:
        return
        yield
    soup = BeautifulSoup(r.text, "lxml")
    for a in soup.find_all('a'):
        if '.tar.gz' in a.string and 'md5' not in a.string:
            yield a['href']

def download_latest_archive(cancer_abbv):
    archives = get_all_archives(cancer_abbv)
    archive_latest = 'unc.edu.Level_3.0.0.0.tar.gz'
    metadata_latest = 'unc.edu.mage-tab.0.0.0.tar.gz'
    count = 0
    for a in archives:
        if 'Level_3' in a:
            archive_latest = get_latest_archive(a, archive_latest)
        if 'mage-tab' in a:
            metadata_latest = get_latest_metadata(a, metadata_latest)
        count+=1
    #count = 0 implies no archives present
    if count == 0:
        return
    dir = os.path.join(root_directory, cancer_abbv)
    if not os.path.exists(dir):
        os.makedirs(dir)
    archive_url = download_url_tmpl.substitute({'cancer_abbv': cancer_abbv})+archive_latest
    metadata_url = download_url_tmpl.substitute({'cancer_abbv': cancer_abbv})+metadata_latest
    print('Downloading archive from '+ archive_url)
    download_file(archive_url, dir)
    print('Downloading metadata from '+ metadata_url)
    download_file(metadata_url, dir)
    print('--------------------------------------------------------')


def download_file(url, dir):
    local_filename = dir+url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename

def get_latest_archive(version, l_version):
    v = version.split('Level_3.')[1].replace('.tar.gz', '')
    lv = l_version.split('Level_3.')[1].replace('.tar.gz', '')
    if StrictVersion(v) > StrictVersion(lv):
        return version
    else:
        return l_version

def get_latest_metadata(version, l_version):
    v = version.split('mage-tab.')[1].replace('.tar.gz', '')
    lv = l_version.split('mage-tab.')[1].replace('.tar.gz', '')
    if StrictVersion(v) > StrictVersion(lv):
        return version
    else:
        return l_version

def get_cancer_list():
    r = requests.get(cancer_list_url)
    soup = BeautifulSoup(r.text, "lxml")
    for a in soup.find_all('a'):
        href = a['href']
        if a.string.endswith('/') and href.endswith('/') and 'lost+found' not in href:
            yield a['href']
        else:
            continue

cancer_list = get_cancer_list()
for c in cancer_list:
    print(c)
    download_latest_archive(c)
