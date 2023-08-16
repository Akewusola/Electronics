// define sound speed in cm per microseconds
#define SOUND_SPEED 0.034
// define the speed limit in km per hour
#define SPEED_LIMIT 60

long duration;
float distanceCm;
float first;
float second;
float totalDistanceCm;
float speedCmperMilli;
float speedMetrePerSec;
float speedKmPerHr;

const int trigPin = 12;
const int echoPin = 13;

void setup() {
  Serial.begin(115200);
  // setting the orientation of the trigger pin and receiver pin of the ultrasonic sensor
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
 
  }

void loop() {
  // clear the everytime trigPin upon returning
  digitalWrite(trigPin, LOW);
  // Get the first distance to the object
  first = ultrasonicRead();
  if (first > 0) {
    // Now, delay the sensor by 90 millisecond before sending another wave
    delay(1000);
    // Get the second distance
    second = ultrasonicRead();
    // find the absolute value of the difference between the two numbers
    totalDistanceCm = abs(first - second);
    // Get the speed in Cm per millisecond
    speedCmperMilli = totalDistanceCm / (1000);
    // Get the speed in metre per second
    speedMetrePerSec = speedCmperMilli * 10;
    Serial.print("Speed is :");
    Serial.println(speedMetrePerSec);
    // Get the speed in km per hour
    speedKmPerHr = speedMetrePerSec * 3.6;
    if (speedKmPerHr > SPEED_LIMIT) {
      // proccess the image
    }
  } 
  // Begin loop after a second
  delay(100); 
}

float ultrasonicRead() {
    // Sent out ultrasonic wave for 10 microseconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin,LOW);

    //Reads the receiver Pin, return the sound wave travel time un microseconds
    duration = pulseIn(echoPin, HIGH);
    // Calculate the distance to the object
    distanceCm = duration * SOUND_SPEED/2;
    return distanceCm;
  }



