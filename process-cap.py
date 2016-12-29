

import glob
import os
import sys
import select
import time
import cv2

import config
import face


if __name__ == '__main__':
	if len(sys.argv)<2:
		print "Usage: python "+sys.argv[0] + " labelID [source video] "
		exit()
	if(len(sys.argv)>2):
		camera=config.get_video(sys.argv[2])
	else:
		camera = config.get_camera()
	PREFIX='image_'
	path=config.TRAINING_FOLDER+sys.argv[1]+'/'
	if not os.path.exists(path):
		os.makedirs(path)
	# Find the largest ID of existing positive images.
	# Start new images after this ID value.
	files = sorted(glob.glob(os.path.join(path,
		PREFIX+'[0-9][0-9][0-9].pgm')))
	count = 0
	if len(files) > 0:
		# Grab the count from the last filename.
		count = int(files[-1][-7:-4])+1

	print 'Press Ctrl-C to quit.'

	cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('frame', 640,480)
	while True:
		image = camera.read()
		if image==None:
			break
		# Convert image to grayscale.
		image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		# Get coordinates of single face in captured image.
		result = face.detect_single(image)
		if result is None:
			continue
		x, y, w, h = result
		# Crop image as close as possible to desired face aspect ratio.
		# Might be smaller if face is near edge of image.
		crop = face.process(face.crop(image, x, y, w, h))
		cv2.imshow('frame', crop)
		# Save image to file.
		filename = os.path.join(path, PREFIX + '%03d.pgm' % count)
		cv2.imwrite(filename, crop)
		config.printCounter('Processed: ',count)
		count += 1
		#time.sleep(0.1)
	sys.stdout.write('\n')
	cv2.destroyAllWindows()
