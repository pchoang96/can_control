import RPi.GPIO as GPIO
from time import sleep
from function import *

moving_speed =0
r_wheel =0
l_wheel =0
double_delay_time=0
prev_buff = [0,0,0,0]
def init_line(TrackSensorLeftPin2,TrackSensorLeftPin1, TrackSensorRightPin1, TrackSensorRightPin2):
	GPIO.setup(TrackSensorLeftPin2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(TrackSensorLeftPin1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(TrackSensorRightPin1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(TrackSensorRightPin2,GPIO.IN,pull_up_down=GPIO.PUD_UP)

def line_track(TrackSensorLeftPin2,TrackSensorLeftPin1, TrackSensorRightPin1, TrackSensorRightPin2 ):
    TrackSensorLeftValue2  = GPIO.input(TrackSensorLeftPin2)
    TrackSensorLeftValue1  = GPIO.input(TrackSensorLeftPin1)
    TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
    TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)
    buff = [0,0,0,0]
    buff[0]=TrackSensorLeftValue2
    buff[1]=TrackSensorLeftValue1
    buff[2]=TrackSensorRightValue1
    buff[3]=TrackSensorRightValue2
    # print TrackSensorLeftValue2,TrackSensorLeftValue1,TrackSensorRightValue1,TrackSensorRightValue2
    return buff
def tracking_rule(buff,l,m,h):
	global l_wheel
	global r_wheel
	global moving_speed
	global prev_buff
	print buff
	if buff != [1,0,0,1] and buff != [0,1,1,1] and buff != [0,0,0,1] and buff != [0,1,0,0] and buff != [0,0,1,0] and buff != [1,0,0,0] and buff != [1,1,1,0] and buff != [0,0,0,0] and buff != [1,1,1,1] and buff != [1,1,0,0] and buff != [0,0,1,1]:
		print 'UNDEFINE'
		buff = prev_buff
	if buff == [1,0,0,1]:
		l_wheel = moving_speed; r_wheel = moving_speed
		lv = l_wheel ; rv = r_wheel
	elif buff == [1,0,0,0]:
		lv = l_wheel*m/100; rv = r_wheel*h/100

	elif buff == [1,1,1,0]:
		lv = l_wheel*h/100; rv = r_wheel*l/100

	elif buff == [0,1,0,0] or buff == [1,1,0,0]:
		lv = l_wheel*h/100; rv = r_wheel*m/100

	elif buff == [0,0,1,0] or buff == [0,0,1,1]:
		lv = l_wheel*m/100; rv = r_wheel*h/100			

	elif buff == [0,1,1,1]:
		lv = l_wheel*l/100; rv = r_wheel*h/100

	elif buff == [0,0,0,1]:
		lv = l_wheel*h/100; rv = r_wheel*m/100

	elif buff == [0,0,0,0]:
		pass
		prev_buff = buff
		return [0,0,1]
	elif buff == [1,1,1,1]:
		print buff
		l_wheel = moving_speed; r_wheel = moving_speed
		lv = -l_wheel*m/100; rv = -r_wheel*m/100
	else:
		print buff
		lv = 0; rv = 0
	prev_buff = buff
	return [int(lv),int(rv),0]
