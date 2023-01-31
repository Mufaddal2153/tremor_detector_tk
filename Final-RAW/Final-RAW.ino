// Code revision: 19th Jan, 2022
// Tremor 
#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 accelgyro;

int16_t ax, ay, az;
int16_t gx, gy, gz;
float accelNorm = 0;
float gyroNorm = 0;

const int numReadings = 10;
float readings[numReadings];      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
float total = 0;                  // the running total
float average = 0;                // the average

//IRModule
int IRSensor = 4; // connect ir sensor to arduino pin 7


void setup() 
{
  Wire.begin();
  Serial.println("Initializing I2C devices...");
  accelgyro.initialize();
  Serial.println("Testing device connections...");
  Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
  pinMode (IRSensor, INPUT); // sensor pin INPUT
  pinMode (4, INPUT);
  Serial.begin(38400); // open the serial port at 9600 bps:
}

void loop()
{
  int IRSwitch = digitalRead(12);
  int MyoSwitch = digitalRead(11);
  int TremorSwitch = digitalRead(13);  
  if(IRSwitch == LOW){
    
  int statusSensor = digitalRead (IRSensor);
  
  if (statusSensor == 0){
    Serial.print("1\n"); 
  }
  else{
    Serial.print("0\n");
  }
  delay(100);
  }
  else if(MyoSwitch == LOW){
    Serial.println(analogRead(A0));
    delay(100);
    }
  else if(TremorSwitch == LOW){
    // read raw accel/gyro measurements from device
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    // these methods (and a few others) are also available
    //accelgyro.getAcceleration(&ax, &ay, &az);
    //accelgyro.getRotation(&gx, &gy, &gz);

    accelNorm = mySmoothing(sqrt(pow(ax, 2) + pow(ay, 2) + pow(az, 2)));
    gyroNorm =  mySmoothing(sqrt(pow(gx, 2) + pow(gy, 2) + pow(gz, 2)));
//     display tab-separated accel/gyro x/y/z values
      //Serial.println(accelNorm);
//      Serial.println(gyroNorm);
      //Serial.print("a/g:\t");
      //Serial.println(ax); 
      //Serial.print(ay); Serial.print("\t");
      //Serial.print(az); Serial.print("\t");
      //Serial.println(gx); //Serial.print("\t");
      //Serial.print(gy); Serial.print("\t");
      //Serial.println(gz);
      Serial.print(ax); Serial.print(", ");
      Serial.print(ay); Serial.print(", ");
      Serial.print(az); Serial.print(", ");
      Serial.print(gx); Serial.print(", ");
      Serial.print(gy); Serial.print(", ");
      Serial.print(gz); Serial.print("\n");
      delay(500);
    }
    else{
      loop();
      }
    
}

int mySmoothing(int fsensorValue){
  
  // subtract the last reading:
  total = total - readings[readIndex];
  // read from the sensor:
  // readings[readIndex] = analogRead(inputPin);
  readings[readIndex] = fsensorValue;
  // add the reading to the total:
  total = total + readings[readIndex];
  // advance to the next position in the array:
  readIndex = readIndex + 1;

  // if we're at the end of the array...
  if (readIndex >= numReadings) {
    // ...wrap around to the beginning:
    readIndex = 0;
  }

  // calculate the average:
  average = total / numReadings;
  // send it to the computer as ASCII digits
  //  Serial.println(average);
  delay(1);        // delay in between reads for stability
  return average;
}
