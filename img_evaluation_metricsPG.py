# -*- coding: utf-8 -*-
"""
Created on Mon Nov 5 13:04:16 2018

Author:
    Prasanth "Prash" Ganesan <prasganesan.pg@gmail.com>

Description:
    This program was originally created to calculate the evaluation 
    statistics of deblurred images. However, this program can be used 
    to evaluate any image with another image.
    
Inputs:
    input_dir = path of the directory where the blur image files are present
    out_dir = path of directory where the output deblurred images have to be saved
    GT_dir = path of directory where ground truth sharp images are present
    
Outputs:
    One output is a text file containing the evaluation metrics. Another output 
    is image files showing the local difference map between images of interest

Literature used:
    [1] https://github.com/RaphaelMeudec/deblur-gan
-------------------------------------------------------------------------------
"""

# Program starts here
from PIL import Image
import time
import os
import matplotlib.cm as cm
import numpy as np
import math
from skimage.measure import compare_ssim as ssim
from matplotlib import pyplot as plt
import pickle

# Secondary Functions
def load_imgRGB(img_path):
    img = Image.open(img_path)
    return img

def save_image(img, path):
    img.save(path)

def is_an_image(filename):
    img_Ext = ['.png', '.jpg', '.jpeg']
    for ext in img_Ext:
        if ext in filename:
            return True
    return False

def list_img_files(directory):
    files = sorted(os.listdir(directory))
    return [os.path.join(directory, f) for f in files if is_an_image(f)]

def PSNR(img1, img2):
	mse = np.mean( (img1/255. - img2/255.) ** 2 )
	if mse == 0:
		return 100
	pix_max = 1
	return 20 * math.log10(pix_max / math.sqrt(mse))

def computeMetrics(input_dir,out_dir,GT_dir):
    listimgs = list_img_files(input_dir)
    if not GT_dir:
        gt_flag=0
    else:
        gt_flag=1
    
    if gt_flag==1:
        comparison_dir_GT = os.path.join(out_dir,'Compare_with_GTImg')
        if not os.path.exists(comparison_dir_GT):
            os.makedirs(comparison_dir_GT)
    comparison_dir_Blur = os.path.join(out_dir,'Compare_with_InputBlurImg')
    if not os.path.exists(comparison_dir_Blur):
        os.makedirs(comparison_dir_Blur)
    
    count=0
    for img_path in listimgs:
        base = os.path.basename(img_path)
        filename = os.path.splitext(base)[0]
        fileext = os.path.splitext(base)[1]
        
        current_img = load_imageRGB(img_path)
        root_filename = filename[:-7]
        if filename[-6:] == 'fake_B':
            fake_img = current_img
            blur_img = load_imgRGB(os.path.join(input_dir,root_filename+"_real_A"+fileext))
            if gt_flag==1:
                gt_img = load_imgRGB(os.path.join(GT_dir,root_filename+fileext))
        else:
            continue
        
        # Comparison with blurred image
        ss_blur,ss_blur_map = ssim(np.array(fake_img),np.array(blur_img),gradient=False, 
                           dynamic_range=None, multichannel=True, gaussian_weights=True, 
                           full=True, use_sample_covariance=False, sigma=1.5)
        
        ss_blur_map_image = np.uint8(ss_blur_map*255)
        ss_blur_map_image = Image.fromarray(ss_blur_map_image,mode='RGB')
        
        # Debug
        #plt.imshow(ss_blur_map_image,interpolation='bilinear')
        #plt.show()
        ps_blur = PSNR(np.array(fake_img),np.array(blur_img))
        
        # Comparison with ground truth
        if gt_flag==1:
            ss_gt,ss_gt_map = ssim(np.array(fake_img),np.array(gt_img),gradient=False, 
                               dynamic_range=None, multichannel=True, gaussian_weights=True, 
                               full=True, use_sample_covariance=False, sigma=1.5)
            ss_gt_map_image = np.uint8(ss_blur_map*255)
            ss_gt_map_image = Image.fromarray(ss_gt_map_image,mode='RGB')
            ps_gt = PSNR(np.array(fake_img),np.array(gt_img))
        
        # File writing operations
        with open(os.path.join(out_dir,'Evaluation_log.txt'), 'a') as f:
            f.write('{} {} {}\n'.format(root_filename+fileext, "I/O_SSIM = "+str(ss_blur), "I/O_PSNR = "+str(ps_blur)))
            if gt_flag==1:
                f.write('{} {} {}\n'.format(root_filename+fileext, "GT/O_SSIM = "+str(ss_gt), "GT/O_PSNR = "+str(ps_gt)))
        
        new_name = os.path.join(comparison_dir_Blur,root_filename+'_IO'+fileext)
        save_image(ss_blur_map_image, new_name)
        if gt_flag==1:
            new_name = os.path.join(comparison_dir_GT,root_filename+'_GTO'+fileext)
            save_image(ss_gt_map_image, new_name)
        print(os.path.basename(img_path)+" Done")
        with open(os.path.join(out_dir,'Evaluation_log.txt'), 'a') as f:
            f.write('\n')
        
#        # To Debug
#        count+=1
#        if count==10:
#            break

# Main function
if __name__ == "__main__":
    start_time = time.time()
    input_dir = 'Z:/<path goes in here>'
    out_dir = 'Z:/<path goes in here>'
    GT_dir = []
    computeMetrics(input_dir,out_dir,GT_dir)
    print("Evaluation complete")
    end_time = time.time()
    print("--- %s minutes ---" % ((end_time - start_time)/60))

#-----------------------------------------------------------------------
