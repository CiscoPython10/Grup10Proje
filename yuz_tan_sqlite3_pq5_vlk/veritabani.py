import sqlite3 # Sqlite'yı dahil ediyoruz

con = sqlite3.connect("yuz_tan_sqlite3_pq5_vlk/yuz.db") # Tabloya bağlanıyoruz.

cursor = con.cursor() # cursor isimli değişken veritabanı üzerinde işlem yapmak için kullanacağımız imleç olacak.

def tablo_oluştur():
    cursor.execute("CREATE TABLE IF NOT EXISTS yuz (İsim TEXT,  ID INT)") # Sorguyu çalıştırıyoruz.
    con.commit() # Sorgunun veritabanı üzerinde geçerli olması için commit işlemi gerekli.
def deger_ekle(isim,id):
    cursor.execute("INSERT INTO yuz VALUES(?,?)",(isim,id))
    con.commit()
def verileri_al3(id):
    cursor.execute("Select * From yuz where id = ?",(id,)) # Girilen idler göre işlem yapıyoruz
    data = cursor.fetchall()
    return data
def veri_tabanikapat():
    con.close()
               