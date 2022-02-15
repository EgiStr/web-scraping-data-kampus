# create a new XLSX workbook using aspose-cells
# and convert a JSON file to an XLSX file

import argparse
import json
import os
import jpype
import asposecells
jpype.startJVM()
from asposecells.api import Workbook, FileFormatType, PdfSaveOptions


class JsonToExcel:
    def __init__(self, json_file, excel_file):
        self.json_file = json_file
        self.excel_file = excel_file
        self.workbook = None
        self.worksheet = None
        self.row = 0

    def convert(self):
        if not os.path.exists(self.json_file):
            raise Exception('JSON file does not exist: {}'.format(self.json_file))

        with open(self.json_file, 'r') as f:
            data = json.load(f)

        self.workbook = self.create_workbook()
        self.worksheet = self.create_worksheet()

        self.write_header()
        self.write_data(data)

        self.workbook.save(self.excel_file)

    def create_workbook(self):
        from com.aspose.cells import Workbook
        return Workbook()

    def create_worksheet(self):
        from com.aspose.cells import Worksheet
        return self.workbook.getWorksheets().get(0)

    def write_header(self):
        from com.aspose.cells import Cell

        header_row = self.worksheet.getCells().getRow(self.row)
        header_row.setHeight(20)

        for i, header in enumerate(['Universitas', 'Prodi', 'Jenjang', 'Peminat 2021', 'Daya Tampung 2022', 'Keketatan']):
            cell = header_row.getCell(i)
            cell.setValue(header)

        self.row += 1

    def write_data(self, data):
        from com.aspose.cells import Cell
        from com.aspose.cells import Style

        style = Style()
        style.setFontBold(True)

        for row in data:
            row_data = [row.
                        get('universitas', ''),
                        row.get('prodi', ''),
                        row.get('jenjang', ''),
                        row.get('peminat_2021', ''),
                        row.get('daya_tampung_2022', ''),
                        row.get('keketatan', '')]

            row_cells = self.worksheet.getCells().createRow(self.row)
            row_cells.setHeight(20)

            for i, cell_value in enumerate(row_data):
                cell = row_cells.getCell(i)
                cell.setValue(cell_value)
                cell.setStyle(style)

            self.row += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert JSON to XLSX')
    parser.add_argument('json_file', help='JSON file to convert')
    parser.add_argument('excel_file', help='Excel file to create')
    args = parser.parse_args()

    json_to_excel = JsonToExcel(args.json_file, args.excel_file)
    json_to_excel.convert()
    print('JSON file converted to XLSX file: {}'.format(args.excel_file))

    # python jsontoexcel.py data.json data.xlsx
    # python jsontoexcel.py data.json data.xlsx

