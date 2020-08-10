from flask import Flask,flash,render_template,Response,request,redirect,url_for,session,logging
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from flask_sqlalchemy import SQLAlchemy
from camera import VideoCamera
from veriSetiOlusturucu import kameragirisi
import Egitme
from TespitEdici import tespitetme
import cv2
from passlib.hash import sha256_crypt




app=Flask(__name__)

#Veri Tabanı İş ve İşlemleri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/MKAVAKLI/Desktop/sonproje/yuztanimlama.db'
db = SQLAlchemy(app)

class Yuz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_soyad = db.Column(db.String(80))
    numara=db.Column(db.Integer)
    

class Kullanici(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kullanici_adi = db.Column(db.String(35) )
    kullanici_sifre = db.Column(db.String(20))
    isim=db.Column(db.String(35))
    mail=db.Column(db.String(65))

    def __init__(self, kullanici_adi, kullanici_sifre,isim,mail):
        self.kullanici_adi = kullanici_adi
        self.kullanici_sifre = kullanici_sifre
        self.isim=isim
        self.mail=mail

class Yoklama(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_soayd = db.Column(db.String(80))
    numara=db.Column(db.Integer)
    complete=db.Column(db.Boolean)

 
#Anasayfa
@app.route("/")
def index():
    return render_template("index.html")

#Hakkımızda

@app.route("/about")
def about():
    return render_template("about.html")

#Yoklama Sayfası
@app.route("/yoklama")
def yoklama():
    yoklama = Yoklama.query.all()#Yoklamam tablosundaki tüm kayıtları al
    return render_template("yoklama.html",yoklama=yoklama)
#Yoklama sayfasında öğrenci silme 
@app.route("/delete/<string:id>")
def deleteogrenci(id):
    #Gönderilen id göre tablodaki kayıtı SQLAlchemy sorgusu ile alma
    ogrenci = Yoklama.query.filter_by(id = id).first()
    db.session.delete(ogrenci)
    db.session.commit()
    return redirect(url_for("yoklama"))
#Web Cam İşlemleri sayfası
@app.route("/cam")
def cam():
    return render_template('cam.html')
#Web cam sayfasında bulunan butonların işlev görevmesi için gerekli sayfaların oluşturulması
@app.route("/cam1/<string:id>")
def cam1(id):
    if id=="1":
        return render_template('cam1.html',id=id)
    elif id=="2":
        return render_template('cam1.html',id=id)
    elif id=="3":
         return render_template('cam1.html',id=id)
    elif id=="4":
        Egitme.egitme_basla()
        return render_template('cam1.html',id=id)
    elif id=="5":
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
                                           
                   
                    else:
                        tahminEdilenKisi= "Bilinmeyen kişi"
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    fontColor = (255, 255, 255)
                    cv2.putText(im, str(tahminEdilenKisi), (x, y + h), fontFace, fontScale, fontColor)
                    cv2.imshow('Yuz Tanimlama',im)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        addYoklama()
                        cam.release() 
                        cv2.destroyAllWindows()
                        break
                        
                        

                        
        tespitetme()
        return render_template('cam.html')
    else:
        return render_template('cam.html')
#Web sayfasında web camden görüntü gösterme
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\(n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#Web arayüzünde yüz tanımlama sırasında Yuz tablosuna veri ekleme işlemi ve yuz resimleri çekme

@app.route("/add",methods=["POST"])
def addYuz():
    ad_soyad=request.form.get("adsoyad")
    numara=request.form.get("numara")
    if ad_soyad=="" or numara=="":
        flash("Kayıt yapmak için lütfen bilgileri giriniz...","danger")
        return redirect(url_for("cam1",id="3"))
    else:

        yeniKayit=Yuz(ad_soyad=ad_soyad,numara=numara)
        db.session.add(yeniKayit)
        db.session.commit()
        kameragirisi(numara)
        return redirect(url_for("cam1",id="3"))
#İçerik sayfaları
@app.route("/icerik1")
def icerik1():
    return render_template("icerik1.html")

@app.route("/icerik2")
def icerik2():
    return render_template("icerik2.html")

@app.route("/icerik3")
def icerik3():
    return render_template("icerik3.html")
@app.route("/kontrol")
def kontrol():
    
    return render_template("kontrol.html")
@app.route("/duzenle")
def duzenle():
    todos = Kullanici.query.all()
    return render_template("kontrol1.html",todos=todos)

# Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim Soyisim",validators=[validators.Length(min = 4,max = 25)])
    username = StringField("Kullanıcı Adı",validators=[validators.Length(min = 5,max = 35)])
    email = StringField("Email Adresi",validators=[validators.Email(message = "Lütfen Geçerli Bir Email Adresi Girin...")])
    password = PasswordField("Parola:",validators=[
        validators.DataRequired(message = "Lütfen bir parola belirleyin"),
        validators.EqualTo(fieldname = "confirm",message="Parolanız Uyuşmuyor...")
    ])
    confirm = PasswordField("Parola Doğrula")
#Kayıt Olma
@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        kullanici_adi=request.form.get("username")
        kullanici_sifre=sha256_crypt.encrypt(request.form.get("password"))
        name = form.name.data
        email = form.email.data
        yeniKayit=Kullanici(kullanici_adi=kullanici_adi,kullanici_sifre=kullanici_sifre,isim=name,mail=email)
        db.session.add(yeniKayit)
        db.session.commit()
        flash("Başarıyla Kayıt Oldunuz...","success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form = form)
#Login İşlemleri
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")
@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method=="POST":

        
        name = request.form['username']
        passw = request.form['password']
        
        bilgi=Kullanici.query.filter_by(kullanici_adi=name).first()
       
        if bilgi is not None:
            g_passw=bilgi.kullanici_sifre
            if sha256_crypt.verify(passw,g_passw):
                session['logged_in'] = True
                session['username']=name
                flash("Başarıyla Giriş Yaptınız...","success")
                return redirect(url_for("index"))
            else:
                flash("Parolanızı Yanlış Girdiniz...","danger")
                return redirect(url_for("login")) 

                 
        
        else:
            
            

            flash("Böyle bir kullanıcı bulunmuyor...","danger")
            
            return redirect(url_for("login"))
     
   
    return render_template("login.html",form = form)
#Kullanıcı silme 
@app.route("/delete1/<string:id>")
def deletekullanici(id):
    #Gönderilen id göre tablodaki kayıtı SQLAlchemy sorgusu ile alma
    kullanici = Kullanici.query.filter_by(id = id).first()
    db.session.delete(kullanici)
    db.session.commit()
    return redirect(url_for("duzenle"))
# Logout İşlemi
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
    