import requests
import json
from bs4 import BeautifulSoup

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
    return string.replace(" ", "").replace("\n", "").replace("\r", "")

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
                    summary['peminat'] = removeSpacing(link.findChildren('td')[5].text).replace("\n", "").replace("\r", "")
                    summary['daya_tampung'] =  link.findChildren('td')[4].text
                    daftar_prodi.append(summary)
    
    except IndexError as e:
        return "SISTEM SEDANG SINGKRONISASI"
    return daftar_prodi
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

    # write to json
    with open('kampus.json', 'w') as outfile:
        json.dump(kampus, outfile, indent=4)
   
    
    print(kampus)

if __name__ == "__main__":
    main()
