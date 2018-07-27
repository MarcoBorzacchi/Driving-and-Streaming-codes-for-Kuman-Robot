import sys
import socket
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import getpass
import time
#import webbrowser
#from subprocess import Popen, check_call, STDOUT, PIPE
from tcp_remote_mobile import robot

VELOCITY_R_VECTOR = [ "\xFF\x02\x01\x02\xFF", "\xFF\x02\x01\x0A\xFF", "\xFF\x02\x01\x20\xFF", "\xFF\x02\x01\x33\xFF", "\xFF\x02\x01\x5A\xFF"]
VELOCITY_L_VECTOR = [ "\xFF\x02\x02\x02\xFF", "\xFF\x02\x02\x0A\xFF", "\xFF\x02\x02\x20\xFF", "\xFF\x02\x02\x33\xFF", "\xFF\x02\x02\x5A\xFF"]

	
class Window(QWidget):
	def __init__(self, parent = None):
		super(Window, self).__init__(parent)
		self.setWindowTitle("Robot controller GUI (for remote usage)")
		self.setGeometry(50, 100, 500, 300)
		self.setFixedSize(self.size())
		self.running = 0
                
                self.controls = QLabel('List of commands:')
                #first row
                self.hbox =  QHBoxLayout()
                self.hbox.addWidget(self.controls)
                self.hbox.addStretch()
                #second row
                self.move = QLabel('Motor control')
		self.cam = QLabel('Camera control')
		
		self.hbox1 = QHBoxLayout()
		self.hbox1.addStretch()
		self.hbox1.addWidget(self.move)
		self.hbox1.addStretch()
		self.hbox1.addStretch()
		self.hbox1.addWidget(self.cam)
		self.hbox1.addStretch()
		#third row
		self.fwdbutton = QPushButton('Forward', self)
		self.fwdbutton.pressed.connect(self.fwdbut)
		self.fwdbutton.released.connect(self.stopper)
		
		self.cupb = QPushButton('Camera Up', self)
		self.cupb.pressed.connect(self.camup)
		
		self.hbox2 = QHBoxLayout()
		self.hbox2.addStretch()
		self.hbox2.addWidget(self.fwdbutton)
		self.hbox2.addStretch()
		self.hbox2.addStretch()
		self.hbox2.addWidget(self.cupb)
		self.hbox2.addStretch()
		
		#fourth row
		self.leftbutton = QPushButton('Turn Left', self)
		self.leftbutton.pressed.connect(self.leftbut)
		self.leftbutton.released.connect(self.stopper)
		
		self.rightbutton = QPushButton('Turn Right', self)
		self.rightbutton.pressed.connect(self.rightbut)
		self.rightbutton.released.connect(self.stopper)
		
		self.crightb = QPushButton('Camera Right', self)
		self.crightb.pressed.connect(self.camright)
		
		self.cleftb = QPushButton('Camera Left', self)
		self.cleftb.pressed.connect(self.camleft)
		
		
		self.hbox3 = QHBoxLayout()
		self.hbox3.addWidget(self.leftbutton)
		self.hbox3.addStretch()
		self.hbox3.addWidget(self.rightbutton)
		self.hbox3.addWidget(self.cleftb)
		self.hbox3.addStretch()
		self.hbox3.addWidget(self.crightb)
		#fifth row
		
		self.bwdbutton = QPushButton('Back Off', self)
		self.bwdbutton.pressed.connect(self.bwdbut)
		self.bwdbutton.released.connect(self.stopper)
		
		self.cdownb = QPushButton('Camera Down', self)
		self.cdownb.pressed.connect(self.camdown)
				
		
		self.hbox4 = QHBoxLayout()
		self.hbox4.addStretch()
		self.hbox4.addWidget(self.bwdbutton)
		self.hbox4.addStretch()
		self.hbox4.addStretch()
		self.hbox4.addWidget(self.cdownb)
		self.hbox4.addStretch()
		
		#sixth row
		
		self.gear=QLabel('Robot speed:')
		self.camera_speed=QLabel('Camera speed:')
		
		self.hbox5 = QHBoxLayout()
		self.hbox5.addStretch()
		self.hbox5.addWidget(self.gear)
		self.hbox5.addStretch()
		self.hbox5.addStretch()
		self.hbox5.addWidget(self.camera_speed)
		self.hbox5.addStretch()
		
		#7th row
		
		self.sl = QSlider(Qt.Vertical)
		self.sl.setMinimum(0)
		self.sl.setMaximum(4)
		self.sl.setValue(2)
		self.sl.setTickPosition(QSlider.TicksBelow)
		self.sl.setTickInterval(5)
		self.sl.valueChanged.connect(self.gear_changed)
		
		self.sl2 = QSlider(Qt.Vertical)
		self.sl2.setMinimum(0)
		self.sl2.setMaximum(4)
		self.sl2.setValue(2)
		self.sl2.setTickPosition(QSlider.TicksBelow)
		self.sl2.setTickInterval(5)
		self.sl2.valueChanged.connect(self.camera_speed_changed)
		
		self.hbox6 = QHBoxLayout()
		self.hbox6.addStretch()
		self.hbox6.addWidget(self.sl)
		self.hbox6.addStretch()
		self.hbox6.addStretch()
		self.hbox6.addWidget(self.sl2)
		self.hbox6.addStretch()
		
		#8th row
                
                self.camerarstbutton = QPushButton('Reset Camera', self)
		self.camerarstbutton.clicked.connect(self.rst_camera)
		
		self.hbox7 = QHBoxLayout()
		self.hbox7.addStretch()
		self.hbox7.addStretch()
		self.hbox7.addWidget(self.camerarstbutton)
		self.hbox7.addStretch()
		self.hbox7.addStretch()
		##########################################################
		
		
                
                self.vbox = QVBoxLayout()
                
                self.vbox.addLayout(self.hbox)
                self.vbox.addStretch()
                self.vbox.addLayout(self.hbox1)
                self.vbox.addLayout(self.hbox2)
                self.vbox.addLayout(self.hbox3)
                self.vbox.addLayout(self.hbox4)
                self.vbox.addStretch()
                self.vbox.addLayout(self.hbox5)
                self.vbox.addLayout(self.hbox6)
		self.vbox.addLayout(self.hbox7)
		
		self.setLayout(self.vbox)
		self.robot_instance = robot()
	
	def fwdbut(self):
            self.robot_instance.fwdbut()
        
        def bwdbut(self):
            self.robot_instance.bwdbut()
        
        def rightbut(self):
            self.robot_instance.rightbut()
        
        def leftbut(self):
            self.robot_instance.leftbut()
        
        def stopper(self):
            self.robot_instance.stopper()
    
        def camup(self):
            self.robot_instance.camera_goup()        
        
        def camdown(self):
            self.robot_instance.camera_godown()
            
        def camright(self):
            self.robot_instance.camera_goright()
            
        def camleft(self):
            self.robot_instance.camera_goleft()
		
	def rst_camera(self):
		self.robot_instance.camera_reset()
		
	def run(self): # start the robot controlling algorithm (tcp.py file)
		if (self.running==1):
			self.running = 0
			self.runbutton.setText('Run')
		else:
			self.running = 1
			self.runbutton.setText('Stop')
			while (self.running == 1):
				self.robot_instance.run()
				QCoreApplication.processEvents()
			
	def gear_changed(self):
		self.robot_instance.VELOCITY_R = VELOCITY_R_VECTOR[self.sl.value()]
		self.robot_instance.VELOCITY_L = VELOCITY_L_VECTOR[self.sl.value()]
		self.robot_instance.gear_change()
		
	def camera_speed_changed(self):
		self.robot_instance.angle_delta = self.sl2.value()+ 1
		
	def edit(self):
		if len(self.forwardEdit.text()) == 1:
			self.robot_instance.forward = str(self.forwardEdit.text())
		if len(self.backwardEdit.text()) == 1:
			self.robot_instance.backward = str(self.backwardEdit.text())
		if len(self.rightEdit.text()) == 1:
			self.robot_instance.right = str(self.rightEdit.text())
		if len(self.leftEdit.text()) == 1:
			self.robot_instance.left = str(self.leftEdit.text())
		if len(self.crightEdit.text()) == 1:
			self.robot_instance.cam_r = str(self.crightEdit.text())
		if len(self.cleftEdit.text()) == 1:
			self.robot_instance.cam_l = str(self.cleftEdit.text())
		if len(self.upEdit.text()) == 1:
			self.robot_instance.cam_up = str(self.upEdit.text())
		if len(self.downEdit.text()) == 1:
			self.robot_instance.cam_down = str(self.downEdit.text())

		self.robot_instance.reset_cam = 'p'

	def closeEvent(self, event):
		self.robot_instance.close_conn()
		event.accept()

		
def main():
	app = QApplication(sys.argv)
	win = Window()
	win.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
