"""Raspberry Pi Face Recognition Treasure Box
Treasure Box Script
Copyright 2013 Tony DiCola
"""
import cv2
import sys
import select

import sys
import select
import config
import face


def is_letter_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False

if __name__ == '__main__':
	# Load training data into model
	print 'Loading training data...'
	model = cv2.createEigenFaceRecognizer()#cv2.createLBPHFaceRecognizer(3,8,8,8)#
	model.load(config.TRAINING_FILE)
	print 'Training data loaded!'
	# Initialize camer and box.
	camera = config.get_camera()
	# Move box to locked position.

	cv2.namedWindow('dst_rt', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('dst_rt', 640,480)
	positive=0
	negative=0
	total=0
	while is_letter_input('q')==False:
		# Check if capture should be made.
		# TODO: Check if button is pressed.
		if True:
			# Check for the positive face and unlock if found.
			image = camera.read()
			if(image==None):
				break
			# Convert image to grayscale.
			image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
			# Get coordinates of single face in captured image.
			result = face.detect_single(image)
			if result is None:
				continue
			x, y, w, h = result
			# Crop and resize image to face.
			crop = face.resize(face.crop(image, x, y, w, h))
			cv2.imshow('dst_rt', crop)

			total+=1

			#cv2.imwrite("capture.pgm",crop)
			# Test face against model.
			label, confidence = model.predict(crop)
			print '{0}: {1} '.format(
				'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE',
				confidence)

			if label == config.POSITIVE_LABEL:
				positive+=1
			else:
				negative+=1

	print "Positive ratio:"+str(100*positive/total)+"%"
	print "Negative ratio:"+str(100*negative/total)+"%"
	cv2.destroyAllWindows()
