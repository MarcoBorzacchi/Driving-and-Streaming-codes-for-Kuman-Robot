import socket
import sys
import time
import keyboard

TCP_IP = '192.168.3.1'
TCP_PORT = 2001

IN_ANGLE 	= str(30)
STOP 		= "\xFF\x00\x00\x00\xFF"
BACKWARD 	= "\xFF\x00\x01\x00\xFF"
FORWARD 	= "\xFF\x00\x02\x00\xFF"
TURN_LEFT 	= "\xFF\x00\x03\x00\xFF"
TURN_RIGHT 	= "\xFF\x00\x04\x00\xFF"
ANGLE_H 	= "\xFF\x01\x07%s\xFF" 
ANGLE_V 	= "\xFF\x01\x08%s\xFF"

angle_v = 30
angle_h = 90

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class robot:
    def fwdbut(self):
        s.send(FORWARD)
    
    def bwdbut(self):
        s.send(BACKWARD)
        
    def leftbut(self):
        s.send(TURN_LEFT)
    
    def rightbut(self):
        s.send(TURN_RIGHT)
        
    def stopper(self):
        s.send(STOP)

    def __init__(self):
        self.forw = 0
        self.backw = 0
        self.dx = 0
        self.sx = 0
        self.set_speed = 1
        self.VELOCITY_R = "\xFF\x02\x01\x20\xFF"
        self.VELOCITY_L = "\xFF\x02\x02\x20\xFF"
        self.max_angle = 140
        self.forward = 'w'
        self.backward = 's'
        self.right = 'd'
        self.left = 'a'
        self.cam_r = 'l'
        self.cam_l = 'j'
        self.cam_up = 'i'
        self.cam_down = 'k'
        self.reset_cam = 'p'
        self.angle_delta = 10            
        self.in_angle_v = angle_v
        self.in_angle_h	= angle_h
        self.ANGLE_H = ANGLE_H % chr(self.in_angle_h)
        self.ANGLE_V = ANGLE_V % chr(self.in_angle_v)
        s.connect((TCP_IP, TCP_PORT))
        s.send(STOP)
        s.send(self.ANGLE_V)		
        s.send(self.ANGLE_H)
        s.send(self.VELOCITY_R)
        s.send(self.VELOCITY_L)
    
    def	camera_goup(self):
        if self.in_angle_v < self.max_angle - 50 :
            self.in_angle_v = self.in_angle_v + self.angle_delta
            self.ANGLE_V = ANGLE_V % chr(self.in_angle_v)
            s.send(self.ANGLE_V)			
            #time.sleep(0.02)	

    def	camera_godown(self):
        if self.in_angle_v > 10 :
            self.in_angle_v = self.in_angle_v - self.angle_delta
            self.ANGLE_V = ANGLE_V % chr(self.in_angle_v)
            s.send(self.ANGLE_V)			
            time.sleep(0.02)

    def camera_goright(self) :
        if self.in_angle_h > 20 :
            self.in_angle_h = self.in_angle_h - self.angle_delta
            self.ANGLE_H = ANGLE_H % chr(self.in_angle_h)
            s.send(self.ANGLE_H)
            time.sleep(0.02)

    def camera_goleft(self) :
        if self.in_angle_h < self.max_angle :
            self.in_angle_h = self.in_angle_h + self.angle_delta
            self.ANGLE_H = ANGLE_H % chr(self.in_angle_h)
            s.send(self.ANGLE_H)
            time.sleep(0.02)

    def camera_reset(self) :
	    self.in_angle_h = angle_h
	    self.in_angle_v = angle_v
	    self.ANGLE_H = ANGLE_H % chr(self.in_angle_h)
	    self.ANGLE_V = ANGLE_V % chr(self.in_angle_v)
	    s.send(self.ANGLE_H)
	    time.sleep(0.01)
	    s.send(self.ANGLE_V)
	    time.sleep(0.01)
    
    def gear_change(self) :
        s.send(self.VELOCITY_R)
        s.send(self.VELOCITY_L)

			
    def close_conn(self):
        s.close()
        exit()
		





