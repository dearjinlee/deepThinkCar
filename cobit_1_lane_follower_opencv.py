import cv2
from adafruit_servokit import ServoKit
from cobit_opencv_lane_detect import CobitOpencvLaneDetect
from cobit_car_motor_l9110 import CobitCarMotorL9110
import time 


def main_loop():
	"""
	1단계: OpenCV를 이용한 차선인식 주행 \n
	OpenCV를 이용해서 차선의 각도를 인식하고, 차량 스티어링 휠을 회전함 \n
	차량 구동용 DC모터를 동작시켜서 차량을 전진시킴. 차선은 빨간색으로 고정되어 있음  \n
	차량이 차선을 정확하게 따라 가면 1단계 성공임 
	"""
	cv_detector = CobitOpencvLaneDetect()
	motor = CobitCarMotorL9110()
	servo = ServoKit(channels=16)

	SCREEN_WIDTH = 320
	SCREEN_HEIGHT = 240

	cap = cv2.VideoCapture(0)
	cap.set(3, SCREEN_WIDTH)
	cap.set(4, SCREEN_HEIGHT)

	servo_offset = 0
	servo.servo[0].angle = 90 + servo_offset

	time.sleep(2)

	for i in range(30):
		ret, img_org = cap.read()
		if ret:
			lanes, img_lane = cv_detector.get_lane(img_org)
			angle, img_angle = cv_detector.get_steering_angle(img_lane, lanes)
			if img_angle is None:
				print("angle image out!!")
				pass
			else:
				#print(angle)
				servo.servo[0].angle = angle + servo_offset		
				print(angle + servo_offset)	
				cv2.imshow("img_angle", img_angle)
				cv2.waitKey(1)
		else:
			print("cap error")



	motor.motor_move_forward(30)

	while True:
		ret, img_org = cap.read()
		if ret:
			lanes, img_lane = cv_detector.get_lane(img_org)
			angle, img_angle = cv_detector.get_steering_angle(img_lane, lanes)
			if img_angle is None:
				print("angle image out!!")
				pass
			else:
				#print(angle)
				servo.servo[0].angle = angle + servo_offset
				print(angle + servo_offset)	
				cv2.imshow("img_angle", img_angle)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		else:
			print("cap error")

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main_loop()
