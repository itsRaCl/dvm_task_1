from books import Book
from populate import populate


class Shelf:
    def __init__(self, genre):
        self.genre = genre
        self.books = populate(genre, "lms_books.xlsx")

    def populate_books(self):
        path = input("Enter the path of excel file: ")

    def show_calalog(self):
        pass
