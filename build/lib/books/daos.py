
import pymysql

class BooksDao():

        
    def findAll(self):
        db = pymysql.connect(host="192.168.1.200",port=3306,user="root",passwd="root123456",db="video")
        cursor = db.cursor()
        cursor.execute("SELECT ssku,stbjsdvdurl FROM t_amusement WHERE stbjsdvdurl != '' AND stbjsdvdurl LIKE '%books.com.tw%'")
        re =  cursor.fetchall()
        cursor.close()
        db.close()
        return re
