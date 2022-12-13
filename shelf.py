from books import Book
from populate import populate
from openpyxl import load_workbook


class Shelf:
    def __init__(self, genre):
        self.genre = genre
        self.books = self.populate_books("lms_books.xlsx")
        self.book_count = self.get_book_count()

    def get_book_count(self):
        return len(self.books)

    def populate_books(self, file):
        return populate(self.genre, file)

    @staticmethod
    def show_catalog(title, books):

        print("\n\n\n" + "=" * 85)
        print("|{:^83}|".format(title))
        print("=" * 85)
        # Making a table of books, column headers Name ISBN Author Genre
        print(
            "|{:^20}|{:^20}|{:^20}|{:^20}|".format(
                "Name", "ISBN No.", "Author", "Genre"
            )
        )
        print("=" * 85)
        for i in books:

            print(
                "|{:^20}|{:^20}|{:^20}|{:^20}|".format(
                    i.name, i.isbn, i.author, i.genre
                )
            )
            print("-" * 85 + "\n\n")
