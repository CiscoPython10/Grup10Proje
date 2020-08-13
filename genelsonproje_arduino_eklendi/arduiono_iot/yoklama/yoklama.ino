
#include <MFRC522.h>
#include <MFRC522Extended.h>
#include <SPI.h>
#include <SoftwareSerial.h>


#define RST_PIN 9
#define SS_PIN 10
#define ledPin 7
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

 
SoftwareSerial esp8266(2,3); // arduino 2 nolu pin esp TX ine, 3 nolu pin esp RX ine


String IP="192.168.0.32";// sunucu adresi
String data="";
String rfid="";
void setup()
{
   Serial.begin(115200);
 
  esp8266.begin(115200); // kullanılan esp modülüne göre değişiklik gösterebilir
 
  connectWifi();
  //rfc522 ayarları
 // Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  pinMode(ledPin, OUTPUT);

}
 
void loop()
{
   if ( ! mfrc522.PICC_IsNewCardPresent())
      {
        return;
      }
      if ( ! mfrc522.PICC_ReadCardSerial())
      {
        return;
      }
      //kartın UID'sini oku, rfid isimli string'e kaydet
      rfid = "";
      for (byte i = 0; i < mfrc522.uid.size; i++)
      {
        rfid += mfrc522.uid.uidByte[i] < 0x10 ? "0" : "";
        rfid += String(mfrc522.uid.uidByte[i], HEX);
      }
      //string'in boyutunu ayarla ve tamamını büyük harfe çevir
      rfid.trim();
      rfid.toUpperCase();
   
    
  
    //Verinin ağ dan gönderilmesi
    data=rfid;
     httppost();
  delay(20);
}
 



  


void connectWifi()
{
  Serial.println("islem basladi");
    String ag="ssid ";
    String sifre="şifre";
          
     esp8266.println("AT\r\n");
     delay(2000);
    if(esp8266.find("OK") ) Serial.println("Hazir");
   
    
    esp8266.println("AT+CWMODE=1\r\n");

   String cmd = "AT+CWJAP=\"" +ag+"\",\"" + sifre + "\"\r\n";  
     
    //esp8266.print(cmd);
    
       delay(10000);
      
    esp8266.println("AT+CWDHCP=\"1\",\"en\"");
    if(esp8266.find("OK")) 
    {
    
      Serial.println("Bağlantı tamam!");
       
    
    }
    
    else 
    {  
   
    
    Serial.println("Bağlanmada sorun var."); 
   // connectWifi();
    }

}
void httppost () 
{

    esp8266.println("AT+CIPSTART=\"TCP\",\"" + IP + "\",5000");//start a TCP connection.

    if( esp8266.find("OK")) 
    {

        Serial.println("TCP connection ready");

    } delay(1000);

    String postRequest =    (String("")+"POST " + "/" +"kartnumarasi/"+data+ " HTTP/1.0\r\n" + "Host: " + IP + "\r\n" +

    "Accept: *" + "/" + "*\r\n" +

    "Content-Length: " + data.length() + "\r\n" +

    "Content-Type: application/x-www-form-urlencoded\r\n" +

    "\r\n" + data);

    String sendCmd = "AT+CIPSEND=";

    esp8266.print(sendCmd);

    esp8266.println(postRequest.length() );

    delay(500);

    if(esp8266.find(">")) 
    { Serial.println("Sending.."); esp8266.print(postRequest);

        if( esp8266.find("SEND OK")) 
        { Serial.println("Packet sent");

            while (esp8266.available()) {

            String tmpResp = esp8266.readString();

            Serial.println(tmpResp);

            }

            // bağlantıyı kapat
            esp8266.println("AT+CIPCLOSE");

        }

    }
}
