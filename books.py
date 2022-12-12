from colorama import Fore
from openpyxl import load_workbook
from datetime import date


class Book:
    def __init__(self, name, isbn, author, genre):
        self.name = name
        self.author = author
        self.isbn = isbn
        self.genre = genre

    def __str__(self):

        return f"\n\nName: {self.name}\nAuthor: {self.author}\nGenre: {self.genre}\nISBN: {self.isbn}\n"

    def get_status(self):
        wb = load_workbook(filename="lms_books.xlsx")
        wb_sheet = wb.active
        for i in range(2, wb_sheet.max_row + 1):
            if wb_sheet.cell(row=i, column=2).value == self.isbn:
                self.status = wb_sheet.cell(row=i, column=5).value
                date_start = wb_sheet.cell(row=i, column=6).value
                date_end = wb_sheet.cell(row=i, column=7).value
                break
        # This assumes that if a book is issued it cannot be reserved before it is returned
        if self.status == "Issued":
            self.issued_date = date_start
            self.return_date = date_end
            print(Fore.RED + f"Status: Issued {self.return_end}" + Fore.WHITE)

        elif self.status == "Reserved":
            self.reserve_start = date_start
            self.reserve_start = date_end
            print(
                Fore.YELLOW
                + f"Status: Reserved from {self.reserve_start} upto {self.reserve_end}"
                + Fore.WHITE
            )
        elif self.status == "Available":
            print(Fore.GREEN + "Status: Available" + Fore.WHITE)
        wb.close()

    def return_book(self):
        wb = load_workbook(filename="lms_books.xlsx")
        wb_sheet = wb.active
        for i in range(2, wb_sheet.max_row + 1):
            if wb_sheet.cell(row=i, column=2).value == self.isbn:
                wb_sheet.cell(row=i, column=5).value = "Available"
                wb_sheet.cell(row=i, column=6).value = 0
                wb_sheet.cell(row=i, column=7).value = 0
                break
        wb.save("lms_books.xlsx")

    def issue_book(self, user):
        wb = load_workbook(filename="lms_books.xlsx")
        wb_sheet = wb.active
        for i in range(2, wb_sheet.max_row + 1):
            if wb_sheet.cell(row=i, column=2).value == self.isbn:
                wb_sheet.cell(row=i, column=5).value = "Issued"
                wb_sheet.cell(row=i, column=6).value = date.today()
                ret_date = [
                    int(x)
                    for x in input("Enter end date in format (yyyy-mm-dd): ").split("-")
                ]
                if ret_date[0] >= date.today().year:
                    if ret_date[1] >= date.today().month:
                        if ret_date[2] > date.today().day:
                            wb_sheet.cell(row=i, column=7).value = date(
                                ret_date[0], ret_date[1], ret_date[2]
                            )
                            wb_sheet.cell(row=1, column=8).value = user.uname
                            wb.save("lms_books.xlsx")
                        else:
                            print("\nEnter a valid date")
                    else:
                        print("\nEnter a valid date")
                else:
                    print("\nEnter a valid date")

                break

    def reserve_book(self, user):
        wb = load_workbook(filename="lms_books.xlsx")
        wb_sheet = wb.active
        for i in range(2, wb_sheet.max_row + 1):
            if wb_sheet.cell(row=i, column=2).value == self.isbn:
                wb_sheet.cell(row=i, column=5).value = "Reserved"
                res_start_date = [
                    int(x)
                    for x in input("Enter start date in format (yyyy-mm-dd)").split("-")
                ]
                if res_start_date[0] >= date.today().year:
                    if res_start_date[1] >= date.today().month:
                        if res_start_date[2] > date.today().day:
                            wb_sheet.cell(row=i, column=6).value = date(
                                res_start_date[0], res_start_date[1], res_start_date[2]
                            )
                        else:
                            print("\nEnter a valid date")
                    else:
                        print("\nEnter a valid date")
                else:
                    print("\nEnter a valid date")

                res_end_date = [
                    int(x)
                    for x in input("Enter end date in format (yyyy-mm-dd)").split("-")
                ]
                if res_end_date[0] >= res_start_date[0]:
                    if res_end_date[1] >= res_start_date[1]:
                        if res_end_date[2] > res_start_date[2]:
                            wb_sheet.cell(row=i, column=7).value = date(
                                res_end_date[0], res_end_date[1], res_end_date[2]
                            )
                            wb_sheet.cell(row=1, column=8).value = user.uname
                            wb.save("lms_books.xlsx")
                        else:
                            print("\nEnter a valid date")
                    else:
                        print("\nEnter a valid date")
                else:
                    print("\nEnter a valid date")

                break
