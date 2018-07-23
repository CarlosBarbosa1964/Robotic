#include <Wire.h>
#include <Servo.h>

#define SLAVE_ADDRESS 0x20

int number = 0;
int servo = 9;
int cont = 0;
int iCont = 0;
int j=0;
String result;
double _ang = 0;
float angulo = 0;
Servo aJuntas[6]; // create servo object to control a servo
float aAng_Origem[6];
float aAng_Destino[6];
float aAng_Atual[6];



// Configurações iniciais
void setup() {
  aJuntas[0].attach(2);// liga o servo no pino 2 ao objeto servo
  aJuntas[1].attach(3);// liga o servo no pino 2 ao objeto servo
  aJuntas[2].attach(4);// liga o servo no pino 2 ao objeto servo
  aJuntas[3].attach(5);// liga o servo no pino 2 ao objeto servo
  aJuntas[4].attach(6);// liga o servo no pino 2 ao objeto servo
  aJuntas[5].attach(7);// liga o servo no pino 2 ao objeto servo
  
  // Atribui angulo para a matriz de origem
  aAng_Origem[0] = float(20.0); 
  aAng_Origem[1] = float(105.0);
  aAng_Origem[2] = float(130.0);
  aAng_Origem[3] = float(180.0);
  aAng_Origem[4] = float(90.0);
  aAng_Origem[5] = float(85.0);

  // Atribui o ang de Origem para Atual
  aAng_Atual[0] = aAng_Origem[0];
  aAng_Atual[1] = aAng_Origem[1];
  aAng_Atual[2] = aAng_Origem[2];
  aAng_Atual[3] = aAng_Origem[3];
  aAng_Atual[4] = aAng_Origem[4];
  aAng_Atual[5] = aAng_Origem[5];

  // Atribui o ang de Origem para Destino
  aAng_Destino[0] = aAng_Origem[0];
  aAng_Destino[1] = aAng_Origem[1];
  aAng_Destino[2] = aAng_Origem[2];
  aAng_Destino[3] = aAng_Origem[3];
  aAng_Destino[4] = aAng_Origem[4];
  aAng_Destino[5] = aAng_Origem[5];  
  
  aJuntas[0].write(aAng_Atual[0]);
  aJuntas[1].write(aAng_Atual[1]);
  aJuntas[2].write(aAng_Atual[2]);
  aJuntas[3].write(aAng_Atual[3]);
  aJuntas[4].write(aAng_Atual[4]);
  aJuntas[5].write(aAng_Atual[5]);
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.println("Ready!");
}

void loop() {
   delay(5);
   int i;
   iCont =0;
   for (i=0; i<=5; i+=1){
       
       if (aAng_Destino[i]<aAng_Origem[i]){
          j=-1;
          aAng_Atual[i]=(aAng_Atual[i] + j);
          aAng_Origem[i]=aAng_Atual[i];
          aJuntas[i].write(aAng_Atual[i]);
          delay(15);
          //Serial.println("Subtrai");          
       } else if(aAng_Destino[i]>aAng_Origem[i]){
          j=1;
          aAng_Atual[i]=(aAng_Atual[i] + j);
          aAng_Origem[i]=aAng_Atual[i];
          aJuntas[i].write(aAng_Atual[i]);
          delay(15);
          //Serial.println("Soma");          
       }      
       if (abs(aAng_Origem[i]-aAng_Destino[i]) <= 1 && (aAng_Origem[i] != aAng_Destino[i])){          
          aAng_Origem[i]=aAng_Destino[i];
          aAng_Atual[i]=aAng_Destino[i];
          aJuntas[i].write(aAng_Origem[i]);
          delay(15);
          iCont+=1;
          Serial.println(iCont);
          if (iCont==5){
            Serial.println("Igual ***********************");
            sendData();
          }
       }   
   }
}

// callback for received data
void receiveData(int byteCount){    
       while(Wire.available()) {
       result = String(Wire.read());
       //Serial.println(result);         // print the character   
       number = result.toInt();
       if (servo == 9){        
         switch (number) {
            case 0:   // Junta 0
              // statements
              servo = number;
              Serial.println(servo);
              break;
            case 1:   // Junta 01
              // statements
              servo = number;
              break;
            case 2: // Junta 02
              // statements
              servo = number;
              break;
            case 3:   // Junta 03
              // statements
              servo = number;
              break;
            case 4:  // Junta 04 - Pulso
              // statements
              servo = number;
              break;
            case 5:   // Junta 05 - Garra
              // statements
              servo = number;
              break;
            case 8:   // Junta 05 - Garra
              // statements              
              servo = 9;
              _ang = 0;
              cont=0;              
              Serial.println("Inicado :");
              break;
            default:
              // statements
              break;
          }
       } else {
          
          if (cont == 0){ 
            _ang = number;
            //Serial.print("Servo: ");
            //Serial.print(servo);  
            //Serial.print(" Angulo ");
            //Serial.print(number);
            cont = cont + 1; 
         } else {
            angulo = (float)_ang + ((float)number/100.0);
            //angulo = 0.55;
            //Serial.print(" Decimal ");
            //Serial.print(number); 
            //Serial.print(" - ");
            //Serial.println(angulo); 
            aAng_Destino[servo] = angulo;
            servo = 9;
            _ang = 0;
            angulo = 0;
            cont=0;              
            Serial.println("Inicado :");                       
         }
       }
    }
}
void move_servo(){   
  
}
// callback for sending data
void sendData(){
    Wire.write("OK");
}
