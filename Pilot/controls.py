#!/usr/bin/python

from Pilot import PiMotor
import time
import RPi.GPIO as GPIO

m1 = PiMotor.Motor("MOTOR1", 1)
m2 = PiMotor.Motor("MOTOR2", 1)
m3 = PiMotor.Motor("MOTOR3", 1)
m4 = PiMotor.Motor("MOTOR4", 1)

motorAll = PiMotor.LinkedMotors(m1, m2, m3, m4)

def execute_action(action):
    match action:
        case "front":
            front()
        case "right":
            right()
        case "far_right":
            far_right()
        case "left":
            left()
        case "far_left":
            far_left()
        case "back":
            back()
        case _:
            print("Nieznana komenda:", action)

def front():
    try:
        print("Robot Moving Forward")
        motorAll.forward(50)
        time.sleep(0.5)
        motorAll.stop()
    except KeyboardInterrupt:
        GPIO.cleanup()

def back():
    try:
        print("Robot Moving Backward")
        motorAll.reverse(50)
        time.sleep(0.5)
        motorAll.stop()
    except KeyboardInterrupt:
        GPIO.cleanup()

def left():
    try:
        print("Robot Turning Left")
        m2.forward(50)
        m4.forward(50)
        m3.reverse(20)
        m1.reverse(20)
        time.sleep(0.75)
        motorAll.stop()
    except KeyboardInterrupt:
        GPIO.cleanup()

def far_left():
    try:
        print("Robot Turning Left")
        m2.forward(50)
        m4.forward(50)
        m3.reverse(20)
        m1.reverse(20)
        time.sleep(1.5)
        motorAll.stop()
    except KeyboardInterrupt:
        GPIO.cleanup()

def right():
    try:
        print("Robot Turning Right")
        m1.forward(50)
        m3.forward(50)
        m4.reverse(20)
        m2.reverse(20)
        time.sleep(0.75)
        motorAll.stop()
    except KeyboardInterrupt:
        GPIO.cleanup()

def far_right():
    try:
        print("Robot Turning Right")
        m1.forward(50)
        m3.forward(50)
        m4.reverse(20)
        m2.reverse(20)
        time.sleep(1.5)
        motorAll.stop()
    except KeyboardInterrupt:
        GPIO.cleanup()
