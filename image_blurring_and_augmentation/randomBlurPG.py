# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 15:18:51 2018

Author:
    Prasanth "Prash" Ganesan <prasganesan.pg@gmail.com>

Description:
    This program creates a blurry version of an input image. The type of blur
    is chosen randomly between Gaussian and average blur. The radius of the 
    blur is also random but the range is hardcoded and can be changed in the 
    program if the user wants to.
    
Inputs:
    input_dir = path of the directory where the image files are present
    out_dir = path of directory where the output images have to be saved
    
Outputs:
    The blurred images are automatically saved in the destination folder along 
    with a log file which mentions the random blur type and the blur radius 
    applied to each image file.
    
Literature used:
    [1] https://github.com/RaphaelMeudec/deblur-gan
-------------------------------------------------------------------------------
"""

# Program starts here
from PIL import ImageFilter, Image
import os
import random
import matplotlib.pyplot as plt

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

def randomBlurPG(img_path,out_dir,random_radius):
    sharpimg = load_imgRGB(img_path)
    if bool(random.randint(0,1)):
        blurredimg = sharpimg.filter(ImageFilter.BoxBlur(radius=random_radius))
        #print(+" boxblur "+str(random_radius))
        with open(out_dir+'log.txt', 'a') as f:
            f.write('{} {} {}\n'.format(os.path.basename(img_path), "BoxBlurRadius =", random_radius))
    else:
        blurredimg = sharpimg.filter(ImageFilter.GaussianBlur(radius=random_radius))
        #print(os.path.basename(img_path)+" gausblur "+str(random_radius))
        with open(out_dir+'log.txt', 'a') as f:
            f.write('{} {} {}\n'.format(os.path.basename(img_path), "GaussianBlurRadius =", random_radius))
    return sharpimg,blurredimg

def save_image(img, path):
    img.save(path)

def createBlurBatchPG(input_dir,out_dir):
    listimgs = list_img_files(input_dir)
    min_blur_radius = 2 #Pixel units
    max_blur_radius = 5 #Pixel units
    for img_path in listimgs:
        rand_num = random.sample(range(min_blur_radius, max_blur_radius+1), 1)
        sharpimg,blurredimg = randomBlurPG(img_path,out_dir,rand_num[0])
        out = os.path.join(out_dir,os.path.basename(img_path))
        save_image(blurredimg, out)
        print(os.path.basename(img_path)+" Done")
    
# Main function
if __name__ == "__main__":
    input_dir = 'Z:/<path goes in here>'
    out_dir = 'Z:/<path goes in here>'
    createBlurBatchPG(input_dir,out_dir)
    print("Blurring complete")
#    sharpimg,blurredimg = blurPG(img_path)
#    plt.imshow(sharpimg)
#    plt.show()
#    plt.imshow(blurredimg)
#    plt.show()    

#-----------------------------------------------------------------------
