import xlsxwriter
import json
import os



class JsonToExcel:
    def __init__(self, json_file_path, excel_file_path):
        self.json_file_path = json_file_path
        self.excel_file_path = excel_file_path
        self.workbook = xlsxwriter.Workbook(self.excel_file_path)
        self.worksheet = self.workbook.add_worksheet()
        self.row = 0    
        self.colomn = 0
        self.headerFomat = self.workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',})
        self.dataFormat = self.workbook.add_format({'align': 'center', 'valign': 'vcenter',})
    

    def convert(self):
        if not os.path.exists(self.json_file_path):
            raise Exception('JSON file does not exist: {}'.format(self.json_file_path))

        with open(self.json_file_path, 'r') as f:
            data = json.load(f)

        self.write_header()
        self.write_data(data)
 

    def write_header(self):
 
        for i, header in enumerate(['Universitas', 'Jurusan', 'Jenjang', 'Peminat 2021', 'Daya Tampung 2022', 'Keketatan']):
            self.worksheet.write_row(0, i, [header],self.headerFomat)

        self.row += 1

    def write_data(self,data):
        for row in data:

            row_data = [row.get('universitas')]
            self.worksheet.write_row(self.row, 0, row_data, self.dataFormat)
  
            for colomn in row.get("prodi"):

                row_data = [colomn.get('prodi'), colomn.get('jenjang'), colomn.get('peminat_2021'), colomn.get('daya_tampung_2022'), colomn.get('keketatan')]
                self.worksheet.write_row(self.row, 1, [row_data[1-1]], self.dataFormat)
                self.worksheet.write_row(self.row, 2, [row_data[2-1]], self.dataFormat)
                self.worksheet.write_row(self.row, 3, [row_data[3-1]], self.dataFormat)
                self.worksheet.write_row(self.row, 4, [row_data[4-1]], self.dataFormat)
                self.worksheet.write_row(self.row, 5, [ "1 : " + str(int(row_data[5-1]))], self.dataFormat)
                self.row += 1
    
    
 
    def close(self):
        self.workbook.close()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Convert JSON to XLSX')
    # parser.add_argument('json_file', help='JSON file to convert')
    # parser.add_argument('excel_file', help='Excel file to create')
    # args = parser.parse_args()

    # json_to_excel = JsonToExcel(args.json_file, args.excel_file)
    json_to_excel = JsonToExcel('json/kampusInformatikaSNMPTN2021.json', 'excel/kampusInformatikaSNMPTN2021.xlsx')
    json_to_excel.convert()
    json_to_excel.close()
    print('Done')
    # thank you co-pilot
    # https://stackoverflow.com/questions/1208118/using-nested-dictionaries-in-a-json-file
