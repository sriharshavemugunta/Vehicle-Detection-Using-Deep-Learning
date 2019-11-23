import pickle
import math
import cv2
import numpy as np
import string
import os
import shutil
import sys
import copy

unique_list         = 'Objects_All.pickle'

raw_image_root      = 'Organized_Raw_Files'

output_image_root   = 'DetectionPatches_256x256'

# How large should each example patch be
patch_size          = 256

# striding step for extract patches from the large orignal image
step_size           = 128

# Should we also extract negative examples (no you shouldn't)
cars_only           = True

# How many pixels in size is the typical car?
car_size            = 32

#========================================================================================================================

class CarProp:
    def __init__(self,phase,type,loc_1,loc_2,obj_class):
        self.phase      = phase
        self.type       = type
        self.loc_1      = loc_1
        self.loc_2      = loc_2
        self.obj_class  = obj_class

#========================================================================================================================

assert(patch_size%step_size==0)
part_steps          = patch_size / step_size

# patch required is the required image for rotation. We force it to be even
# We use this to get our initial crop from the large raw scene. It's over sized so we can
# then crop out the rotated patch without running out of bounds. 
patch_required      = int( round( math.sqrt(patch_size*patch_size + patch_size*patch_size)/2.0 ) )*2
#count = 0 

if patch_required%2 != 0:
    patch_required = patch_required + 1
    
print ("Loading: " + unique_list)

in_file             = open(unique_list)

item_list           = pickle.load(in_file)

if not os.path.isdir(output_image_root):
    os.mkdir(output_image_root)

for file_dir in sorted(item_list):
    
    print ("Processing Dir:\t" + file_dir)
    
    set_raw_root            = raw_image_root    + '/' + file_dir
    set_output_root         = output_image_root + '/' + file_dir
    
    if not os.path.isdir(set_output_root):
        os.mkdir(set_output_root)
            

    for file_root in sorted(item_list[file_dir]):        

        raw_file = set_raw_root + '/' + file_root + '.png'
        
        pstring =  "\tReading Raw File:\t" + raw_file + " ... "
        
        sys.stdout.write(pstring)
        sys.stdout.flush()
        
        raw_image = cv2.imread(raw_file)
        
        print ("Image Size: ")
        print (raw_image.shape)
        
        print ("Done")
        
        print ("Processing:")
        
        counter = 0
        
        steps_x = int(int(raw_image.shape[1])/int(step_size))
        steps_y = int(int(raw_image.shape[0])/int(step_size))
        
        step_locs = []
        
        for y in range(steps_y + 1):
            ts = []
            for x in range(steps_x + 1):
                ts.append([])

            step_locs.append(ts)


        for locs in sorted(item_list[file_dir][file_root]):
            
            loc_1 = int(locs.loc_1)
            loc_2 = int(locs.loc_2)

            step_loc_1 = int(loc_1)/int(step_size)
            step_loc_2 = int(loc_2)/int(step_size)

            step_locs[step_loc_2][step_loc_1].append(locs)

        for y in range(steps_y):
            
            y1 = y * step_size
            y2 = y1 + patch_size 
            
            if y2 > raw_image.shape[0]:
                break

            for x in range(steps_x):
                x1 = x * step_size
                x2 = x1 + patch_size             
                
                if x2 > raw_image.shape[1]:
                    break 
                
                bb_name = "{}/{}.{}.{}.txt".format(set_output_root,file_root,x,y)         
                im_name = "{}/{}.{}.{}.jpg".format(set_output_root,file_root,x,y)
                ck_name = "{}/{}.{}.{}.check.jpg".format(set_output_root,file_root,x,y)
                
                img_patch = raw_image[y1:y2,x1:x2,:]

                obj_list = []
                
                for sy in range(part_steps):
                    for sx in range(part_steps):
                        
                        for locs in step_locs[y + sy][x + sx]:                         
                            
                            if locs.obj_class != 0:
                                obj_list.append(locs)

                if len(obj_list) > 0:                
                    cv2.imwrite(im_name, img_patch, [int(cv2.IMWRITE_JPEG_QUALITY), 95])                
                    
                    bb_file = open(bb_name,'w')                
                    
                    img_patch_cp = copy.deepcopy(img_patch)
                    
                    # in case we want to do something else, we keep the obj_list list
                    for l in obj_list:
                        x_loc   = float(int(l.loc_1) - x1)/float(patch_size)
                        y_loc   = float(int(l.loc_2) - y1)/float(patch_size)
                        h       = float(car_size)/float(patch_size)
                        w       = float(car_size)/float(patch_size)
                        
                        if cars_only:
                            if l.obj_class != 0:        
                                bb_file.write("{} {} {} {} {}\n".format(l.obj_class,x_loc,y_loc,h,w))
                        else:
                            bb_file.write("{} {} {} {} {}\n".format(l.obj_class,x_loc,y_loc,h,w))
                
                        if l.obj_class == 0:
                            col = (255,255,255)
                        elif l.obj_class == 1:
                            col = (0,0,255)   
                        elif l.obj_class == 2:
                            col = (0,255,0)      
                        elif l.obj_class == 3:
                            col = (255,0,0)   
                        elif l.obj_class == 4:
                            col = (0,0,0)  
                                 
                        img_patch_cp = cv2.rectangle(img_patch_cp,
                                                     (int(l.loc_1)- x1+(car_size/2),int(l.loc_2)- y1+(car_size/2)),
                                                     (int(l.loc_1)- x1-(car_size/2),int(l.loc_2)- y1-(car_size/2)),
                                                     col)
                        
                    cv2.imwrite(ck_name, img_patch_cp) 
            
                if counter > 0:
                    if counter%100 == 0:
                        sys.stdout.write('.')
                        sys.stdout.flush()
                    if counter%5000 == 0:
                        sys.stdout.write('\n')
                        sys.stdout.flush()
                counter += 1
            
        print ('x')