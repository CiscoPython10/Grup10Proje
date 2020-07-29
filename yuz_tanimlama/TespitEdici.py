import cv2
import os,json

def tespitetme():
    recognizer=cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('yuz_tanimlama/training/trainer.yml')
    cascadePath = "yuz_tanimlama/face.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    path = 'yuz_tanimlama/yuzverileri'
    cam = cv2.VideoCapture(0)
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
        
        for(x,y,w,h) in faces:
            tahminEdilenKisi, conf = recognizer.predict(gray[y:y + h, x:x + w])

            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            # if(tahminEdilenKisi==2):
            #     tahminEdilenKisi= 'Kişi 2'
            # elif (tahminEdilenKisi == 1):
            #     tahminEdilenKisi = 'Kişi 1'
            # else:
            #     tahminEdilenKisi= "Bilinmeyen kişi"

            kisiler={} 
            try:   
                dosya = open("etiketler.json","r")
                kisiler = json.load(dosya)
                dosya.close()
                tahminEdilenKisiAd=kisiler[str(tahminEdilenKisi)]
            except:        
                tahminEdilenKisi="Bilinmeyen Kisi"

            fontFace = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            fontColor = (255, 255, 255)
            cv2.putText(im, str(tahminEdilenKisiAd), (x, y + h), fontFace, fontScale, fontColor)
            cv2.imshow('im',im)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cam.release() 
                cv2.destroyAllWindows()
        









