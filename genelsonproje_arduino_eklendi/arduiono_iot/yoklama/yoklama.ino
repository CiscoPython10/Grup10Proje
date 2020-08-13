
#include <MFRC522.h>
#include <MFRC522Extended.h>
#include <SPI.h>
#include <SoftwareSerial.h>


#define RST_PIN 9
#define SS_PIN 10
#define ledPin 7
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

 
SoftwareSerial esp8266(2,3); // make RX Arduino line is pin 2, make TX Arduino line is pin 3.
                             // This means that you need to connect the TX line from the esp to the Arduino's pin 2
                             // and the RX line from the esp to the Arduino's pin 3


String IP="192.168.0.32";
String data="";
String rfid="";
void setup()
{
   Serial.begin(115200);
 
  esp8266.begin(115200); // your esp's baud rate might be different
 
  connectWifi();
  //rfc522 ayarları
 // Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  pinMode(ledPin, OUTPUT);
  Serial.println("RFID KART OKUMA UYGULAMASI");
  Serial.println("--------------------------");
  Serial.println();
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
    //Kart versinin okunması
    //Verinin ağ dan gönderilmesi
    //esp8266.println("192.168.0.13/index2.php2=22");
    
  
    //Verinin ağ dan gönderilmesi
    data=rfid;
     httppost();
 // delay(2000);
}
 
/*
* Name: sendData
* Description: Function used to send data to ESP8266.
* Params: command - the data/command to send; timeout - the time to wait for a response; debug - print to Serial window?(true = yes, false = no)
* Returns: The response from the esp8266 (if there is a reponse)
*/



  


void connectWifi()
{
  Serial.println("islem basladi");
    String ag="etenketen";
    String sifre="ss9932550811";
          
     esp8266.println("AT\r\n");
     delay(2000);
    if(esp8266.find("OK") ) Serial.println("Hazir");
   
    
    esp8266.println("AT+CWMODE=1\r\n");

   //String cmd = "AT+CWJAP=\"" +ag+"\",\"" + sifre + "\"\r\n";  
     esp8266.println("AT+CWJAP=\"etenketen\",\"ss9932550811\"\r\n");
    //esp8266.print(cmd);
    
       delay(10000);
      
    esp8266.println("AT+CWDHCP=\"1\",\"en\"");
    if(esp8266.find("OK")) 
    {
    
      Serial.println("Connected!");
       
    
    }
    
    else 
    {  
   
    
    Serial.println("Cannot connect to wifi"); 
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

    String sendCmd = "AT+CIPSEND=";//determine the number of caracters to be sent.

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

            // close the connection

            esp8266.println("AT+CIPCLOSE");

        }

    }
}
