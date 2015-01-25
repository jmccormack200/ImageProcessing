import Image

img = Image.open("ship.png")
pix = img.load()
(width, height) = img.size
for x in range(width):
	for y in range(height):
		r,g,b = pix[x,y]
		pix[x,y] = (255 - r, 255 - g, 255- b)
img.save("ship2.png")