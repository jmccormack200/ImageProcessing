import Image
import numpy as np

class ImageProcessing:

    def __init__(self, imagepath):
        self.image = Image.open(imagepath).convert("LA")
        (self.width, self.height) = self.image.size 
        
    def outputImageAs(self, filename):
        self.image.convert("RGB").save(filename + ".bmp")
        
    def linearSmoothingFilter(self, weighted=False):
        if weighted:
            print self.width
        else:
            self.__iterator()
    
    def __iterator(self, filtergrid=False):
        filtergrid = [[1,1,1][1,1,1][1,1,1]]
        new_image = self.image
        pix = new_image.load()
        for x in range(self.width):
            for y in range(self.height):
                pix[x,y][0] = pix[x,y][0] * filtergrid[1][1]
                if (y+1 < self.height):
                    pix[x,y+1][0] = pix[x,y+1][0] * filtergrid[1][1]
                if (y-1 >= 0):
                    pix[x,y-1][0] = pix[x,y-1][0] * filtergrid[1][1]
                if (x+1 < self.width):
                    pix[x+1,y][0] = pix[x+1,y][0] * filtergrid[1][1]
                    if (y+1 < self.height):
                        pix[x+1,y+1][0] = pix[x+1,y+1][0] * filtergrid[1][1]
                    if (y-1 >= 0):
                        pix[x+1,y-1][0] = pix[x+1,y-1][0] * filtergrid[1][1]
                if (x-1 >= 0):
                    pix[x-1,y][0] = pix[x-1,y][0] * filtergrid[1][1]
                    if (y+1 < self.height):
                        pix[x-1,y+1][0] = pix[x-1,y+1][0] * filtergrid[1][1]
                    if (y-1 >= 0):
                        pix[x-1,y-1][0] = pix[x-1,y-1][0] * filtergrid[1][1]
                
                
                
        self.image.convert("RGB").save("whoop.bmp")
        

        
        
        
        
        
        
        
        
if __name__ == "__main__":
    imageprocessing = ImageProcessing("Boston_Normal.bmp")
    imageprocessing.outputImageAs("Test")
    imageprocessing.linearSmoothingFilter()
