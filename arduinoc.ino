// Define pin numbers
const int trigPin = 7;  // Pin connected to the trigger signal of the ultrasonic sensor
const int echoPin = 6;  // Pin connected to the echo signal of the ultrasonic sensor

// Declare variables
long duration;  // Time it takes for the ultrasonic pulse to travel to the object and back
int distance;   // Calculated distance based on the measured duration

void setup() {
  pinMode(trigPin, OUTPUT);  // Set the trigPin as an output
  pinMode(echoPin, INPUT);   // Set the echoPin as an input
  Serial.begin(9600);        // Start the serial communication at a baud rate of 9600
}

void loop() {
  // Clear the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Set the trigPin to HIGH state for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echoPin and measure the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculate the distance based on the measured duration
  distance = duration * 0.034 / 2;

  // Print the distance to the Serial Monitor
  Serial.println(distance);
}
