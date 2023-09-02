#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

msg = """
Control Your Turtle!
---------------------------
Moving around:
   m1
m3  s  m4
   m2

m1/m2 : increase/decrease linear velocity
m3/m4 : increase/decrease angular velocity
space key, s : stop
CTRL-C to quit
"""

 'right' : (1, 0),
 'left': (-1, 0),
 'up': (0, 1),
'down': (0, -1)

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key



 speed = 0.5
 turn = 0.5
 
def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed, turn)

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('turtle_keyboard_control')

   
    pub =  pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    try:
        print(msg)
        print(vels(speed, turn))
        while True:
            ## gets keyboard press, then controls turtle if it's a key defined in moveKeys
            key = getKey()
            if key in moveKeys.keys():
                x = moveKeys[key][0]
                theta = moveKeys[key][1]
            else:
                x = 0
                theta = 0
                if (key == '\x03'):
                    break
            
            ###TODO: create a new Twist message ###
            twist_msg = Twist()
            twist_msg.linear.x = x * speed
            twist_msg.angular.z = theta * turn

            pub.publish( twist_msg)

    except Exception as e:
        print(e)

    finally:
        stop_msg= Twist()
        stop_msg.linear.x = 0
        stop_msg.angular.z = 0
        pub.publish(stop_msg)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
