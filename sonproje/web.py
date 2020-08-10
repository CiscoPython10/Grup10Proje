from flask import Flask,flash,render_template,Response,request,redirect,url_for,session,logging
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from flask_sqlalchemy import SQLAlchemy
from camera import VideoCamera
from veriSetiOlusturucu import kameragirisi
import Egitme
import cv2
from passlib.hash import sha256_crypt
from functools import wraps




app=Flask(__name__)

#Veri Tabanı İş ve İşlemleri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/MKAVAKLI/Desktop/sonproje/yuztanimlama.db'
db = SQLAlchemy(app)

#Tablo sınıflarının oluşturulması
class Yuz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_soyad = db.Column(db.String(80))
    numara=db.Column(db.Integer)
    kartno=db.Column(db.String(80))
    
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

# Kullanıcı Giriş Decorator'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın.","danger")
            return redirect(url_for("login"))
    return decorated_function
 
#Anasayfa Sayfa
@app.route("/")
def index():
    return render_template("index.html")

#Hakkımızda Sayfası

@app.route("/about")
def about():
    return render_template("about.html")

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

#Login olduktan sonra gidilecek kontrol panel sayfası
@app.route("/kontrol")
@login_required
def kontrol():
    
    return render_template("kontrol.html")

#Kullanıcıları listeleme iş ve işlemleri (Admin)

@app.route("/duzenle")
@login_required
def duzenle():
    todos = Kullanici.query.all()
    return render_template("kontrol1.html",todos=todos)

#Kullanıcı Silme İş ve İşlemleri
@app.route("/delete1/<string:id>")
def deletekullanici(id):
    #Gönderilen id göre tablodaki kayıtı SQLAlchemy sorgusu ile alma
    kullanici = Kullanici.query.filter_by(id = id).first()
    db.session.delete(kullanici)
    db.session.commit()
    return redirect(url_for("duzenle"))

#Web Cam İşlemleri sayfası
@app.route("/cam")
@login_required
def cam():
    return render_template('cam.html')
#Web cam sayfasında bulunan butonların işlev görevmesi için gerekli sayfaların oluşturulması
@app.route("/cam1/<string:id>")
@login_required
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
        return render_template('cam1.html',id=id)
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
@app.route('/video_feedYT')
def video_feedYT():
    
    return Response(gen(VideoCameraYT()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6               

class VideoCameraYT(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        recognizer=cv2.face.LBPHFaceRecognizer_create()
        #ds_factor=0.6
        recognizer.read('training/trainer.yml')
        cascadePath = "face.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)
        path = 'yuzverileri'
        success, image = self.video.read()
        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        face_rects=face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in face_rects:
            tahminEdilenKisi, conf = recognizer.predict(gray[y:y + h, x:x + w])
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            fontFace = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            fontColor = (255, 255, 255)
            cv2.putText(image, str(tahminEdilenKisi), (x, y + h), fontFace, fontScale, fontColor)
            todo = Yuz.query.filter_by(numara = tahminEdilenKisi).first()

            if todo:
                #yoklamaya kayıt edilmiş mi kontrol edilecek
                todo1 = Yoklama.query.filter_by(numara = todo.numara).first()
                if  not todo1:                 
                    ad_soyad=todo.ad_soyad
                    numara=todo.numara
                    yeniKayit=Yoklama(ad_soayd=ad_soyad,numara=numara,complete=True)
                    db.session.add(yeniKayit)
                    db.session.commit()
                           

            break
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
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


#Yoklama Sayfası
@app.route("/yoklama")
@login_required
def yoklama():
    yoklama = Yoklama.query.all()#Yoklamam tablosundaki tüm kayıtları al
    return render_template("yoklama.html",yoklama=yoklama)

#Yoklama sayfasında öğrenci silme 

@app.route("/delete/<string:id>")
@login_required
def deleteogrenci(id):
    #Gönderilen id göre tablodaki kayıtı SQLAlchemy sorgusu ile alma
    ogrenci = Yoklama.query.filter_by(id = id).first()
    db.session.delete(ogrenci)
    db.session.commit()
    return redirect(url_for("yoklama"))


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
    