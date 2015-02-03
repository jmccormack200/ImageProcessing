import Image


##################################
#
# binarize
#
# This function converts the image into a two
# color image. 
#
# Inputs: pix = the image
#         width = the width of the image
#         height = the height of the image
#
# Output: returns pix, the image, but with the circles
#         filled in. 
#
###################################

def  binarize (pix, width, height):
	for x in range(width):
		for y in range(height):
			if pix[x,y] >= 95:
				pix[x,y] = 255
			else:
				pix[x,y] = 0

	for x in range(width):
		for y in range(height):
			averagePixel(x,y,pix,width,height)
	return pix
    
##################################
#
# expandCircle
#
# Once a circle is identified, this
# function can be used to expand the circle.
# It starts from the point and searches all 
# its neighbours for valid parts of the circle.
# It uses a breadth first search and appends possible
# circle points to a list. 
#
# Inputs: x = x coordinate of pixel
#         y = y coordinate of pixel
#         pix = the image
#         width = the width of the image
#         height = the height of the image
#         count = the number of circles found.
#                 this number is used to increment
#                 the grey scale.
#
# Output: returns pix, the image, but with a circle
#         filled in. 
#
###################################

def expandCircle(x,y,pix,width,height,count):
	gray_level = 10 * count
	done = False
	search = []
	
	while(done == False):
		if x + 1 < width:
			if pix[x+1,y] == 255:
				pix[x+1,y] = gray_level
				search.append([x+1,y])
		if x - 1 >= 0:
			if pix[x-1,y] == 255:
				pix[x-1,y] = gray_level
				search.append([x-1,y])
		if y + 1 < height:
			if pix[x,y+1] == 255:
				pix[x,y+1] = gray_level
				search.append([x,y+1])
		if y - 1 >= 0:
			if pix[x,y-1] == 255:
				pix[x,y-1] = gray_level
				search.append([x,y-1])
		if len(search) != 0:
			next_point = search.pop()
			y = next_point[1]
			x = next_point[0]
		else:
			done = True
	return pix

##################################
#
# findCircle
#
# This function is used to find circles
#
# Inputs: pix = the image
#         width = the width of the image
#         height = the height of the image
#
# Output: returns pix, the image, but with the circles
#         filled in. 
#
###################################

def findCircle(pix, width, height):
#count is used to keep a total for incremnting the grey scale
	count = 1
	for x in range(width):
		for y in range(height):
			if pix[x,y] == 255:
				pix = expandCircle(x,y,pix,width,height,count)
				count += 1
	return pix
		
        
##################################
#
# averagePixel
#
# This function is used to smooth over 
# stray noise areas.
#
# Inputs: x = x coordinate of pixel
#         y = y coordinate of pixel
#         pix = the image
#         width = the width of the image
#         height = the height of the image
#
# Output: returns pix, the image, but with the pixel averaged
#
###################################
def averagePixel(x,y,pix,width,height):
	sum = pix[x,y]
	count = 1
	if x + 1 < width:
		sum += pix[x+1,y]
		count += 1
		if y + 1 < height:
			sum += pix[x+1,y+1]
			count += 1
		if y - 1 >= 0:
			sum += pix[x+1,y-1]
			count += 1
	if x - 1 >= 0:
		sum += pix[x-1,y]
		count += 1
		if y + 1 < height:
			sum += pix[x-1,y+1]
			count += 1
		if y - 1 >= 0:
			sum += pix[x-1, y-1]
			count += 1
	if y + 1 < height:
		sum += pix[x, y+1]
		count += 1
	if y - 1 >= 0:
		sum += pix[x, y-1]
		count +=1
	average = sum / count
	if average >= 125:
		output = 255
	else:
		output = 0
	pix[x,y] = output
	return pix


if __name__ == '__main__':
	img = Image.open("coins.png")
	pix = img.load()
	(width, height) = img.size
	pix = binarize(pix, width, height)
	pix = findCircle(pix, width, height)
	img.save('coins2.png')