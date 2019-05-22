from function import *
import line_tracking as track
import infrared_sensor as ir
import usonic_sensor as sonic
import RPi.GPIO as GPIO
from time import sleep


motorLeft = 25
motorRight = 59
#TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
#      3                 5                  4                   18
TrackSensorLeftPin2  =  4  #The second tracking infrared sensor pin on the left is connected to  BCM port 5 of Raspberry pi
TrackSensorLeftPin1  =  17   #The first tracking infrared sensor pin on the left is connected to  BCM port 3 of Raspberry pi
TrackSensorRightPin1 =  14   #The first tracking infrared sensor pin on the right is connected to  BCM port 4 of Raspberry pi
TrackSensorRightPin2 =  2  #The second tracking infrared sensor pin on the right is connected to  BCMport 18 of Raspberry pi

#infrared input pin------------------------
infra_left 	= 15
infra_right = 25

sonic_left = 0
sonic_left_trig = 23		#sonic trigger pin: GPIO 23
sonic_left_echo = 24		#sonic echo pin: GPIO 24
#check_distance(sonic_left_trig,sonic_left_echo)

sonic_right = 0
sonic_right_trig = 22		#sonic trigger pin: GPIO 25
sonic_right_echo = 27	#sonic echo pin: GPIO 8
#check_distance(sonic_right_trig,sonic_right_echo)

#SPI-mcp2515 pin:
"""
mcp2515			Raspberry

VCC		---		5V pin
GND		---		GND
SI		---		MOSI/GPIO 10
SO		---		MISO/GPIO 9
SCK/CLK	---		SCLK/GPIO 11
CS		---		CS0/GPIO 8
"""
track.moving_speed=1000
track.r_wheel = 1000
track.l_wheel = 1000
sensor_delay_time = 0.5
          #---trackSensorLeftValue2/|TrackSensorLeftValue1||TrackSensorRightValue1||TrackSensorRightValue2--------------
def init_all():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TrackSensorLeftPin2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TrackSensorLeftPin1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TrackSensorRightPin1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TrackSensorRightPin2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    sonic.setup_sonic(sonic_left_trig,sonic_left_echo)
    sonic.setup_sonic(sonic_right_trig,sonic_right_echo)
    ir.init_ir(infra_right)
    ir.init_ir(infra_left)
    mcp2515_init()
    set_mode('speed',motorLeft)
    set_mode('speed',motorRight)

#main programs---------------------------------------------------------------------

init_all()
try:
	while True:
		line = track.line_track(TrackSensorLeftPin2, TrackSensorLeftPin1,  TrackSensorRightPin1, TrackSensorRightPin2)
		speed = track.tracking_rule(line,30,60,90)
		spdLeft=speed[0]
		spdRight=speed[1]
		if not speed[2]:
			print spdLeft,spdRight
			set_speed(spdLeft,motorLeft)
			set_speed(spdRight,motorRight)
			time.sleep(sensor_delay_time)
		elif speed[2]:
			time.sleep(0.05)
			line = track.line_track(TrackSensorLeftPin2, TrackSensorLeftPin1,  TrackSensorRightPin1, TrackSensorRightPin2)
			if line == [1,1,1,1]:
				pass
			else:
				break
			break_motor()
			print "reading aruco"
			speed_motion(0,2)
			line = track.line_track(TrackSensorLeftPin2, TrackSensorLeftPin1,  TrackSensorRightPin1, TrackSensorRightPin2)
			while line != [1,1,1,1] and line != [0,1,1,1] and line != [1,1,1,0]
				line = track.line_track(TrackSensorLeftPin2, TrackSensorLeftPin1,  TrackSensorRightPin1, TrackSensorRightPin2)
			while True
				line = track.line_track(TrackSensorLeftPin2, TrackSensorLeftPin1,  TrackSensorRightPin1, TrackSensorRightPin2)
				if line[1] == 0 or line[2] == 0
					break_motor()
					break				
#------------------------------------------------------------------------------------------------------
		while not ir.check_obstacle(infra_left) or not ir.check_obstacle(infra_right):
			break_motor()
			if not ir.check_obstacle(infra_left):
				print 'IR: obstacle left'
			if not ir.check_obstacle(infra_right):
				print 'IR: obstacle right'
			time.sleep(sensor_delay_time)
#-----------------------------------------------------------------------------------------------------
		sonicLeft = sonic.check_distance(sonic_left_trig,sonic_left_echo)
		sonicRight = sonic.check_distance(sonic_right_trig,sonic_right_echo)
		while sonicLeft <=20 or sonicRight<=20:
				break_motor();
				sonicLeft = sonic.check_distance(sonic_left_trig,sonic_left_echo)
				sonicRight = sonic.check_distance(sonic_right_trig,sonic_right_echo)
				if sonicLeft <=20 and sonicRight<=20:
					print 'obstacle ahead:',sonicLeft,sonicRight
				elif sonicLeft <=20 and sonicRight>20:
					print 'obstacle left: ',sonicLeft,'ahead'
				elif sonicLeft >20 and sonicRight<=20:
					print 'obstacle right: ',sonicRight,'ahead'
				time.sleep(sensor_delay_time)
except KeyboardInterrupt:
	break_motor()
	GPIO.cleanup()
