import cv2
import numpy as np
from scipy import ndimage
import time
import matplotlib.pyplot as plt
from keras.models import load_model
from google.colab.patches import cv2_imshow


def masking(img, lower_hsv, upper_hsv, red=0):
    # histogram equalisation
    temp = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    # equalize the histogram of the Y channel
    temp[:, :, 0] = cv2.equalizeHist(temp[:, :, 0])
    # convert the YUV image back to RGB format
    img = cv2.cvtColor(temp, cv2.COLOR_YUV2BGR)

    # creating mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
		
		# if we need to detect red we need to submerge two different masks
		# it is because hue values of red
    if red == 1:
        lower_red_l = np.array([0, 60, 20])
        upper_red_l = np.array([15, 255, 255])
        mask_l = cv2.inRange(hsv, lower_red_l, upper_red_l)
        mask = mask + mask_l
        print("red")

		#initialising mask
    bitw = cv2.bitwise_and(mask, mask, mask=mask)

    # applying opening operation
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(bitw, cv2.MORPH_OPEN, kernel)

    # removing parasites
    mask_f = ndimage.median_filter(opening, size=5)

    return mask_f

def load_data(dir,datasetname):
    npzfile = np.load(dir + datasetname + "_training_data.npz")
    train = npzfile["arr_0"]
    
    npzfile = np.load(dir + datasetname + "_training_labels.npz")
    train_labels = npzfile["arr_0"]
    
    npzfile = np.load(dir + datasetname + "_test_data.npz")
    test = npzfile["arr_0"]
    
    npzfile = np.load(dir + datasetname + "_test_labels.npz")
    test_labels = npzfile["arr_0"]
    
    return (train,train_labels), (test, test_labels)



def data_prep(dir, datasetname):
    
    (train,train_labels), (test, test_labels) =  load_data(dir, datasetname)
    
    img_rows = train[0].shape[0]
    img_cols = train[1].shape[0]
    
    train = train.reshape(train.shape[0], img_rows, img_cols, 1)
    test = test.reshape(test.shape[0], img_rows, img_cols, 1)

    train_labels = train_labels.reshape(train_labels.shape[0],1)
    test_labels = test_labels.reshape(test_labels.shape[0],1)
    
    train = train.astype("float32")
    test = test.astype("float32")
    
    train /=255
    test/=255

    print(train.shape)
    print(train_labels.shape)
    print(test.shape)
    print(test_labels.shape)

    return (train,train_labels), (test, test_labels)

def bounding_box(mask,img,dim):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
				# to find closest desired object we need to sort our object array
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        while cv2.contourArea(sorted_contours[0]) > 150:
            try:
                # finding minimum enclosing circle and bounding box
                x, y, w, h = cv2.boundingRect(sorted_contours[0])
                obj_area = cv2.contourArea(sorted_contours[0])
                start = (x-30,y-50)
                end = (x+w+30,y+h+30)
                #finding radius
                radius = w / 2
                if radius < h / 2:
                    radius = h / 2

                circle_area = 3.14 * (radius ** 2)
                sf = round(obj_area / circle_area,3)

         									
					# getting center coordinates
                gX = int(x + (w / 2))
                gY = int(y + (h / 2))

					# sf filter can be usable to detect roundess of an object
					# but it wont be useful with low res. images
                # sf_check = sf > 0.4 and sf < 1.5
                
                isVertical = w/h < 1.2
                
                if isVertical == True:
                    input_im = img[start[1]:end[1],start[0]:end[0]]
                    input_im = cv2.cvtColor(input_im,cv2.COLOR_BGR2GRAY)
                    input_im = cv2.resize(input_im, dim, interpolation=cv2.INTER_AREA) 
                    print(input_im.shape)
                    cv2_imshow(input_im)
                    input_im=input_im.reshape(1,dim[0],dim[0],1)
                    predict_im=classifier.predict(input_im)   
                    print(str(predict_im))
                    if predict_im < 0.4:
                        print("object found")
                        print("object area= {}".format(obj_area))
                        print("radius= {}".format(radius))
                        print("circle area = {}".format(circle_area))
                        print("sf value = {}".format(sf))
                        # cv2.putText(img, "area: " + str(obj_area), (gX,gY), font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
                        # cv2.putText(img, "sf value: " + str(sf), (gX,gY+15), font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
                        return [start, end, w, h, int(radius * 2), gX, gY, sorted_contours]
                    else:
                        print("popped")
                        sorted_contours.pop(0)
                else:
						# if first object don't satisfies the conditions 
			  	  # then delete object
                    print("popped")
                    sorted_contours.pop(0)
            except:
                return None

    else:
        print("none")
        return None

