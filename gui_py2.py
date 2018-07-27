import sys
import socket
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import getpass
import time
from tcp_py2 import robot

VELOCITY_R_VECTOR = [ "\xFF\x02\x01\x02\xFF", "\xFF\x02\x01\x0A\xFF", "\xFF\x02\x01\x20\xFF", "\xFF\x02\x01\x33\xFF", "\xFF\x02\x01\x5A\xFF"]
VELOCITY_L_VECTOR = [ "\xFF\x02\x02\x02\xFF", "\xFF\x02\x02\x0A\xFF", "\xFF\x02\x02\x20\xFF", "\xFF\x02\x02\x33\xFF", "\xFF\x02\x02\x5A\xFF"]
	
class Window(QWidget):
	def __init__(self, parent = None):
		super(Window, self).__init__(parent)
		self.setWindowTitle("Robot controller GUI")
		self.setGeometry(250, 700, 450, 250)
		self.setFixedSize(self.size())
		self.running = 0
		# GUI widgets ----------------------
		self.gear=QLabel('Gear')
		self.sl = QSlider(Qt.Vertical)
		self.sl.setMinimum(0)
		self.sl.setMaximum(4)
		self.sl.setValue(2)
		self.sl.setTickPosition(QSlider.TicksBelow)
		self.sl.setTickInterval(5)
		self.sl.valueChanged.connect(self.gear_changed)
		
		self.camera_speed=QLabel('Camera speed')
		self.sl2 = QSlider(Qt.Vertical)
		self.sl2.setMinimum(0)
		self.sl2.setMaximum(4)
		self.sl2.setValue(2)
		self.sl2.setTickPosition(QSlider.TicksBelow)
		self.sl2.setTickInterval(5)
		self.sl2.valueChanged.connect(self.camera_speed_changed)
		
		self.controls=QLabel('List of commands:')
		self.forward=QLabel('Forward')
		self.forwardEdit = QLineEdit()
		self.forwardEdit.setText('w')
		self.forwardEdit.setMaxLength(1)
		self.backward= QLabel('Backward')
		self.backwardEdit = QLineEdit()
		self.backwardEdit.setText('s')
		self.backwardEdit.setMaxLength(1)
		self.right= QLabel('Right')
		self.rightEdit = QLineEdit()
		self.rightEdit.setText('d') 
		self.rightEdit.setMaxLength(1)
		self.left= QLabel('Left')
		self.leftEdit =  QLineEdit()
		self.leftEdit.setText('a')
		self.leftEdit.setMaxLength(1)
		
		self.up= QLabel('Camera up')
		self.upEdit =  QLineEdit()
		self.upEdit.setText('i')
		self.upEdit.setMaxLength(1)
		self.down= QLabel('Camera down')
		self.downEdit =  QLineEdit()
		self.downEdit.setText('k')
		self.downEdit.setMaxLength(1)
		self.cright= QLabel('Camera right')
		self.crightEdit =  QLineEdit()
		self.crightEdit.setText('l')
		self.crightEdit.setMaxLength(1)
		self.cleft= QLabel('Camera left')
		self.cleftEdit =  QLineEdit()
		self.cleftEdit.setText('j')
		self.cleftEdit.setMaxLength(1)
		
		self.runbutton = QPushButton('Run', self)
		self.runbutton.clicked.connect(self.run)
		self.editbutton = QPushButton('Edit commands', self)
		self.editbutton.clicked.connect(self.edit)
		self.camerarstbutton = QPushButton('Reset camera (p)', self)
		self.camerarstbutton.clicked.connect(self.rst_camera)
		
		# Layout arrangement
		self.vbox = QVBoxLayout()
		self.vbox2 = QVBoxLayout()
		self.vbox3 = QVBoxLayout()
		self.vbox4 = QVBoxLayout()
		self.vbox5 = QVBoxLayout()
		self.vbox6 = QVBoxLayout()
		self.vboxglob = QVBoxLayout()
		self.hbox = QHBoxLayout()
		self.hbox2 = QHBoxLayout()
		self.hbox3 = QHBoxLayout()
		
		self.vbox.addWidget(self.forward)
		self.vbox.addWidget(self.backward)
		self.vbox.addWidget(self.left)
		self.vbox.addWidget(self.right)
		
		self.vbox2.addWidget(self.forwardEdit)
		self.vbox2.addWidget(self.backwardEdit)
		self.vbox2.addWidget(self.leftEdit)
		self.vbox2.addWidget(self.rightEdit)
		
		self.vbox3.addWidget(self.up)
		self.vbox3.addWidget(self.down)
		self.vbox3.addWidget(self.cleft)
		self.vbox3.addWidget(self.cright)
		
		self.vbox4.addWidget(self.upEdit)
		self.vbox4.addWidget(self.downEdit)
		self.vbox4.addWidget(self.cleftEdit)
		self.vbox4.addWidget(self.crightEdit)
		
		self.vbox5.addWidget(self.gear)
		self.vbox5.addWidget(self.sl)
		self.vbox5.setAlignment(self.sl, Qt.AlignCenter)
		
		self.vbox6.addWidget(self.camera_speed)
		self.vbox6.addWidget(self.sl2)
		self.vbox6.setAlignment(self.sl2, Qt.AlignCenter)
		
		self.hbox.addLayout(self.vbox)
		self.hbox.addLayout(self.vbox2)
		self.hbox.addLayout(self.vbox3)
		self.hbox.addLayout(self.vbox4)
		self.hbox.addLayout(self.vbox5)
		self.hbox.addLayout(self.vbox6)
		
		self.hbox2.addWidget(self.editbutton)	
		self.hbox2.addWidget(self.camerarstbutton)	
		
		self.vboxglob.addWidget(self.controls)
		self.vboxglob.addLayout(self.hbox)
		self.vboxglob.addLayout(self.hbox2)
		self.vboxglob.addWidget(self.runbutton)
		
		self.setLayout(self.vboxglob)
		self.robot_instance = robot()
		
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
		self.robot_instance.angle_delta = self.sl2.value() + 1
		
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
