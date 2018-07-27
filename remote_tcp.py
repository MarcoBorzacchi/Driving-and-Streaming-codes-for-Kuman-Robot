import socket
import sys
import time
import pygame
import keyboard


TCP_IP = '192.168.3.1'
TCP_PORT = 2001

IN_ANGLE 	= str(30)
STOP 	        = "\xFF\x00\x00\x00\xFF"
BACKWARD 	= "\xFF\x00\x01\x00\xFF"
FORWARD 	= "\xFF\x00\x02\x00\xFF"
TURN_LEFT 	= "\xFF\x00\x03\x00\xFF"
TURN_RIGHT 	= "\xFF\x00\x04\x00\xFF"
ANGLE_H 	= "\xFF\x01\x07%s\xFF" 
ANGLE_V 	= "\xFF\x01\x08%s\xFF"

angle_v = 30
angle_h = 90

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
max_angle = 140

flag_camup = 0
flag_camdown = 0
flag_camr = 0
flag_caml = 0

pygame.init()
screen = pygame.display.set_mode((400, 150))
font = pygame.font.SysFont("comicsansms", 35)
press = font.render("Write here to run (X to close)", True, (0, 0, 0))

screen.fill((255, 255, 255))
screen.blit(press,(200- press.get_width() // 2, 75 - press.get_height() // 2))
pygame.display.flip()

class robot:

    def __init__(self):
        self.forw = 0
        self.backw = 0
        self.dx = 0
        self.sx = 0
        
        self.set_speed = 0
        print("\n___________________________________________________________________")
        print("Command Settings")
        print("Motor: \n   w = forward \n   s = backward \n   a = turn left \n   d = turn right")
        print("\nCamera: \n   i = cam_up \n   k = cam down \n   l = cam right \n   j = cam left")
        print("\nPress p for resetting the camera position")
        print("\nPress o to change speed")
        print("___________________________________________________________________")
        print("Set Speed:")
        print("   v = gear 1st(high accuracy)")
        print("   b = gear 2nd")
        print("   n = gear 3rd")
        print("   m = gear 4th!(full power)\n")
        print("Press buttons in the pygame window")
        

	while not(self.set_speed): 
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
                            s.close()
			    sys.exit()
			    print("press ESC on the video to close it")
	
			if event.type == pygame.KEYDOWN:
			    if event.key == pygame.K_v:
	                        self.VELOCITY_R = "\xFF\x02\x01\x02\xFF"
	                        self.VELOCITY_L = "\xFF\x02\x02\x02\xFF"
	                        s.send(self.VELOCITY_R)
	                        s.send(self.VELOCITY_L)
	                        print("")
	                        print("speed set to slow")
	                        self.set_speed = 1
				break
	                    elif event.key == pygame.K_b:
	                        self.VELOCITY_R = "\xFF\x02\x01\x0A\xFF"
	                        self.VELOCITY_L = "\xFF\x02\x02\x0A\xFF"
	                        s.send(self.VELOCITY_R)
	                        s.send(self.VELOCITY_L)
	                        print("")
	                        print("speed set to medium")
	                        self.set_speed = 1  
				break     
	                    elif event.key == pygame.K_n:
	                        self.VELOCITY_R = "\xFF\x02\x01\x2F\xFF"
	                        self.VELOCITY_L = "\xFF\x02\x02\x2F\xFF"
	                        s.send(self.VELOCITY_R)
	                        s.send(self.VELOCITY_L)
	                        print("")
	                        print("speed set to fast")
	                        self.set_speed = 1
				break
	                    elif event.key == pygame.K_m:
	                        self.VELOCITY_R = "\xFF\x02\x01\x5A\xFF"
	                        self.VELOCITY_L = "\xFF\x02\x02\x5A\xFF"
	                        s.send(self.VELOCITY_R)
	                        s.send(self.VELOCITY_L)
	                        print("")
	                        print("speed set to insane, good luck!")
	                	self.set_speed = 1
				break
        print("___________________________________________________________________\n") 

        self.in_angle_v = angle_v
        self.in_angle_h	= angle_h
        self.ANGLE_H = ANGLE_H % chr(self.in_angle_h)
        self.ANGLE_V = ANGLE_V % chr(self.in_angle_v)
        s.send(STOP)
        s.send(self.ANGLE_V)		
        s.send(self.ANGLE_H)
        s.send(self.VELOCITY_R)
        s.send(self.VELOCITY_L)
    
    def forward(self):
        if not(self.forw): 
            s.send(FORWARD)	
            self.forw = 1	

    def backward(self):
        if not(self.backw):
            s.send(BACKWARD)
            self.backw = 1

    def right(self):
        if not(self.dx):
            s.send(TURN_RIGHT)
            self.dx = 1

    def left(self):
        if not(self.sx):
            s.send(TURN_LEFT)
            self.sx = 1

    def not_forward(self):
        if self.forw: 
            s.send(STOP)	
            self.forw = 0
            if self.backw :
                s.send(BACKWARD)
            if self.dx :
                s.send(TURN_RIGHT)
            if self.sx :
                s.send(TURN_LEFT)

    def not_backward(self):
        if self.backw:
            s.send(STOP)
            self.backw = 0
            if self.forw :
                s.send(FORWARD)
            if self.dx :
                s.send(TURN_RIGHT)
            if self.sx :
                s.send(TURN_LEFT)            

    def not_right(self):
        if self.dx:
            s.send(STOP)
            self.dx = 0
            if self.backw :
                s.send(BACKWARD)
            if self.forw :
                s.send(FORWARD)
            if self.sx :
                s.send(TURN_LEFT)

    def not_left(self):
        if self.sx:
            s.send(STOP)
            self.sx = 0
            if self.backw :
                s.send(BACKWARD)
            if self.dx :
                s.send(TURN_RIGHT)
            if self.forw :
                s.send(FORWARD)

    def	camera_up(self):
        if self.in_angle_v < max_angle - 50 :
            self.in_angle_v = self.in_angle_v + 2
            self.ANGLE_V = ANGLE_V % chr(self.in_angle_v)
            s.send(self.ANGLE_V)			
            time.sleep(0.02)	

    def	camera_down(self):
        if self.in_angle_v > 10 :
            self.in_angle_v = self.in_angle_v - 2
            self.ANGLE_V = ANGLE_V % chr(self.in_angle_v)
            s.send(self.ANGLE_V)			
            time.sleep(0.02)

    def camera_right(self) :
        if self.in_angle_h > 20 :
            self.in_angle_h = self.in_angle_h - 2
            self.ANGLE_H = ANGLE_H % chr(self.in_angle_h)
            s.send(self.ANGLE_H)
            time.sleep(0.02)

    def camera_left(self) :
        if self.in_angle_h < max_angle :
            self.in_angle_h = self.in_angle_h + 2
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
            self.set_speed = 0
            s.send(STOP)
            self.forw = 0
            self.backw = 0
            self.dx = 0
            self.sx = 0
            flag_camup = 0
	    flag_camdown = 0
    	    flag_camr = 0
            flag_caml = 0

            print("\n___________________________________________________________________")
            print("Set a new gear:")
            print("   v = gear 1st(high accuracy)")
            print("   b = gear 2nd")
            print("   n = gear 3rd")
            print("   m = gear 4th!(full power)")  

            while not(self.set_speed): 

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
                            print("press ESC on the video to close it")
                            s.close()
			    sys.exit()

			if event.type == pygame.KEYDOWN:
			    if event.key == pygame.K_v:
	                        self.VELOCITY_R = "\xFF\x02\x01\x02\xFF"
	                        self.VELOCITY_L = "\xFF\x02\x02\x02\xFF"
	                        s.send(self.VELOCITY_R)
	                        s.send(self.VELOCITY_L)
	                        print("")
	                        print("speed set to slow")
	                        self.set_speed = 1
				break
	                    elif event.key == pygame.K_b:
	                        self.VELOCITY_R = "\xFF\x02\x01\x0A\xFF"
	                        self.VELOCITY_L = "\xFF\x02\x02\x0A\xFF"
	                        s.send(self.VELOCITY_R)
	                        s.send(self.VELOCITY_L)
	                        print("")
	                        print("speed set to medium")
	                        self.set_speed = 1  
				break     
	                    elif event.key == pygame.K_n:
	                        self.VELOCITY_R = "\xFF\x02\x01\x2F\xFF"
	                        self.VELOCITY_L = "\xFF\x02\x02\x2F\xFF"
	                        s.send(self.VELOCITY_R)
	                        s.send(self.VELOCITY_L)
	                        print("")
	                        print("speed set to fast")
	                        self.set_speed = 1
				break
	                    elif event.key == pygame.K_m:
	                        self.VELOCITY_R = "\xFF\x02\x01\x5A\xFF"
	                        self.VELOCITY_L = "\xFF\x02\x02\x5A\xFF"
	                        s.send(self.VELOCITY_R)
	                        s.send(self.VELOCITY_L)
	                        print("")
	                        print("speed set to insane, good luck!")
                        	self.set_speed = 1
				break
            print("___________________________________________________________________\n") 


robot = robot()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("press ESC on the video to close it")
            s.close()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:
                robot.forward()

            if event.key == pygame.K_s:
                robot.backward()

            if event.key == pygame.K_d:
                robot.right()

            if event.key == pygame.K_a:
                robot.left()

            if event.key == pygame.K_i:
		flag_camup = 1

            if event.key == pygame.K_l:
                flag_camr = 1

            if event.key == pygame.K_j:
		flag_caml = 1

            if event.key == pygame.K_k:
                flag_camdown = 1

            if event.key == pygame.K_o:
                robot.gear_change()

            if event.key == pygame.K_p:
                robot.camera_reset()
	
	        
    	if event.type == pygame.KEYUP:
	        
            if event.key == pygame.K_w:
                robot.not_forward()

            if event.key == pygame.K_s:
                robot.not_backward()

            if event.key == pygame.K_d:
                robot.not_right()

            if event.key == pygame.K_a:
                robot.not_left()

            if event.key == pygame.K_i:
		flag_camup = 0

            if event.key == pygame.K_l:
                flag_camr = 0

            if event.key == pygame.K_j:
		flag_caml = 0

            if event.key == pygame.K_k:
                flag_camdown = 0

    if flag_camup:
        robot.camera_up()

    if flag_camdown:
	robot.camera_down()

    if flag_camr :
	robot.camera_right()

    if flag_caml :
	robot.camera_left()



