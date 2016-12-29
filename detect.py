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


def loadLabelsMap(path,labelsMap):
	f=open(path,'r')

	if f==None:
		print 'Labels map file [%s] not found! '%(path)
		return
	lines=f.readlines()
	lines.remove(lines[0])
	for l in lines:
		parts=l.split(':')
		labelsMap[int(parts[0])]=parts[1].strip()

if __name__ == '__main__':


	labelsMap={}
	loadLabelsMap(config.LABELS_FILE,labelsMap)
	# Load training data into model
	print 'Loading training data...'
	model = cv2.createEigenFaceRecognizer()#cv2.createLBPHFaceRecognizer(3,8,8,8)#
	model.load(config.TRAINING_FILE)
	print 'Training data loaded!'
	# Initialize camer and box.
	camera = config.get_camera()
	# Move box to locked position.

	cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('frame', 640,480)


	foundLabels={}
	total=0
	while config.CheckLetterInput('q')==False:
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
		crop = face.process(face.crop(image, x, y, w, h))
		cv2.imshow('frame', crop)

		total+=1

		# Test face against model.
		label, confidence = model.predict(crop)
		print 'detected [%s] with confidence %f'%(labelsMap[label],confidence)

		if not label in foundLabels:
			foundLabels[label]=0
		foundLabels[label]+=1

	for l,c in foundLabels.items:
		print "Label %s: %f%"%(labelsMap[l],100*c/total)
	cv2.destroyAllWindows()
