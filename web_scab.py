import requests
import json
from bs4 import BeautifulSoup
import math

URL = "https://sidata-ptn.ltmpt.ac.id/ptn_sn.php"
MY_PRODI = ["Sistem Informasi",'informatika','teknik informatika','Ilmu Komputasi','Ilmu Komputer', 'Matematika Komputasi',"teknologi informasi",'Manajemen Informatika']


def getRequest(url):
    #  get request and get raw html
    r = requests.get(url)
    html = r.text
    return html

def removeDuplicateList(list):
    # remove duplicate list
    return list(set(list))

def removeSpacing(string):
    return string.replace(" ", "").replace("\n", "").replace("\r", "").replace(".", "")

def lowercase(string):
    return string.lower()

def isProdi(prodi,target):
    
    prodi = lowercase(removeSpacing(prodi))
    for i in target:
        i = lowercase(removeSpacing(i))
        if i in prodi:
            return True
    return False

def getSoup(html):
    #  get soup
    soup = BeautifulSoup(html, "html.parser")
    return soup

def getLinks(soup):
    #  get all links
    links = soup.find_all('a')
    return links

def sortListofObject(kampus):

    # sort list of object
    kampus.sort(key=lambda x: x['prodi'][0].get("keketatan",0) if x['prodi'] and len(x['prodi']) > 0 else 0 , reverse=True)
    return kampus


def kampus():
    pass

def findProdi(url):
    daftar_prodi = []
    try:
        html = getRequest(URL+url)
        soup = getSoup(html)
        tbody = soup.findChildren('tbody')

        tr = tbody[0].findChildren('tr')
        
        for link in tr:
            if lowercase(link.findChildren('td')[3].text) == "s1":
                if isProdi(link.findChildren('td')[2].findChildren('a')[0].text,MY_PRODI):
                    summary = {}
                    summary['jenjang'] = link.findChildren('td')[3].text
                    summary['prodi'] = link.findChildren('td')[2].findChildren('a')[0].text
                    summary['peminat_2020'] = int(removeSpacing(link.findChildren('td')[5].text).replace("\n", "").replace("\r", ""))
                    summary['daya_tampung_2021'] =  int(link.findChildren('td')[4].text)
                    summary['keketatan'] =  float(summary.get('peminat_2020'))/float(summary.get('daya_tampung_2021'))
                    daftar_prodi.append(summary)
        return daftar_prodi
    except IndexError as e:
        return []

def main():    
    kampus = []
    html = getRequest(URL)
    soup = getSoup(html)
    tbody = soup.findChildren('tbody')

    tr = tbody[0].findChildren('tr')

    for link in tr:
        kampus.append({
            'universitas': link.findChildren('td')[2].findChildren('a')[0].text,
            "prodi":findProdi(link.findChildren('td')[2].findChildren('a')[0].get('href'))
        })

    kampus = sortListofObject(kampus)
    # # write to json
    with open('kampusInformatika.json', 'w') as outfile:
        json.dump(kampus, outfile, indent=4)
    # read kampus.json 
    # write and read kampusInformatika.json
    # with open('kampusInformatika.json', 'wr') as f:
    #     kampus = json.load(f)
    
    #     # sortListofObject(kampus)
    #     print(sortListofObject(kampus))
    
if __name__ == "__main__":
    main()
