import argparse
import os
import sys

import cv2 as cv
import numpy as np
from functools import reduce
import operator
import math

#################### Functions #####################

points = []
def on_click(event, x, y, flags, params):
    if (event == cv.EVENT_LBUTTONDOWN and len(points) < 4):
        coordinate = [x, y]
        points.append(coordinate)
        print(f"Added coordinate ({x}, {y})")
    elif (len(points) == 4):
        print("")
        print("Calculating...")
        cv.destroyAllWindows()

def sort_square_clockwise(points):
    center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), points), [len(points)] * 2))
    return sorted(points, key=lambda points: (135 + math.degrees(math.atan2(*tuple(map(operator.sub, points, center))[::-1]))) % 360)


#################### Preparation ####################

# Parsing variables
parser = argparse.ArgumentParser()
parser.add_argument(
    'filename',
    help='Image filename used for conversion and saving.',
    type=str
)
args = parser.parse_args()

# Save image path in variable
image_name = f'images/{args.filename}'

# Check if given path exists
if not os.path.exists(image_name):
    print('Image does not exist.')
    sys.exit(1)

# Read RGB image
image_original = cv.imread(image_name, cv.IMREAD_COLOR)
rows, cols = image_original.shape[:2]

#################### Exercice 9 ####################

# Show image
cv.imshow('original', image_original)
cv.setMouseCallback("original", on_click)
cv.waitKey(0)

# Original corner & clicked corners
sorted_points = sort_square_clockwise(points)
sorted_points[2], sorted_points[3] = sorted_points[3], sorted_points[2]

width_top = (sorted_points[1][0] - sorted_points[0][0]) / 2
width_bottom = (sorted_points[3][0] - sorted_points[2][0]) / 2

sorted_points[0][0] -= width_top 
sorted_points[1][0] += width_top - 5
sorted_points[2][0] -= width_bottom
sorted_points[3][0] += width_bottom

sorted_points[0][1] -= 30
sorted_points[1][1] -= 30
sorted_points[2][1] += 10
sorted_points[3][1] += 10

pts1 = np.float32(sorted_points)
pts2 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])

# Warp
size = (sorted_points[3][0] - sorted_points[2][0], sorted_points[2][1] - sorted_points[0][1])
matrix = cv.getPerspectiveTransform(pts1, pts2)
image_warp = cv.warpPerspective(image_original, matrix, (cols, rows))

# Show
cv.imshow("warp", image_warp)
cv.waitKey(0)
cv.destroyAllWindows()

#################### Save ####################

# Create 'output' folder if not exists
print('Writing output files...')

output_directory = "result/"
if not os.path.isdir(output_directory):
    print('Output folder does not exist, creating it...')
    os.makedirs(output_directory)

# Save
warp_output = f'result/warp_{args.filename}'
success = cv.imwrite(warp_output, image_warp)
if not success:
    print(f'Could not write to {warp_output}.')