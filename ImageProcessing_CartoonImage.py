#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 18:28:44 2018

@author: digisha
"""

class Cartoon_version:
    
    """ A program to create the cartoon version of a given image """
    
    def __init__(self):
        pass

    def cartoon(self, img):
        #read the image
        img = cv2.imread(img)
        #resize the image
        img = cv2.resize(img, (1400,1400))
        # number of downscaling steps using list container type
        numDownSamples = [1,1,2] 
        # number of bilateral filtering steps (in smaller steps)
        numBilateralFilters = 7  

        Colorimg = img
        
         #downscaling image
        for _ in numDownSamples:
            Colorimg = cv2.pyrDown(Colorimg)
            
            #applying bilateral filters to get the cartoon flavour
        for _ in range(numBilateralFilters):
            Colorimg = cv2.bilateralFilter(Colorimg,
                                            d=9,
                                            sigmaColor=1,
                                            sigmaSpace=7)
        
        for _ in numDownSamples:
            #upscaling image the sam enumber of times it was downscaled
            Colorimg = cv2.pyrUp(Colorimg)
            
        #coverting image to gray scale to blur it, so that colors do not interfere
        img_gray = cv2.cvtColor(Colorimg, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.medianBlur(img_gray, 3)
        
        # GAUSSIAN detect and enhance edges to get the sketch pen effect - using adaptive threshhold technique
        type_threshold=input("Enter the type of adaptive threshold (mean or gaussian):")
        
        #ask user for type of threshold technique for blurring
        if type_threshold == 'mean':
            img_edge = cv2.adaptiveThreshold(img_blur,
                                             255,
                                             cv2.ADAPTIVE_THRESH_MEAN_C,
                                             cv2.THRESH_BINARY,
                                             blockSize=11,
                                             C=2)
        elif type_threshold == 'gaussian':                                 
            img_edge = cv2.adaptiveThreshold(img_blur,
                                             255,
                                             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY,
                                             blockSize=19,
                                             C=2)
        else:
            return None
		#obj.Proxy.img = cv2.cvtColor(th3, cv2.COLOR_GRAY2RGB) 

        (x,y,z) = Colorimg.shape
        img_edge = cv2.resize(img_edge,(y,x))
        
        #convert back to color, to perform bitwise AND of the resultant image with color image
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
        
        return cv2.bitwise_and(Colorimg, img_edge)

#Program starts
        
#initializing user defined class
tmp_canvas = Cartoon_version()

#Import the necessary modules
import cv2
import os
from matplotlib import pyplot as plt
#%matplotlib qt - allow the image to be opened in a new window in jupyter notebook

#open the file using opencv library
file_dir = os.path.join('/Users/digisha/Desktop')
file_name = cv2.imread(os.path.join(file_dir, 'hp.png'))

#check if the file exist
if not os.path.exists('/Users/digisha/Desktop/hp.png'):
    print("File Does Not Exist")
else:
    #call the cartoon function to get the cartoon version of the given image
    cartoon_image = tmp_canvas.cartoon(os.path.join(file_dir, 'hp.png'))
    
    #printing both original and the cartoon version of the image
    plt.subplot(121),plt.imshow(cv2.cvtColor(file_name, cv2.COLOR_BGR2RGB))
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    
    plt.subplot(122),plt.imshow(cv2.cvtColor(cartoon_image, cv2.COLOR_BGR2RGB))
    plt.title('Cartoon version'), plt.xticks([]), plt.yticks([])