import RPi.GPIO as GPIO
import time
#from adafruit_servokit import ServoKit
import speech_recognition as sr
from gtts import gTTS
import os
from openai import OpenAI
#import busio

#kit=ServoKit(channels=16)
#servo=3

#Declare Servos
#servoR = kit.servo[5] #Reference at 0
#servoL = kit.servo[11] #Reference at 180

#motor start
in1 = 24
in2 = 23
en = 25


in22 = 27
in21 = 22
en2 = 17


GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

GPIO.setup(in21,GPIO.OUT)
GPIO.setup(in22,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in21,GPIO.LOW)
GPIO.output(in22,GPIO.LOW)



q=GPIO.PWM(en2,500)
p=GPIO.PWM(en,500)


p.start(10)
q.start(20)

#motor end






client = OpenAI(api_key="**********************************",)

def motor_forward():
    GPIO.output([IN1, IN2, IN3, IN4], [GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW])
    time.sleep(2)
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

def recognize_speech(timeout=None):
    recognizer = sr.Recognizer()
    #recognizer.energy_threshold = 72.28488019259504
    

    with sr.Microphone(device_index = 1) as source:
        print("Listening for commands...")

        try:
            audio = recognizer.listen(source,timeout=timeout)  
            recognizer.adjust_for_ambient_noise(source)
            recognizer.pause_threshold = 1
            recognizer.dynamic_energy_threshold = 3000
                      
             
            command = recognizer.recognize_google(audio).lower()
            return command

        except (sr.UnknownValueError, sr.WaitTimeoutError) as e:
            print(f"Error: {e}")
            return None
        except sr.RequestError as e:
            print(f"Error during speech recognition: {e}")
            return None

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    tts.save("response.mp3")
    os.system("mpg321 response.mp3 && rm response.mp3")

#def both_up():
    #servoR.angle = 90
    #servoL.angle = 90

# def original_pos():
    #servoR.angle = 0
    #servoL.angle = 180

#def right_up() :
    #servoR.angle = 90

#def left_up() :
    #servoL.angle = 90
#def right_down() :
    #servoR.angle = 0
#def left_down() :
    #servoL.angle = 180
def respond(query):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "Your name is Marvin. You are an AI assistant robot.You were created by Omar Faruk. You have vast knowledge about various topics. You respond to the question asked to you with very precise, accurate and very short answer. If you are asked something that you do not have knowledge about, you simple say that you don't know. Do not ever start any sentense by saying 'As an AI model'. You are an AI assistant robot. You have a great sense of humour. You provide your answers in an eye catching manner. Your way of talking is very stylish and professional.",
        },
        {"role": "user", "content": f"{format(query)}"}
        ])
    return response.choices[0].message.content

if __name__ == "__main__":
    try:
        while True:
            command = recognize_speech(timeout=1)  # Initial timeout of 5 seconds

            if command == "marvin":
                print("Keyword 'marvin' detected. Now listening continuously...")
                text_to_speech("Hello there! how can I assist you ?")

                while True:
                    command = recognize_speech(timeout=None)  # No timeout for continuous listening

                    if command == "bye":
                        print("Exiting continuous listening...")
                        break
                    elif command == "raise hands":
                        both_up()
                    elif command == "lower hands" :
                        original_pos()
                    elif command == "right hand up":
                        right_up()
                    elif command == "right hand down":
                        right_down()
                    elif command == "left hand up":
                        left_up()
                    elif command == "left hand down":
                        left_down()
                    elif command:
                        print(f"You said: {command}")
                        answer = respond(command)
                        print(answer)
                        text_to_speech(answer)
                        
            elif command == "raise hands":
                both_up()
            elif command == "lower hands" :
                original_pos()
            elif command == "right hand up":
                right_up()
            elif command == "right hand down":
                right_down()
            elif command == "left hand up":
                left_up()
            elif command == "left hand down":
                left_down()
            elif command == "forward":
                text_to_speech("going forward")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in21,GPIO.LOW)
                GPIO.output(in22,GPIO.HIGH)
                time.sleep(1)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in21,GPIO.LOW)
                GPIO.output(in22,GPIO.LOW)
            elif command == "backward":
                text_to_speech("going backward")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in21,GPIO.HIGH)
                GPIO.output(in22,GPIO.LOW)
                time.sleep(1)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in21,GPIO.LOW)
                GPIO.output(in22,GPIO.LOW)
            elif command == "left":
                text_to_speech("turning left")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in21,GPIO.HIGH)
                GPIO.output(in22,GPIO.LOW)
                time.sleep(1)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in21,GPIO.LOW)
                GPIO.output(in22,GPIO.LOW)
            elif command == "right":
                text_to_speech("turning right")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in21,GPIO.LOW)
                GPIO.output(in22,GPIO.HIGH)
                time.sleep(1)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in21,GPIO.LOW)
                GPIO.output(in22,GPIO.LOW)
            elif command == "exit":
                print("Exiting program...")
                break

    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        GPIO.cleanup()
