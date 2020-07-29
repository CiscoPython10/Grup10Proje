import sys,os
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5 import uic
from PyQt5 import QtWidgets,QtGui
import cv2
from PyQt5.QtCore import QTimer
import numpy as np
from PIL import Image
import sqlite3
import veritabani
from PyQt5.QtGui import QImage,QPixmap

class Pencere(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.devam=False
        self.init_ui()# tüm işlemlerin yapılacağı kısım

    def init_ui(self):
       
        self.win = uic.loadUi("yuz_tan_sqlite3_pq5_vlk/form.ui")
        self.say=0      
        
        self.win.buton.clicked.connect(self.click)
        self.win.buton1.clicked.connect(self.kapat)
        self.win.buton2.clicked.connect(self.veriseti)
        self.win.buton3.clicked.connect(self.egitme)
        self.win.buton4.clicked.connect(self.tanima)
        
        self.win.kamera_label.setPixmap(QPixmap("yuz_tan_sqlite3_pq5_vlk/webcam.jpg"))
        self.win.show()


    def tanima(self):

        recognizer=cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('yuz_tan_sqlite3_pq5_vlk/training/trainer.yml')
        cascadePath = "yuz_tan_sqlite3_pq5_vlk/face.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)
        path = 'yuz_tan_sqlite3_pq5_vlk/yuzverileri'
        self.cam = cv2.VideoCapture(0)
        self.timer.start(3)

        if self.devam==True:
            self.win.yazi_alani.setText("Tanımlama İşlemi Yapılıyor")
        else:
            self.win.yazi_alani.setText("Önce Kamerayı Açın")

        while self.devam==True:
            ret, im =self.cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
            #aces=face_cascade.detectMultiScale(gray,1.3,5)
            for(x,y,w,h) in faces:
                tahminEdilenKisi, conf = recognizer.predict(gray[y:y + h, x:x + w])
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                tahminEdilenKisi=veritabani.verileri_al3(tahminEdilenKisi)
                if(tahminEdilenKisi):
                    tahminEdilenKisi= tahminEdilenKisi[0][0]
            
                else:
                    tahminEdilenKisi= "Bilinmeyen kişi"
                fontFace = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                fontColor = (255, 255, 255)
                cv2.putText(im, str(tahminEdilenKisi), (x, y + h), fontFace, fontScale, fontColor)
                
                #cv2.imshow('im',im)

            im = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
            height,width,channel = im.shape
            step = channel*width
            qImg = QImage(im.data,width,height,step,QImage.Format_RGB888)
            self.win.kamera_label.setPixmap(QPixmap.fromImage(qImg))

            if (cv2.waitKey(1) & 0xFF == ord("q")):
                break
            
        self.cam.release() 
        self.timer.stop()             

    def kapat(self):
        self.win.yazi_alani.setText("Kamera Kapatıldı")
        self.win.kamera_label.setPixmap(QPixmap("yuz_tan_sqlite3_pq5_vlk/webcam.jpg"))
        self.devam=False

    def click(self):
        self.devam=True
        if not self.timer.isActive():
            self.kamera=cv2.VideoCapture(0)
            self.timer.start(3)
            self.win.yazi_alani.setText("Kamera Aktif")
            ret,im=self.kamera.read()
            #cv2.imshow("Görüntü",goruntu)
            # im = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
            # height,width,channel = im.shape
            # step = channel*width
            # qImg = QImage(im.data,width,height,step,QImage.Format_RGB888)
            # self.win.kamera_label.setPixmap(QPixmap.fromImage(qImg))
            while self.devam==True:
                ret,im=self.kamera.read()
                #cv2.imshow("Görüntü",goruntu)
                im = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
                height,width,channel = im.shape
                step = channel*width
                qImg = QImage(im.data,width,height,step,QImage.Format_RGB888)
                self.win.kamera_label.setPixmap(QPixmap.fromImage(qImg))

                if cv2.waitKey(25)& 0xFF==ord('q'):
                    break
            self.kamera.release()
            self.timer.stop()
            #cv2.destroyAllWindows()
        


    def egitme(self):
        
        if self.timer.isActive():
            self.win.yazi_alani.setText("Eğitime İşlemleri Yapılıyor")
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            cascadePath = "yuz_tan_sqlite3_pq5_vlk/face.xml"
            faceCascade = cv2.CascadeClassifier(cascadePath)
            path = 'yuz_tan_sqlite3_pq5_vlk/yuzverileri'
            def get_images_and_labels(path):
                image_paths = [os.path.join(path, f) for f in os.listdir(path)]
                images = []
                labels = []
                for image_path in image_paths:
                    image_pil = Image.open(image_path).convert('L')
                    image = np.array(image_pil, 'uint8')
                    nbr = int(os.path.split(image_path)[1].split(".")[0].replace("face-", ""))
                    #self.win.egit_bilgi.setVisible(True)
                    self.win.yazi_alani.setText(str(nbr))
                    #☺print(nbr)
                    faces = faceCascade.detectMultiScale(image)
                    for (x, y, w, h) in faces:
                        images.append(image[y: y + h, x: x + w])
                        labels.append(nbr)
                        cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])

                        #self.win.kamera_label.setPixmap(QPixmap.fromImage(images[y: y + h, x: x + w]))
                        cv2.waitKey(10)
                return images, labels
            images, labels = get_images_and_labels(path)
            cv2.imshow('test',images[0])
            # im = cv2.cvtColor(images[0],cv2.COLOR_BGR2RGB)
            # height,width,channel = im.shape
            # step = channel*width
            # qImg = QImage(im.data,width,height,step,QImage.Format_RGB888)
            # self.win.kamera_label.setPixmap(QPixmap.fromImage(qImg))
            cv2.waitKey(1)

            recognizer.train(images, np.array(labels))
            recognizer.write('yuz_tan_sqlite3_pq5_vlk/training/trainer.yml')
            #cv2.destroyAllWindows()
        else:
            self.win.yazi_alani.setText("Önce Kamerayı Açın")


    def veriseti(self):
        
        if self.timer.isActive():
            
            self.kamera=cv2.VideoCapture(0)
            self.detector=cv2.CascadeClassifier('yuz_tan_sqlite3_pq5_vlk/face.xml')
            self.kisi_id=self.win.kisi_id.text()
            self.kisi_adi=self.win.kisi_adi.text()
            self.kisi_adi=self.kisi_adi.upper()
            veritabani.deger_ekle(self.kisi_adi,self.kisi_id)
            #self.timer.start(3)
            i=0
            self.win.yazi_alani.setText("Veri Seti İşlemleri")
            
            
            while self.devam==True:
                _, img =self.kamera.read()
                gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces=self.detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
                for(x,y,w,h) in faces:
                    i=i+1
                    cv2.imwrite("yuz_tan_sqlite3_pq5_vlk/yuzverileri/face-" + self.kisi_id + '.' + str(i) + ".jpg", gray[y:y + h , x :x + w])
                    cv2.rectangle(img, (x , y), (x + w, y + h), (225, 0, 0), 2)
                    #cv2.imshow('resim', img[y :y + h, x :x + w])

                    im = cv2.cvtColor(img[y :y + h, x :x + w],cv2.COLOR_BGR2RGB)
                    height,width,channel = im.shape
                    step = channel*width
                    qImg = QImage(im.data,width,height,step,QImage.Format_RGB888)
                    self.win.kamera_label.setPixmap(QPixmap.fromImage(qImg))


                    cv2.waitKey(100)
                    if i>40:
                        # self.kamera.release()
                        # self.timer.stop()
                        self.kapat()
                        self.devam=False
                        #cv2.destroyAllWindows()
        else:
            self.win.yazi_alani.setText("Önce Kamera Açın")
            
        
        

app=QtWidgets.QApplication(sys.argv)
pencere=Pencere()
sys.exit(app.exec_())