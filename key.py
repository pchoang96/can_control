import sys, termios, tty, os, time
button_delay = 0.06
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

check1 = True
while check1:
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print '\nkeyboard control program'
        linear_speed = 100
        angular_speed = 0.5
        while True:
            char = getch()
            print char
            if (char == " "):
                print("Stop!")
            if (char == "a"):
                print("Left turn")
                time.sleep(button_delay)
            elif (char == "d"):
                print("Right turn")
                time.sleep(button_delay)
            elif (char == "w"):
                print("Foward")
                time.sleep(button_delay)
            elif (char == "s"):
                print("Go back")
                time.sleep(button_delay)

            elif (char == 'r'):
				linear_speed += 5
				print 'linear_speed: ',linear_speed
				time.sleep(button_delay)

            elif (char == 'f'):
				linear_speed -= 5
				print 'linear_speed: ',linear_speed
				time.sleep(button_delay)

            elif (char == 't'):
				angular_speed += 0.1
				print 'angular_speed: ',angular_speed
				time.sleep(button_delay)

            elif (char == 'g'):
				angular_speed -= 0.1
				print 'angular_speed: ',angular_speed
				time.sleep(button_delay)
			
            elif (char == "b"):
                time.sleep(button_delay)
                print "back to automatic traking loop"
                break
            elif char == "k":
                print 'break program'
                time.sleep(button_delay)
                check1 = False
                break