
import pymysql
import xlrd

class BooksDao():

        
    def findAll(self):
        db = pymysql.connect(host="192.168.1.200",port=3306,user="root",passwd="root123456",db="video")
        cursor = db.cursor()
        cursor.execute("SELECT ssku,stbjsdvdurl FROM t_amusement WHERE stbjsdvdurl != '' AND stbjsdvdurl LIKE '%books.com.tw%'")
        re =  cursor.fetchall()
        cursor.close()
        db.close()
        return re
    
    def findAllFromExcel(self,path):
        data = xlrd.open_workbook(path)
        table = data.sheet_by_index(0)
        nrows = table.nrows
        ncolumns = table.ncols
        
        
