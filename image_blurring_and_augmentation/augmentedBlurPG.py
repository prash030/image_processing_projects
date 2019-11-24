# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 15:18:51 2018

Copyright (c) Prasanth "Prash" Ganesan
Author Email: <prasganesan.pg@gmail.com>

Description:
    This program creates a augmented images that are blurry version of an input 
    image. The types of blur is hard coded as Gaussian and average blur. The 
    radius of the blur is also hardcoded to be 4 and 8. Hence for each image 
    there are four augmented images created - two with gaussian blur (with blur 
    radius 4 and 8), two with average blur (with blur radius 4 and 8).
    
Inputs:
    input_dir = path of the directory where the image files are present
    out_dir = path of directory where the output images have to be saved
    out_GT_dir = path of directory where the ground truth corresponding to the 
    augmented images are saved.
    
Outputs:
    The augmented images are automatically saved in the destination folder 
    along with a log file which mentions the blur type and the blur 
    radius applied to each image file. The ground truth images are also saved 
    in the respective destination folder. The ground truth and the augmented 
    images form an image pair (so the number of images in these two output 
    folders are the same).
    
Literature used:
    [1] https://github.com/RaphaelMeudec/deblur-gan
-------------------------------------------------------------------------------
"""

# Program starts here
from PIL import ImageFilter, Image
import os
import time
#import matplotlib.pyplot as plt

# Secondary Functions
def load_imgRGB(img_path):
    img = Image.open(img_path)
    return img

def is_an_image(filename):
    img_ext = ['.png', '.jpg', '.jpeg']
    for ext in img_ext:
        if ext in filename:
            return True
    return False

def list_img_files(directory):
    files = os.listdir(directory)
    return [os.path.join(directory, f) for f in files if is_an_image(f)]

def applyBlurPG(img_path,blur_radius,blur_type):
    sharpimg = load_imgRGB(img_path)
    blurredimg=[]
    if blur_type is 'avg':
        blurredimg = sharpimg.filter(ImageFilter.BoxBlur(radius=blur_radius))
    elif blur_type is 'gaus':
        blurredimg = sharpimg.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    else:
        raise ValueError("Unknown blur type. Please check the blur options in applyBlurPG function")
        return 0
    return sharpimg,blurredimg

def save_image(img, path):
    img.save(path)

def createBlurBatchPG(input_dir,out_dir,out_GT_dir):
    listimgs = list_img_files(input_dir)
    min_blur_radius = 4 #Pixel units
    increament_factor = 4 #This is the step size of the blur radius
    blur_types = ['avg', 'gaus']
    augment_size = 2 # This is the number of augmented images per blur type
    for img_path in listimgs:
        count = 1
        for blur in blur_types:
            blur_radius = min_blur_radius
            for aug in range(augment_size):
                #blur_radius = min_blur_radius+aug
                sharpimg,blurredimg = applyBlurPG(img_path,blur_radius,blur)
                base = os.path.basename(img_path)
                filename = os.path.splitext(base)[0]
                fileext = os.path.splitext(base)[1]
                #out = os.path.join(out_dir,filename+'_'+blur+'_'+str(blur_radius)+fileext)
                out = os.path.join(out_dir,filename+'_'+str(count)+fileext)
                save_image(blurredimg, out)
                out_GT = os.path.join(out_GT_dir,filename+'_'+str(count)+fileext)
                save_image(sharpimg, out_GT)
                with open(out_dir+'log.txt', 'a') as f:
                    f.write('{} {} {}\n'.format(filename+'_'+str(count)+fileext, blur+" =", blur_radius))
                blur_radius = blur_radius+increament_factor
                count+=1
        with open(out_dir+'log.txt', 'a') as f:
            f.write('\n')
        """ Uncomment the following line to test for one file"""
        #break
        print(os.path.basename(img_path)+" Done")
        
# Main function
if __name__ == "__main__":
    start_time = time.time()
    input_dir = 'Z:/<path goes in here>'
    out_dir = 'Z:/<path goes in here>'
    out_GT_dir = 'Z:/<path goes in here>'
    createBlurBatchPG(input_dir,out_dir,out_GT_dir)
    print("Blurring complete")
    end_time = time.time()
    print("--- %s minutes ---" % ((end_time - start_time)/60))

#-----------------------------------------------------------------------
