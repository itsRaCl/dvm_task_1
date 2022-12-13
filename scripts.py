from books import Book


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
