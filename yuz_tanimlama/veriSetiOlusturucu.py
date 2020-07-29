import cv2
import os,json

def kameragirisi():
    cam = cv2.VideoCapture(0)
    detector=cv2.CascadeClassifier('yuz_tanimlama/face.xml')
    i=0

    kisi_id=input('ID numarası giriniz')
    kisi_ad=input('Kişi Ad Soyad Giriniz:')
    while True:
        _, img =cam.read()
        gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
        for(x,y,w,h) in faces:
            i=i+1
            cv2.imwrite("yuz_tanimlama/yuzverileri/face-" + kisi_id + '.' + str(i) + ".jpg", gray[y:y + h , x :x + w])
            cv2.rectangle(img, (x , y), (x + w, y + h), (225, 0, 0), 2)
            cv2.imshow('resim', img[y :y + h, x :x + w])
            cv2.waitKey(100)
        if i>40:
            cam.release()
            cv2.destroyAllWindows()
            break
    kisiler={}
    try:
        dosya = open("etiketler.json","r")
        kisiler = json.load(dosya)
        dosya.close()
    except:
        pass
    
    kisiler[kisi_id]=kisi_ad    
    dosya = open("etiketler.json","w")
    a = json.dump(kisiler,dosya)
    dosya.close()
        


    


