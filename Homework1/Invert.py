import Image

def inverse_image():
    #Open Image 
    img = Image.open("brady.jpg")
    #Load pixel information
    pix = img.load()
    #Find the width and height of the image
    (width, height) = img.size
    #Iterate over the width and the height
    for x in range(width):
        for y in range(height):
            #Replace each pixel with the number referenced from 255 instead of 0
            r,g,b = pix[x,y]
            pix[x,y] = (255 - r, 255 - g, 255- b)
    #Save Input
    img.save("brady_inv.png")

if __name__ == "__main__":
    inverse_image()
