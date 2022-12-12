import mysql.connector as sql

class User:
    def __init__(self, uname, passwd):
        self.uname = uname
        self.passwd = passwd
    
    
class Basic(User):
    def login():
        self.priviledge = "basic"
        self. uname = input("Enter your username: ")
        __db = sql.connect(host="localhost", user="racl", passwd="", database="library_login")
        __cur = __db.cursor()


