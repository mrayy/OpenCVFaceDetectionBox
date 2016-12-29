
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
    return face.process(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

if __name__ == '__main__':
    files=walk_files(config.TRAINING_FOLDER,'*.pgm')
    for d in files:
        f=prepare_image(d)
        cv2.imwrite(d,f)
