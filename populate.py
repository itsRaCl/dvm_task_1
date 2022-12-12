from openpyxl import load_workbook


def populate(genre, file):
    wb = load_workbook(filename=file)
    wb_sheet = wb.active