font = cv2.FONT_HERSHEY_SIMPLEX

path="/content/"

classifier = load_model('/content/buoy_check.h5')

# these intervals can change over different cameras
# it can be adjustable with analysing few samples
# i also wrote a code to analyse
# !! hue values must be discrete
lower_green = np.array([55, 100, 100])
upper_green = np.array([100, 255, 255])

lower_orange = np.array([0, 103, 170])
upper_orange = np.array([18, 240, 255])

lower_yellow = np.array([18, 74, 230])
upper_yellow = np.array([30, 170, 255])


for i in range(1,7):
    start_time = time.time()
    image_path = path+"{}.jpg".format(i)
    img = cv2.imread(image_path)
    width = img.shape[1]
    height = img.shape[0]


		#cropping the sky from image
    # img = img [int(height/3):height,:] 
    # height = img.shape[0]

    dim = (256,256)
    #img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
		
		#initialise masks
    #mask_green = masking(img, lower_green, upper_green, 0)
    mask_yellow = masking(img, lower_yellow, upper_yellow, 0)
    mask_orange = masking(img, lower_orange, upper_orange, 0)

		#finding objects and it's features
    #buoy_green = bounding_box(mask_green)
    print("*****yellow*****")
    buoy_yellow = bounding_box(mask_yellow,img,dim)
    print("*****orange*****")
    buoy_orange = bounding_box(mask_orange,img,dim)
		
		# when sun reflects over an buoy, some area on orange buoy can be detected
		# as yellow. So i added a filter that checks if circle of orange buoy includes 
		# yellow buoy 
   
    if buoy_orange == None or buoy_yellow == None:
        pass
    else:
        distance = ((buoy_yellow[5]-buoy_orange[5])**2 + (buoy_yellow[6]-buoy_orange[6])**2)**(1/2)
        radius = [int(buoy_yellow[4]/2),0]
        if int(radius[0]) < int(buoy_orange[4]/2):
            radius = [int(buoy_orange[4] / 2),1]

        if distance < radius[0]:
            if radius[1] == 0:
                buoy_orange = None
            else:
                buoy_yellow = None
                

            
    # try:
    #     cv2.drawContours(img, buoy_green[7], -1, (0, 255, 0), 1)
    #     cv2.circle(img, (buoy_green[5],buoy_green[6]), int(buoy_green[4]/2), (0, 255, 0), 1)

    # except:
    #     pass

    try:
        cv2.drawContours(img, buoy_yellow[7], -1, (0, 150, 150), 2) 
        # cv2.circle(img, (buoy_yellow[5],buoy_yellow[6]), int(buoy_yellow[4]/2), (0, 0, 0), 2)
        cv2.rectangle(img,buoy_yellow[0],buoy_yellow[1],(0, 0, 0), 2)
        
    except:
        pass

    try:
        cv2.drawContours(img, buoy_orange[7], -1, (0, 0, 255), 2)
        # cv2.circle(img, (buoy_orange[5], buoy_orange[6]), int(buoy_orange[4] / 2), (0, 0, 0), 2)
        cv2.rectangle(img,buoy_orange[0],buoy_orange[1],(0, 0, 0), 2)

    except:
        pass

    cv2.putText(img, "image: " + str(i), (dim[0]-120, 25), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2_imshow(img)
    print("--- %s seconds ---" % (time.time() - start_time))

    cv2.waitKey(0)


cv2.destroyAllWindows()