#include <SPI.h>
#include <MFRC522.h>
#include <EEPROM.h>

#define RST_PIN 9
#define SS_PIN 10
#define ledPin 7

MFRC522 mfrc522(SS_PIN, RST_PIN);

String lastRfid = "";
String kart1 = "";
String kart2 = "";

MFRC522::MIFARE_Key key;

void setup()
{
  //rfc522 ayarları
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  pinMode(ledPin, OUTPUT);
 
  //EEPROM'dan kart bilgisini oku

}

void loop()
{
  //yeni kart okununmadıkça devam etme
  if ( ! mfrc522.PICC_IsNewCardPresent())
  {
    return;
  }
  if ( ! mfrc522.PICC_ReadCardSerial())
  {
    return;
  }
  //kartın UID'sini oku, rfid isimli string'e kaydet
  String rfid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++)
  {
    rfid += mfrc522.uid.uidByte[i] < 0x10 ? "0" : "";
    rfid += String(mfrc522.uid.uidByte[i], HEX);
  }
  //string'in boyutunu ayarla ve tamamını büyük harfe çevir
  rfid.trim();
  rfid.toUpperCase();
   Serial.flush();
 //while(1)
 {
  Serial.println("*"+rfid+"*");
  //delay(20);
 }
  delay(10000);

}
