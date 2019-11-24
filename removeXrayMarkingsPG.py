# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:00:06 2018

Copyright (c) Prasanth "Prash" Ganesan
Author email: <prasganesan.pg@gmail.com>

Description:
    This program automatically locates the label 'L' in chest x-ray images and 
    removes it. It also creates images showing the detected 'L' bounding box.
    
    If the input image does not have the marking 'L' then it saves the image 
    unaltered.
    
    The program takes some time to finish running if there is a large set of 
    images (~5sec per image), so please be patient. Tip to make it faster: 
    Don't save the bounding box image. You can comment out that part.
    
Inputs:
    input_dir = path of the directory where the image files (3-channel images) 
    are present
    out_dir = path of directory where the output images have to be saved 
    (Caution: If the input and output directories are same, then the original 
    images will get replaced!!)
    
Outputs:
    The output images are automatically saved in the output folder. In addition
    the detected markings are also saved in a separate folder inside the given
    output folder.
    
-------------------------------------------------------------------------------
"""

# Program starts here
from PIL import ImageFilter, Image
import os
import time
import cv2
from scipy.interpolate import griddata
import numpy as np
#import matplotlib.pyplot as plt

# Secondary Functions
def is_an_image(filename):
    image_ext = ['.png', '.jpg', '.jpeg']
    for ext in image_ext:
        if ext in filename:
            return True
    return False

def list_img_files(directory):
    files = os.listdir(directory)
    return [os.path.join(directory, f) for f in files if is_an_image(f)]

def save_image(img, path):
    img.save(path)
    
def findBoundingBoxL(BwImg):
    _, contours, _ = cv2.findContours(BwImg.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE )   
    if not contours:
        return [0,0,0,0]
    countour = contours[-1]
    rect = cv2.boundingRect(countour)
    x,y,w,h = rect
    offset=10
    x=x-offset
    y=y-offset
    w=w+offset*2
    h=h+offset*2   
    BBox = [x,y,w,h]
    return BBox

def interpolateBBox(BBox,orgImg):
    x,y,w,h = BBox
    interpImg = orgImg.copy()
    for slice in range(3):
        search_space = orgImg[y:y+h,x:x+w,slice]
        points = np.where((search_space>0.5)&(search_space<254))
        points=np.transpose(np.asarray(points))
        values = search_space[points[:,0],points[:,1]]
        points[:,[0, 1]] = points[:,[1, 0]]
        grid_x, grid_y = np.meshgrid(np.arange(0,np.shape(search_space)[1]), np.arange(0,np.shape(search_space)[0]))
        interp_slice = griddata(points, values, (grid_x, grid_y), method='linear')
        interpImg[y:y+h,x:x+w,slice] = interp_slice       
    return interpImg
    
def removeMarkingPG(input_dir,out_dir):
    listimgs = list_img_files(input_dir)
    #count=0
    BBox_dir = os.path.join(out_dir,'Detected_markings')
    if not os.path.exists(BBox_dir):
        os.makedirs(BBox_dir)
    
    #del listimgs[0:190] # If you wish to start from the middle then use this (This starts from image 191)
    for img_path in listimgs:
        orgImg = cv2.imread(img_path,-1)
        orgImg_copy = orgImg.copy()
        grayImg = cv2.imread(img_path,0)
        
#        # Debug
#        cv2.imshow('Gray scale image',grayImg)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
        
        BW_threshold = 254
        _,BwImg = cv2.threshold(grayImg, BW_threshold, 255, cv2.THRESH_BINARY)
        
#        # Debug
#        cv2.imshow('Thresholded image',BwImg)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
        
        x,y,w,h = findBoundingBoxL(BwImg)
        if not(x==y==w==h==0): 
            cv2.rectangle(orgImg_copy,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(orgImg_copy,'Marking Detected',(x+w+10,y+h),0,0.5,(0,255,0))
        
        base = os.path.basename(img_path)
        filename = os.path.splitext(base)[0]
        fileext = os.path.splitext(base)[1]
        out_bb = os.path.join(BBox_dir,filename+'_bbox'+fileext)
        bgr_converted = cv2.cvtColor(orgImg_copy, cv2.COLOR_BGR2RGB)
        pil_orgImg_copy = Image.fromarray(bgr_converted)
        save_image(pil_orgImg_copy, out_bb)
        
#        # Debug
#        cv2.imshow("Bounding Box",orgImg_copy)
#        cv2.waitKey()  
#        cv2.destroyAllWindows()
        if not(x==y==w==h==0):
            BBox = [x,y,w,h]
            interpImg = interpolateBBox(BBox,orgImg)
        else:
            interpImg = orgImg
        out_interp = os.path.join(out_dir,base)
        interpImg_bgr_converted = cv2.cvtColor(interpImg, cv2.COLOR_BGR2RGB)
        pil_interpImg = Image.fromarray(interpImg_bgr_converted)
        save_image(pil_interpImg, out_interp)
        
#        # Debug
#        cv2.imshow("Marking removed image",interpImg)
#        cv2.waitKey()  
#        cv2.destroyAllWindows()
#        count+=1
#        if count==10:
#            break
        
        print(os.path.basename(img_path)+" Done")
            
# Main function
if __name__ == "__main__":
    start_time = time.time()
    input_dir = 'Y:/<path>'
    out_dir = 'Y:/<path>'
    removeMarkingPG(input_dir,out_dir)
    print("Marking removal complete")
    end_time = time.time()
    print("--- %s minutes ---" % ((end_time - start_time)/60))

#-----------------------------------------------------------------------
