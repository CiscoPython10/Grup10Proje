import cv2

# İnsan vücudunu ve arabayı algılayan Sınıflandırıcıları ayrı ayrı değişkenlere tanımlıyorum
insan_algilama = cv2.CascadeClassifier('haarcascade_fullbody.xml')
arac_algilama = cv2.CascadeClassifier('haarcascade_car.xml')

# Resmi yükleyip resim değişkenine tanımlıyorum
resim = cv2.imread('goruntu.jpg')
# resmi grileştiriyorum gri_resim değişkenine tanımlıyorum
gri_resim = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)

# detectMultiScale insan vücudunu algılamaya yarar.
# aldığı parametrelerden gri_resim yüklenen gri formattaki resimfir.
# scaleFactor, resmi yeniden ölçeklendirir. 1.1 değeri resmi 1/10 oranında küçültür.
# minNeighbors, dikdörtgen içerisinde alınacak resim için kaç tane komşu sayısı gerektiğini ifade eder
# Ben burada komşu sayısını 3 seçtim.
insan = insan_algilama.detectMultiScale(gri_resim, scaleFactor=1.1, minNeighbors=3)

# Algılanan resmin kutu şeklinde çerveye alınmasını sağlar.
# (0,255,0) değeri çerçevenin rengini yeşil yapar.
for (x,y,w,h) in insan:
    resim = cv2.rectangle(resim, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Çerçeve içerisine alınan resmi etiketlendirir. Burada kutunun yanında "insan" yazacaktır.
# (0,255,0) değeri çerçevenin etiket rengini yeşil yapar.
cv2.putText(resim, 'insan', (x, y - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

# detectMultiScale insan vücudunu algılamaya yarar.
# aldığı parametrelerden gri_resim yüklenen gri formattaki resimfir.
# scaleFactor, resmi yeniden ölçeklendirir. 1.1 değeri resmi 1/10 oranında küçültür.
# minNeighbors, dikdörtgen içerisinde alınacak resim için kaç tane komşu sayısı gerektiğini ifade eder
# Ben burada komşu sayısını 1 seçtim.
araba = arac_algilama.detectMultiScale(gri_resim, scaleFactor=1.1, minNeighbors=1)

# Algılanan resmin kutu şkelinde çerveye alınmasını sağlar.
# (255,0,0) değeri çerçevenin rengini mavi yapar.
for (x,y,w,h) in araba:
    resim = cv2.rectangle(resim, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Çerçeve içerisine alınan resmi etiketlendirir. Burada kutunun yanında "arac" yazacaktır.
# (255,0,0) değeri çerçevenin etiket rengini mavi yapar.
cv2.putText(resim, 'arac', (x, y + h + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)

# nesneleri tespit edilip kutu içerisine alınmış resmi gösterir.
cv2.imshow('Algilanan Nesneler', resim)

# Herhangi bir tuşa basılıncaya kadar program sonlanmaz ve
# görüntülenen resim ekranda görünmeye devam eder.
cv2.waitKey(0)

# Uygulamaya ait peneceyi kapatır.
cv2.destroyAllWindows()