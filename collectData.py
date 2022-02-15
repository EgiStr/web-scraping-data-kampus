import requests
import json
from bs4 import BeautifulSoup
from jsontoexcel import JsonToExcel

class Request:
    def __init__(self, url,my_prodi,file_name):
        self.domain = ["https://sidata-ptn.ltmpt.ac.id/ptn_sn.php","https://sidata-ptn.ltmpt.ac.id/ptn_sb.php"]
        self.URL = self.domain[url]
        self.MY_PRODI = my_prodi
        self.html = self.getRequest(self.URL)
        self.soup = self.getSoup(self.html)
        self.tbody = self.soup.findChildren('tbody')
        self.tr = self.tbody[0].findChildren('tr')
        self.link= self.tr[0]
        self.kampus = []
        self.file_name = file_name

    def getSoup(html):
        #  get soup
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def getLinks(soup):
        #  get all links
        links = soup.find_all('a')
        return links

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
        
        prodi = self.lowercase(self.removeSpacing(prodi))
        for i in target:
            i = self.lowercase(self.removeSpacing(i))
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
                            summary['peminat_2021'] = int(self.removeSpacing(link.findChildren('td')[5].text).replace("\n", "").replace("\r", ""))
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
        with open(f'excel/{self.file_name}.json', 'w') as outfile:
            json.dump(self.getKampus(), outfile, indent=4)
        json_file = JsonToExcel(f'excel/{self.file_name}.json',f'excel/{self.file_name}.xlsx')
        json_file.convert()
        json_file.close()
        print("DONE !!")

