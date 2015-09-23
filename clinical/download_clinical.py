import requests
import string
import os

from bs4 import BeautifulSoup


download_url_tmpl = string.Template('https://tcga-data.nci.nih.gov/tcgafiles/ftp_auth/distro_ftpusers/anonymous/tumor/${cancer_abbv}/bcr/biotab/clin/nationwidechildrens.org_clinical_patient_${cancer_abbv}.txt')
cancer_list_url = 'https://tcga-data.nci.nih.gov/tcgafiles/ftp_auth/distro_ftpusers/anonymous/tumor/'
root_directory = '/home/optimus/Documents/TCGA/clinical_data/'


def download_file(url, dir):
    print(url)
    local_filename = dir+url.split('/')[-1]
    r = requests.get(url, stream=True)
    try:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return local_filename
    except requests.exceptions.HTTPError:
        return r.status_code

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
    print(download_file(download_url_tmpl.substitute({'cancer_abbv': c.replace('/','')}), root_directory))
