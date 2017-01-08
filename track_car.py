import cv2

#given information: the first car location
img = cv2.imread('00000001.jpg',0)
car=img[166:193, 6:49]#given initial position of the car
cv2.imwrite('car.jpg',car)

scale=2 #scaling factor in # of pixels
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

#GIVEN: size_change AND occlusion
occlusion=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
size_change=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1]
count=0
for i in range (2,253):
	#open next frame
	if i<10:
		nextFrame='0000000'+`i`+'.jpg'
	elif(i>=10 and i<=99):
		nextFrame='000000'+`i`+'.jpg'
	else:
		nextFrame='00000'+`i`+'.jpg'
	img = cv2.imread(nextFrame,0)
	
	#check for occlusion, if occlusion true, do not update template
	if occlusion[i-1] == 0:
		template=car
		
	print(nextFrame)
	#check if size change, if yes, rescale template
	#before matching
	if size_change[i-1]==1:
		count=count+1
	#if two frames changed size, resize template
	if (size_change[i-1]==1 and count == 2):
		template = cv2.resize(template,(scale+w, scale+h), interpolation = cv2.INTER_LINEAR)
		count=0
	w, h = template.shape[::-1]
	#template/patch matching
	for meth in methods:
		#use matchTemplate
		method = eval(meth)
		res = cv2.matchTemplate(img,template,method)
		
		#get min,max
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		
		#get top left coordinate
		if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
			top_left = min_loc
		else:
			top_left = max_loc
			
		#get bottom right coordinate
		bottom_right = (top_left[0] + w, top_left[1] + h)
		
		#store coordinate
		#topLeft[0]=x1 bottomRight[0]=x2
		#topLeft[1]=y1 bottomRight[1]=y2
		
		#set new template
		car=img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
		cv2.imwrite('car'+`i`+'.jpg',car)
		
		#print coordinate to text file
		with open('vehicle_location.txt', 'a') as text_file:
			text_file.write('\n'+`i`+ '         ' + `top_left[0]`+'           '+ `top_left[1]`+ '          ' + `bottom_right[0]` + '          ' + `bottom_right[1]`)
			break
