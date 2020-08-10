import cv2


def tespitetme():
            recognizer=cv2.face.LBPHFaceRecognizer_create()
            #ds_factor=0.6
            recognizer.read('training/trainer.yml')
            cascadePath = "face.xml"
            faceCascade = cv2.CascadeClassifier(cascadePath)
            path = 'yuzverileri'
            cam = cv2.VideoCapture(0)
            while True:
                ret, im =cam.read()
                #im=cv2.resize(im,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
                gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
                for(x,y,w,h) in faces:
                    tahminEdilenKisi, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                    #Tespit edilen id/numara ile Yuz veritananında eşleşen kayıdı getirme
                    todo = Yuz.query.filter_by(numara = tahminEdilenKisi).first()
                    def addYoklama():
                            ad_soyad=todo.ad_soyad
                            numara=todo.numara
                            yeniKayit=Yoklama(ad_soayd=ad_soyad,numara=numara,complete=True)
                            db.session.add(yeniKayit)
                            db.session.commit()
                    if(todo):
                        tahminEdilenKisi= todo.ad_soyad
                        addYoklama()
                        #cam.release() 
                        fontFace = cv2.FONT_HERSHEY_SIMPLEX
                        fontScale = 1
                        fontColor = (255, 255, 255)
                        cv2.putText(im, str(tahminEdilenKisi), (x, y + h), fontFace, fontScale, fontColor)
                        cv2.imshow('Yuz Tanimlama',im)
                        cv2.destroyAllWindows()
                        return tahminEdilenKisi                                          
                   
                    else:
                        tahminEdilenKisi= "Tanimlanmadi"
                        fontFace = cv2.FONT_HERSHEY_SIMPLEX
                        fontScale = 1
                        fontColor = (255, 255, 255)
                        cv2.putText(im, str(tahminEdilenKisi), (x, y + h), fontFace, fontScale, fontColor)
                        cv2.imshow('Yuz Tanimlama',im)
                        #cam.release() 
                        cv2.destroyAllWindows()
                        return tahminEdilenKisi 


                   
                   
                    #     addYoklama()
                    #     cam.release() 
                    #     cv2.destroyAllWindows()
                    #     break






