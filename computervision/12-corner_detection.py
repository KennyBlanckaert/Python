import argparse
import os
import sys

import cv2 as cv
import numpy as np

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

#################### Exercice 12 ####################

image1_grayscale = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)
image2_grayscale = cv.cvtColor(image2, cv.COLOR_BGR2GRAY)

corners1 = cv.goodFeaturesToTrack(image1_grayscale, 50, 0.01, 10)
corners2 = cv.goodFeaturesToTrack(image2_grayscale, 50, 0.01, 10)

for x in range(0, len(corners1)):
    for x, y in corners1[x]:
        cv.circle(image1, (x, y), 10, (0, 0, 0), 2)

for x in range(0, len(corners2)):
    for x, y in corners2[x]:
        cv.circle(image2, (x, y), 10, (0, 0, 0), 2)

# show
cv.imshow("Image 1", image1)
cv.imshow("Image 2", image2)
cv.waitKey(0)
cv.destroyAllWindows()

#################### Save ####################

# Create 'result' folder if not exists
print('Writing output files...')

output_directory = "result/"
if not os.path.isdir(output_directory):
    print('Output folder does not exist, creating it...')
    os.makedirs(output_directory)

# Save
image1_output = f'result/corners_{args.filename1}'
image2_output = f'result/corners_{args.filename2}'
success_1 = cv.imwrite(image1_output, image1)
success_2 = cv.imwrite(image2_output, image2)
if not success_1:
    print(f'Could not write to {image1_output}.')
if not success_2:
    print(f'Could not write to {image2_output}.')