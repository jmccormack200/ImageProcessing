import Image

img = Image.open("coins.png")
pix = img.load()
(width, height) = img.size
for x in range(width):
	for y in range(height):
		if pix[x,y] >= 100:
			pix[x,y] = 255
		else:
			pix[x,y] = 0




def expandCircle(x,y,pix,width,height,count):
	gray_level = 100
	done = False
	search = []
	
	while(done == False):
		done = True
		if x + 1== width - 1:
			done = True
			break
		if y == height - 1:
			done = True
			break
		
		if pix[x+1,y] == 255:
			pix[x+1,y] = gray_level
			search.append([x+1,y])
			done = False
		if pix[x-1,y] == 255:
			pix[x+1,y] = gray_level
			search.append([x-1,y])
			done = False
		if pix[x,y+1] == 255:
			pix[x,y+1] = gray_level
			search.append([x,y+1])
			done = False
		if pix[x,y-1] == 255:
			pix[x,y-1] = gray_level
			search.append([x,y-1])
			done = False
		next_point = search.pop()
		x = next_point[0]
		y = next_point[1]
	return pix

pix = expandCircle(0,0, pix,width, height,0)
img.save('coins2.png')


		
	