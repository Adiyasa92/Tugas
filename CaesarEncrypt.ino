/*
 * Project    = Interface Enkripsi Caesar Pada Arduino Nano Menggunakan Python3 dan Qt5
 * Author     = I Wayan Adiyasa
 * NIM        = 16/404567/PTK/10984
 * Dosen      = Agus Bejo
 * Deskripsi  = Program firmware ini diperuntukan pengunci dengan menggunakan sandi Caesar
 *              dengan menggeser data string yang diterima. Data yang diterima dari 
 *              interface Python dan PyQt akan dienkripsi sesuai dengan jumlah data yang
 *              akan digeser. Hasil enkripsi akan diolah untuk disimpan ke dalam EEPROM 
 *              atau digunakan untuk membuka kunci / password. Data yang disimpan dalam 
 *              EEPROM adala hasil enkripsi, sehingga orang lain tidak mampu mengetahui
 *              password yang tersimpan dalam mikrokontroler. 
 */

#include <EEPROM.h>
#include "String.h"

int DataEEPROM[50];			        // Jumlah karakter pada EEPROM
int EncripVal;                  // Nilai pergeseran data saat di encript
int count;                      // Variable untuk fungsi for

String datain;					        // Data Masuk dari USART
String data1;					          // Akses baca atau tulis
int data2;					            // Data encript dan decript
String data3;					          // Data password
bool stsPassword;

void setup() {
  Serial.begin(115200);			    // Inisialisasi memulai komunikasi
  pinMode(13, OUTPUT);			    // Indikator LED
  BacaEEPROM();                 // Baca semua isi EEPROM
  stsPassword = false;          // Status ini, password tertutup
}

void loop() {
  ReadUART();
}

// Proses membaca UART
void ReadUART(){
  if(Serial.available()>0){
    datain = Serial.readStringUntil('\n');
    data1 = datain.substring(0,7);  			    // Status Opening atau Writing
    data2 = datain.substring(7,8).toInt(); 	  // Konversi data string ke integer dari 0 sampai 9
    data3 = datain.substring(8,33);  			    // Jumlah password 25

    delay(50);
    Serial.println("Data diterima : ");
    Serial.print("     Status   : ");
    Serial.println(data1);
    Serial.print("     Enkripsi : ");
    Serial.println(data2);
    Serial.print("     Password : ");
    Serial.println(data3);
    
    Serial.print("     Result   : ");
    if(data1 == "Opening"){Opening();}
    else if(data1 == "Writing"){Writing();}
    else {Closing();}
    
    Serial.print("     Proses   : ");
    for(count=0;count<7;count++){Serial.print(data3[count]+data2);}
    Serial.println();
    BacaEEPROM();
    Serial.print("     Memori   : ");
    for(count=0;count<7;count++){Serial.print(DataEEPROM[count]);}
    Serial.println();
  }
}

// Proses membuka kunci 
void Opening(){
  for(count=0;count<7;count++){
    if(data3[count]+data2 == DataEEPROM[count]){
      digitalWrite(13,HIGH);
      stsPassword = true;
    }
    else {
      count=7;
      digitalWrite(13,LOW);
      stsPassword = false;
    }
  }
  if(stsPassword == true){Serial.println("Password terbuka");}
  else{Serial.println("Password tertutup");}
}

// Proses penulisan data ke memori EEPROM
void Writing(){
  EEPROM.write(0,data2);
  for(count=1;count<8;count++){
    EEPROM.write(count, data3[count-1]+data2);
    delay(50);
  }
  Serial.println("Password sudah ditulis ke memori");
}

// Ketika data yang diterima tidak sesuai dengan protokol 
void Closing(){
  digitalWrite(13, LOW);
  Serial.println("Protokol SALAH!!!");
}

// Proses pembacaan pada EEPROM
void BacaEEPROM(){
  EncripVal = EEPROM.read(0);                 //Baca EEPROM alamat 0 untuk geser encript
  for(count=1;count<51;count++){				      // Mengcounter data EEPROM 100x
    DataEEPROM[count-1] = EEPROM.read(count);}	// Membaca data pada EEPROM
}

