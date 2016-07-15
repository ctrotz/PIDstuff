#!/usr/bin/env python
import rospy, math
from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped
from PID import PIDController

class pidDriver:
    try:
	    def __init__(self, d_des, speed):
		self.error = 0 # initializes the running error counter
		self.d_des = d_des # takes desired dist from wall
		self.speed = speed
		self.scan = [0]
		rospy.init_node("wall_PID",  anonymous=False)
		rate = rospy.Rate(10)
		pid = PIDController(rospy.Time.now().to_sec(), 0.1,0.00000001,0.07)
		#init the pub/subs
		self.drive = rospy.Publisher("/racecar/ackermann_cmd_mux/input/teleop",  AckermannDriveStamped,  queue_size=5)
		rospy.Subscriber("/racecar/laser/scan",  LaserScan,  self.callback)
		
		drive_msg = AckermannDriveStamped()
		drive_msg.drive.steering_angle = 0.0
		drive_msg.drive.speed = self.speed
		
		dist_trav = 50.0
		total = 0.0
		
		time = dist_trav/self.speed
		ticks = int(time * 10)
		for t in range(ticks):
		    self.error = 0
		    total = 0
		    meanD = 0
		    for i in self.scan:
		        total += i
		    meanD = total/len(self.scan)
		    self.error = self.d_des - meanD
		    print str(self.error)
		    pidVal = pid.update(self.error,  rospy.Time.now().to_sec())
		    pidVal = pidVal/abs(pidVal) * min(1.0,  abs(pidVal)) if pidVal!=0 else 0
		    print pidVal
		    drive_msg.drive.steering_angle = pidVal
		    self.drive.publish(drive_msg)
		    print "published"
		    rate.sleep()
		self.drive.publish(AckermannDriveStamped())
	    def callback(self,msg):
		self.scan = []	
		for i in range(355, 366):
			self.scan.append(msg.ranges[i])
	    
	    def shutdown(self):
		rospy.loginfo("Stopping robot")
		self.drive.publish(AckermannDriveStamped())
		rospy.sleep(1)
    except KeyboardInterrupt:
	self.shutdown()
if __name__ == "__main__":
    #try:
	pidDriver(1.5,1.5)
    	rospy.spin()
   ## except:
	#rospy.loginfo("PID Driver terminated")
