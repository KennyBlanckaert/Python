import argparse
import os
import sys

import cv2 as cv
import numpy as np

from matplotlib import pyplot as plt

#################### Preparation ####################

# Parsing variables
parser = argparse.ArgumentParser()
parser.add_argument(
    'filename1',
    help='Image filename used for conversion and saving.',
    type=str
)
parser.add_argument(
    'filename2',
    help='Image filename used for conversion and saving.',
    type=str
)
args = parser.parse_args()

# Save image path in variable
image_path1 = f'images/{args.filename1}'
image_path2 = f'images/{args.filename2}'

# Check if given path exists
if not os.path.exists(image_path1):
    print('Image does not exist.')
    sys.exit(1)
if not os.path.exists(image_path2):
    print('Image does not exist.')
    sys.exit(1)

# Read RGB image
image1 = cv.imread(image_path1, cv.IMREAD_COLOR)
image2 = cv.imread(image_path2, cv.IMREAD_COLOR)

#################### Exercice 13 ####################

orb = cv.ORB_create()

kp1, des1 = orb.detectAndCompute(image1, None)
kp2, des2 = orb.detectAndCompute(image2, None)

bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

matches = bf.match(des1, des2)
matches = sorted(matches, key = lambda x:x.distance)

# ! outImg should be optional, passing None instead as workaround
result = cv.drawMatches(image1, kp1, image2, kp2, matches[:48], None, flags=2)

# show
plt.imshow(result)
plt.show()