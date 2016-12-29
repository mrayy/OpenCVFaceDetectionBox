
import fnmatch
import os
import sys

import cv2
import numpy as np

import config
import face




def walk_files(directory, match='*'):
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, match):
            yield os.path.join(root, filename)

def prepare_image(filename):
    return cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

def normalize(X, low, high, dtype=None):
    """Normalizes a given array in X to a value between low and high.
    Adapted from python OpenCV face recognition example at:
      https://github.com/Itseez/opencv/blob/2.4/samples/python2/facerec_demo.py
    """
    X = np.asarray(X)
    minX, maxX = np.min(X), np.max(X)
    # normalize to [0...1].
    X = X - float(minX)
    X = X / float((maxX - minX))
    # scale to [low...high].
    X = X * (high-low)
    X = X + low
    if dtype is None:
        return np.asarray(X)
    return np.asarray(X, dtype=dtype)

def AddLabels(labelID,dir,labels,faces):
    count=0
    for filename in walk_files(dir, '*.pgm'):
        faces.append(prepare_image(filename))
        labels.append(labelID)
        count+=1
    return count

if __name__ == '__main__':
    print "Reading training images..."
    faces = []
    labels = []
    pos_count = 0
    neg_count = 0
    trainingRoot="training/"
    ID=1
    labelMap=[]
    totalCount=0
    for d in os.listdir(trainingRoot):
        count=AddLabels(ID,trainingRoot+d,labels,faces)
        if(count>0):
            labelMap.append([ID,d,count])
            print 'Found %d pictures for %s'%(count,d)
            ID+=1
        totalCount+=count

    print "Total training photos count is: %d"%(totalCount)
    f=open(config.LABELS_FILE,'w')
    f.write('%d,%d\r\n'%(config.FACE_WIDTH,config.FACE_HEIGHT))#write image size
    for l in labelMap:
        f.write('%d : %s\r\n'%(l[0],l[1]))
    f.close()

    print 'Training model...'
    model = cv2.createEigenFaceRecognizer()#cv2.createLBPHFaceRecognizer(3,8,8,8)#createEigenFaceRecognizer()
    model.train(np.asarray(faces), np.asarray(labels))

    # Save model results
    model.save(config.TRAINING_FILE)
    print 'Training data saved to', config.TRAINING_FILE

    # Save mean and eignface images which summarize the face recognition model.
    mean = model.getMat("mean").reshape(faces[0].shape)
    cv2.imwrite(config.TRAINING_FOLDER+'mean.png', normalize(mean, 0, 255, dtype=np.uint8))
    eigenvectors = model.getMat("eigenvectors")
    for l in labelMap:
        img_eigenvector = eigenvectors[:,l[0]].reshape(faces[0].shape)
        cv2.imwrite(config.TRAINING_FOLDER+ l[1]+'.png', normalize(img_eigenvector, 0, 255, dtype=np.uint8))
