"""Raspberry Pi Face Recognition Treasure Box
Webcam OpenCV Camera Capture Device
Copyright 2013 Tony DiCola

Webcam device capture class using OpenCV.  This class allows you to capture a
single image from the webcam, as if it were a snapshot camera.

This isn't used by the treasure box code out of the box, but is useful to have
if running the code on a PC where only a webcam is available.  The interface is
the same as the picam.py capture class so it can be used in the box.py code
without any changes.
"""
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
