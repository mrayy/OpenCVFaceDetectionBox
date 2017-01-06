
import glob
import os
import sys
import select
import time
import cv2
import cv

#import hardware
import config
import face
import webcam



if __name__ == '__main__':
	path='output'
	if(len(sys.argv)>1):
		path=sys.argv[1]
	path+='.mp4'
	if os.path.exists(path):
		os.remove(path);
	fourcc = cv2.cv.CV_FOURCC(*'MP4V')
	out = cv2.VideoWriter(path,fourcc, 20.0, (640,480))
	cap = cv2.VideoCapture(0)
	if not cap.isOpened():
		cap.open()
	cap.set(cv.CV_CAP_PROP_FRAME_WIDTH,640);
	cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT,480);

	while(cap.isOpened()):
	    ret, frame = cap.read()
	    if ret==True:
			#frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
			out.write(frame)
			cv2.imshow('frame',frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
	    else:
	        break

	# Release everything if job is finished
	cap.release()
	out.release()

	cv2.destroyAllWindows()
