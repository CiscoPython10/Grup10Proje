import sqlite3 # Sqlite'yı dahil ediyoruz

con = sqlite3.connect("yuztanimlama.db") # Tabloya bağlanıyoruz.

cursor = con.cursor() # cursor isimli değişken veritabanı üzerinde işlem yapmak için kullanacağımız imleç olacak.

def verileri_al3(numara):
    cursor.execute("Select * From yuz where numara = ?",(numara,)) # Girilen idler göre işlem yapıyoruz
    data = cursor.fetchall()
    return data
def veri_tabanikapat():
    con.close()
               