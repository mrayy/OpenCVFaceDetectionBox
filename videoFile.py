
import threading
import time

import cv2
import cv

import config


# Rate at which the webcam will be polled for new images.
CAPTURE_HZ = 10.0


class OpenCVVideo(object):
	def __init__(self, path):
		"""Create an OpenCV capture object associated with the provided webcam
		device ID.
		"""
		# Open the camera.
		self._camera = cv2.VideoCapture(path)

		if not self._camera.isOpened():
			self._camera.open()


	def read(self):
		retval, frame = self._camera.read()
		return frame
