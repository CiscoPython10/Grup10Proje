import Egitme
import TespitEdici
import veriSetiOlusturucu


while True:
    print("""
    -------------------------------------
    ************Yüz Tanımlama***********
    1-Veri Seti Oluşturma
    2-Eğitme
    3-Tespit   Edici
    Çıkmak içim q ' basınız
    """)
    islem=input("Yapacağınız işlemi seciniz(1-3)")
    if islem=="1":
        veriSetiOlusturucu.kameragirisi()
    elif islem=="2":
        Egitme.egitme_basla()
    elif islem=="3":
        TespitEdici.tespitetme()
    elif  islem=="q":
        print("İslem Sonlandırıldı")
        break
    else:
        print("Hatalı Giriş")