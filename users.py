import mysql.connector as sql
from getpass import getpass
from shelf import Shelf
from books import Book
from openpyxl import load_workbook
import sys

user_dat = {
    "User_1": ["084101115116105110103064049050051", "USR"],
    "Librarian": ["076105098114097114105097110064049050051", "LIB"],
}
# This dictionary can be stored in an sql database too


class User:
    def __init__(self, priv):

        self.uname = input("\nUsername: ")
        if self.uname in user_dat:
            if priv != user_dat[self.uname][1]:
                print("\n\nYou don't have permission to log into this section\n\n")
            else:
                self.passwd = pass_hash(getpass("\nPassword: "))
                if self.passwd == user_dat[self.uname][0]:
                    print("Logged In!\n\n")
                    del self.passwd
                else:
                    print("Wrong password\n\nProgram Terminated\n")
                    exit()
        else:
            print("User does not exist contact adimistrators for help")
            exit()


class Basic_User(User):
    def __init__(self):
        self.priv = "USR"
        super().__init__(self.priv)

    def book_actions(self, book_obj):
        book_obj.get_status()
        if book_obj.status != "Available":
            print(
                f"Sorry the book is already {book_obj.status}, Try again after the book is available\n\n"
            )
        else:
            choice = int(
                input("What do you want to do:\n1.Issue Book\n2.Reserve Book\n>>")
            )
            if choice in [1, 2]:
                if choice == 1:
                    book_obj.issue_book(self)
                if choice == 2:
                    book_obj.reserve_book(self)
            else:
                print("Enter a valid choice")
                self.book_actions(self, book_obj)

    def options(self):
        while True:
            choice = int(
                input(
                    "1.Search Genre\n2.Search Book via Book Title\n3.Search Book Via ISBN\n4.Search Book Via Author Name\n5.Return Book\n0.Logout\n>>"
                )
            )
            if choice in range(0, 6):
                wb = load_workbook(filename="lms_books.xlsx")
                wb_sheet = wb.active
                if choice == 1:
                    genre_shelf = Shelf(input("\n\nEnter the Genre: "))
                    Shelf.show_catalog(genre_shelf.genre, genre_shelf.books)
                    # TODO Complete this
                elif choice == 2:
                    query = input("\nEnter the Book Title: ")
                    for i in range(2, wb_sheet.max_row + 1):
                        cell = wb_sheet.cell(row=i, column=1)
                        if str(cell.value).lower() == query.lower():
                            result_book = create_book(wb_sheet, i)
                            print(result_book)
                            break
                        else:
                            print("The Book is not in the library database")
                    self.book_actions(result_book)
                elif choice == 3:
                    query = int(input("\nEnter the Book ISBN Number: "))
                    for i in range(2, wb_sheet.max_row + 1):
                        cell = wb_sheet.cell(row=i, column=2)
                        if cell.value == query:
                            result_book = create_book(wb_sheet, i)
                            print(result_book)
                            break
                        else:
                            print("The Book is not in the library database")
                    self.book_actions(result_book)
                elif choice == 4:
                    query = input("\nEnter the Author's Name: ")
                    books = []
                    for i in range(2, wb_sheet.max_row + 1):
                        cell = wb_sheet.cell(row=i, column=3)
                        if str(cell.value).lower().strip() == query.lower().strip():
                            result_book = create_book(wb_sheet, i)
                            books.append(result_book)
                    if len(books) == 0:
                        print("The Author is not in the database")
                    else:
                        for i in range(len(books)):
                            print(f"\n\n=====Book No.{i+1}=====")
                            print(str(books[i]) + "\n\n")
                        n = int(input("Which book do you want to select:"))
                        self.book_actions(books[n - 1])
                elif choice == 5:
                    isbn = int(
                        input("Enter the ISBN number of the book you want to return: ")
                    )
                    for i in range(2, wb_sheet.max_row + 1):
                        cell = wb_sheet.cell(row=i, column=2)
                        if cell.value == isbn:
                            result_book = create_book(wb_sheet, i)
                            reserved_by = wb_sheet.cell(row=i, column=8).value
                            break
                        else:
                            print("The Book is not in the library database")
                    result_book.get_status()
                    if result_book.status != "Issued":
                        print("\n\nThe book is not issued no need to return")
                    elif result_book.status == "Issued" and self.uname == reserved_by:
                        result_book.return_book()
                    else:
                        print("\n\nBook has not been issued to you\n\n")
                elif choice == 0:
                    wb.close()
                    break


class Librarian(User):
    def __init__(self):
        self.priv = "LIB"
        super().__init__(self.priv)

    def options(self):
        while True:
            choice = int(
                input("Options:\n1.See Issued Books\n2.Manage Books by genre\n0.Logout")
            )
            if choice in [0, 1, 2]:
                if choice == 2:
                    genre = input("Enter the Genre you want to manage: ")
                    genre_shelf = Shelf(genre)
                    choice = int(input("1.Add Book\n2.Remove Book\n0.Logout\n>>"))
                elif choice == 1:
                    self.get_issued_books()

    def get_issued_books():
        books = []
        wb = load_workbook(filename="lms_books.xlsx")
        wb_sheet = wb.active
        for i in range(2, wb._sheet.max_row + 1):
            if wb_sheet.cell(row=i, column=4).value == "Issued":
                books.append(create_book(wb_sheet, i))
        return books


def pass_hash(
    passwd,
):  # Very basic hashing algorithm just to not store passwords in plain text
    passwd_hash = [str(ord(x)) for x in passwd]
    for i in range(len(passwd_hash)):
        if len(passwd_hash[i]) != 3:
            passwd_hash[i] = "0" * (3 - len(passwd_hash[i])) + passwd_hash[i]
    return "".join(passwd_hash)


def create_book(wb_sheet, i):
    return Book(
        wb_sheet.cell(row=i, column=1).value,
        wb_sheet.cell(row=i, column=2).value,
        wb_sheet.cell(row=i, column=3).value,
        wb_sheet.cell(row=i, column=4).value,
    )
