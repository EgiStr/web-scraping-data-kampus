import requests
import json
from bs4 import BeautifulSoup

# URL = "https://sidata-ptn.ltmpt.ac.id/ptn_sn.php"
# MY_PRODI = ["Sistem Informasi",'informatika','teknik informatika','Ilmu Komputasi','Ilmu Komputer', 'Matematika Komputasi',"teknologi informasi",'Manajemen Informatika','sains data','data sains','data science','komputer sains','computer science','PERANGKAT LUNAK','sofware']
MY_PRODI = ["gizi",'pangan','industri pangan']
# MY_PRODI = ["industri gizi"]

class Request:
    def __init__(self, url,my_prodi,file_name):
        self.domain = ["https://sidata-ptn.ltmpt.ac.id/ptn_sn.php","https://sidata-ptn.ltmpt.ac.id/ptn_sb.php"]
        self.URL = self.domain[url]
        self.MY_PRODI = my_prodi
        self.html = getRequest(self.URL)
        self.soup = getSoup(self.html)
        self.tbody = self.soup.findChildren('tbody')
        self.tr = self.tbody[0].findChildren('tr')
        self.link= self.tr[0]
        self.kampus = []
        self.file_name = file_name

    
    def getRequest(self,url):
        #  get request and get raw html
        r = requests.get(url)
        html = r.text
        return html

    def removeDuplicateList(self,list):
        # remove duplicate list
        return list(set(list))

    def removeSpacing(self,string):
        return string.replace(" ", "").replace("\n", "").replace("\r", "").replace(".", "")

    def lowercase(self,string):
        return string.lower()

    def isProdi(self,prodi,target):
        
        prodi = self.lowercase(removeSpacing(prodi))
        for i in target:
            i = self.lowercase(removeSpacing(i))
            if i in prodi:
                return True
        return False

    def getSoup(self,html):
        #  get soup
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def getLinks(self,soup):
        #  get all links
        links = soup.find_all('a')
        return links

    def sortListofObject(self,kampus):
        # sort list of object
        kampus.sort(key=lambda x: x['prodi'][0].get("keketatan",0) if x['prodi'] and len(x['prodi']) > 0 else 0 , reverse=True)
        return kampus

    def findProdi(self,url):
        daftar_prodi = []
        try:
            html = self.getRequest(self.URL+url)
            soup = self.getSoup(html)
            tbodys = soup.findChildren('tbody')
            for tbody in tbodys:
                tr = tbody.findChildren('tr')
                for link in tr:
                    if self.lowercase(link.findChildren('td')[3].text) == "s1":
                        if self.isProdi(link.findChildren('td')[2].findChildren('a')[0].text,self.MY_PRODI):
                            summary = {}
                            summary['jenjang'] = link.findChildren('td')[3].text
                            summary['prodi'] = link.findChildren('td')[2].findChildren('a')[0].text
                            summary['peminat_2021'] = int(removeSpacing(link.findChildren('td')[5].text).replace("\n", "").replace("\r", ""))
                            summary['daya_tampung_2022'] =  int(link.findChildren('td')[4].text)
                            summary['keketatan'] =  float(summary.get('peminat_2021'))/float(summary.get('daya_tampung_2022'))
                            daftar_prodi.append(summary)
            return daftar_prodi
        except IndexError as e:
            print(e)
            return []

    def getKampus(self):
        for link in self.tr:
            self.kampus.append({
                'universitas': link.findChildren('td')[2].findChildren('a')[0].text,
                "prodi":self.findProdi(link.findChildren('td')[2].findChildren('a')[0].get('href'))
            })
            
        self.kampus = self.sortListofObject(self.kampus)
        return self.kampus

    def start(self):
        with open(f'{self.file_name}.json', 'w') as outfile:
            json.dump(self.getKampus(), outfile, indent=4)



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
        tbodys = soup.findChildren('tbody')
        for tbody in tbodys:
            tr = tbody.findChildren('tr')
            for link in tr:
                if lowercase(link.findChildren('td')[3].text) == "s1":
                    if isProdi(link.findChildren('td')[2].findChildren('a')[0].text,MY_PRODI):
                        summary = {}
                        summary['jenjang'] = link.findChildren('td')[3].text
                        summary['prodi'] = link.findChildren('td')[2].findChildren('a')[0].text
                        summary['peminat_2021'] = int(removeSpacing(link.findChildren('td')[5].text).replace("\n", "").replace("\r", ""))
                        summary['daya_tampung_2022'] =  int(link.findChildren('td')[4].text)
                        summary['keketatan'] =  float(summary.get('peminat_2021'))/float(summary.get('daya_tampung_2022'))
                        daftar_prodi.append(summary)
        return daftar_prodi
    except IndexError as e:
        print(e)
        return []

def main():    
    kampus = []
    html = getRequest(URL)
    soup = getSoup(html)
    tbody = soup.findChildren('tbody')

    tr = tbody[0].findChildren('tr')
    link= tr[0]

    for link in tr:
        kampus.append({
            'universitas': link.findChildren('td')[2].findChildren('a')[0].text,
            "prodi":findProdi(link.findChildren('td')[2].findChildren('a')[0].get('href'))
        })

    kampus = sortListofObject(kampus)
    # # write to json
    with open('kampusPanganSBMPTN2022.json', 'w') as outfile:
        json.dump(kampus, outfile, indent=4)
  
if __name__ == "__main__":
    Kampus = Request(1,['dokter'],'kampusDokter2022')
    Kampus.start()