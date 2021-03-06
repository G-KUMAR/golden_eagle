#!/usr/bin/env python

from geometry_msgs.msg import PoseStamped
import rospy
import tf.transformations
import numpy as np
from numpy import median

arr_x = []
arr_y = []
arr_z = []
arr_yaw = []
window_size=10

def tag_detect_node():

	global aruco_filtered_pose_pub
	rospy.init_node('aruco_transform', anonymous=True)
	aruco_filtered_pose_pub = rospy.Publisher("/aruco_single/filtered_pose", PoseStamped, queue_size=10)
	aruco_tag_sub = rospy.Subscriber("/aruco_single/pose",PoseStamped, tag_detection_cb)
	rospy.spin()

def tag_detection_cb(msg):

	pos_x = msg.pose.position.x
	pos_y = msg.pose.position.y
	pos_z = msg.pose.position.z

	orient_x = msg.pose.orientation.x
	orient_y = msg.pose.orientation.y
	orient_z = msg.pose.orientation.z
	orient_w = msg.pose.orientation.w

	angles = tf.transformations.euler_from_quaternion([msg.pose.orientation.x,msg.pose.orientation.y,msg.pose.orientation.z,msg.pose.orientation.w], axes='sxyz')
	yaw = angles[2]

	print(yaw)
	# print('Before')
	# print(arr_x)
	# print(arr_y)
	# print(arr_z)

	if len(arr_x)<window_size:
		arr_x.append(pos_x)
		arr_y.append(pos_y)
		arr_z.append(pos_z)
		arr_yaw.append(yaw)
	else:
		arr_x.pop(0)
		arr_y.pop(0)
		arr_z.pop(0)
		arr_yaw.pop(0)
		arr_x.append(pos_x)
		arr_y.append(pos_y)
		arr_z.append(pos_z)
		arr_yaw.append(yaw)

		filtered_yaw = median(arr_yaw)

		x,y,z,w = tf.transformations.quaternion_from_euler(0, 0, filtered_yaw, axes='sxyz')
		
		filtered = PoseStamped()
		filtered.header.stamp = rospy.Time.now()
		filtered.header.frame_id = "home"
		filtered.pose.position.x = median(arr_x)
		filtered.pose.position.y = median(arr_y)
		filtered.pose.position.z = median(arr_z)
		filtered.pose.orientation.x = x
		filtered.pose.orientation.y = y
		filtered.pose.orientation.z = z
		filtered.pose.orientation.w = w
		aruco_filtered_pose_pub.publish(filtered)

		# print('Median')
		# print(filtered.pose.position.x)
		# print(filtered.pose.position.y)
		# print(filtered.pose.position.z)
	# print('After')
	# print(arr_x)
	# print(arr_y)
	# print(arr_z)

	print('\n')



if __name__ == '__main__':
	try:
		tag_detect_node()
	except rospy.ROSInterruptException:
		pass
