import argparse
import os
import sys

import cv2 as cv
import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier

#################### Functions ######################

def create_DoGfilter(scale, orientation):

    gaussian_1D = cv.getGaussianKernel(scale, 1)

    middle = int(np.floor(scale / 2))
    matrix_2D = np.ones((scale, scale))
    matrix_2D[:, middle] = gaussian_1D[:, 0]

    kernel_1D_lower_deviation = cv.getGaussianKernel(scale, 0)
    kernel_1D_lower_deviation = np.transpose(kernel_1D_lower_deviation)

    gaussian_2D = cv.filter2D(matrix_2D, -1, kernel_1D_lower_deviation)

    filter_DoG = cv.Sobel(gaussian_2D, cv.CV_64F, 0, 1, scale)
    #filter_DoG = cv.Sobel(gaussian_2D, cv.CV_64F, 1, 0, scale)

    rotation_matrix = cv.getRotationMatrix2D((middle, middle), orientation, 1)

    rotated_filter_DoG = cv.warpAffine(filter_DoG, rotation_matrix, (scale, scale))

    return rotated_filter_DoG

def get_results(image, classifier):

    ### Read
    image = cv.imread(image_paths[index], cv.IMREAD_GRAYSCALE)
    rows, cols = image.shape[:2]
    blocks = (int(rows / 16), int(cols / 16))

    ### Foreach block
    for x in range(0, blocks[0]):
        for y in range(0, blocks[1]):

            ### Feature vector
            filter_number = 1
            feature_vector = []

            ### Foreach filter
            for scale in scales:
                for orientation in orientations:

                    ### Filter image
                    filter_DoG = create_DoGfilter(scale, orientation)
                    result = cv.filter2D(image, -1, filter_DoG)
                    result = np.absolute(result)

                    ### Max in block
                    crop = result[x * 16 : (x+1) * 16, y * 16 : (y+1) * 16] 
                    maximum = np.max(crop)
                    feature_vector.append(maximum)

            ### Test
            prediction = model.predict([feature_vector])

            ### Change original image to mask
            alpha = 0.3
            if (prediction == 1):
                overlay = image.copy()
                cv.rectangle(overlay, (y*16, x*16), ((y*16)+15, (x*16)+15), (255, 255, 255), -1)
                cv.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
    
    return image

#################### Preparation ####################

# Images
image_paths = ['images/road1.png', 'images/road2.png', 'images/road3.png', 'images/road4.png']
mask_paths = ['images/road1_blocks.png', 'images/road2_blocks.png', 'images/road3_blocks.png', 'images/road4_blocks.png']

#################### Exercice 15 ####################

np.random.seed(0)

scales = [10, 5]
orientations = [15, 30, 60, 90, 180, 220]

# Create data
road_blocks = pd.DataFrame(columns=[f"vector{index}" for index in range(1, 13)])
non_road_blocks = pd.DataFrame(columns=[f"vector{index}" for index in range(1, 13)])

### Foreach image
for index in range(0, len(image_paths)):
    print(f"processing image {index+1}...")

    ### Read
    image = cv.imread(image_paths[index], cv.IMREAD_GRAYSCALE)
    rows, cols = image.shape[:2]
    blocks = (int(rows / 16), int(cols / 16))

    mask = cv.imread(mask_paths[index], cv.IMREAD_GRAYSCALE)

    ### Foreach block
    for x in range(0, blocks[0]):
        for y in range(0, blocks[1]):

            ### Feature vector
            filter_number = 1
            feature_vector = {}

            ### Foreach filter
            for scale in scales:
                for orientation in orientations:

                    ### Filter image
                    filter_DoG = create_DoGfilter(scale, orientation)
                    result = cv.filter2D(image, -1, filter_DoG)
                    result = np.absolute(result)

                    ### Max in block
                    crop = result[x * 16 : (x+1) * 16, y * 16 : (y+1) * 16] 
                    maximum = np.max(crop)
                    feature_vector[f"vector{filter_number}"] = maximum
                    
                    filter_number = filter_number + 1

            ### Determine part of mask
            if (mask[int(x*16)][int(y*16)] == 255):
                feature_vector['road_mark'] = 1
                road_blocks = road_blocks.append(feature_vector, ignore_index=True)
            else:
                feature_vector['road_mark'] = 0
                non_road_blocks = non_road_blocks.append(feature_vector, ignore_index=True)

# Balanced tree
size = road_blocks.shape[0]
road_blocks = road_blocks[:size]
non_road_blocks = non_road_blocks[:size]
dataframe = road_blocks.append(non_road_blocks, ignore_index=True)

# Classifier
model = RandomForestClassifier(n_estimators=10)
model.fit(dataframe[dataframe.columns[:12]], dataframe['road_mark'])

# Output directory
output_directory = "result/"
if not os.path.isdir(output_directory):
    print('Output folder does not exist, creating it...')
    os.makedirs(output_directory)
print("")

# Visualize
for index in range(0, len(image_paths)):
    print(f"predicting image {index+1}...")

    result = get_results(image_paths[index], model)
    cv.imshow("mask", result)
    cv.waitKey(0)
    cv.destroyAllWindows()

    cv.imwrite(f"result/road{index+1}_mask.png", result)

