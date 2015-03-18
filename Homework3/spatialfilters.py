import Image
import numpy as np
from math import exp, pi


class ImageProcessing:

    def __init__(self, imagepath):
        self.image = Image.open(imagepath).convert("L")
        (self.width, self.height) = self.image.size
        #pad image
        self.__pad()
        
        
        
    def __pad(self):
        pix = self.image.load()
        padded_array = []
        padded_array.append([0]*(self.width + 2))
        for y in range(self.height):
            row = []
            for x in range(self.width + 2):
                if ((x <= 0) or (x - 1 >= self.width)):
                    row.append(0)
                else:
                    row.append(pix[x-1,y])
            padded_array.append(row)
        padded_array.append([0]*(self.width + 2))
        im = Image.fromarray(np.uint8(padded_array))
        self.image = im
        (self.width, self.height) = self.image.size
        
        
        
    def linearSmoothingFilter(self, weighted=False):
        if weighted:
            filtergrid = [[1,2,1],[2,4,2],[1,2,1]]
            constant = 16
            name = "weightedSmoothing"
            filtered_im = self.__iterator(filtergrid, constant)
            filtered_im.convert('RGB').save(name + ".jpg")
        else:
            filtergrid = [[1,1,1],[1,1,1],[1,1,1]]
            constant = 9
            name = "linearSmoothing"
            filtered_im = self.__iterator(filtergrid, constant)
            filtered_im.convert('RGB').save(name + ".jpg") 
    
    def gaussianFilter(self, variance):
        center = 1 / (2 * pi * variance)
        exponential = exp(-1.0/(2 * variance))
        edge = center * exponential
        corner = center * exp(-(2)/2  * variance)
        
        filtergrid = [[corner, edge, corner],[edge, center, edge],
                [corner, edge, corner]]
        constant = corner * 4 + edge * 4 + center
        for a in filtergrid:
            print a
        name = "gaussian"
        filtered_im = self.__iterator(filtergrid, constant=constant)
        filtered_im.convert('RGB').save(name + ".jpg") 
        
    def laplacianFilter(self, laplacian=True):
        if laplacian:
            filtergrid = [[0,-1,0],[-1,4,-1],[0,-1,0]]
            name = "laplacian"
            filtered_im = self.__iterator(filtergrid, scale=150)
        else: 
            #otherwise isotropic
            filtergrid = [[1,1,1],[1,-8,1],[1,1,1]]
            name = "isotropic"
            filtered_im = self.__iterator(filtergrid, scale=150)
        filtered_im.convert('RGB').save(name + ".jpg") 
    
    def sobelFilter(self, mode="x"):
        if mode == "y":
            filtergrid = [[-1,0,1],[-2,0,2],[-1,0,1]]
            name = "sobelY"
            filtered_im = self.__iterator(filtergrid)
            filtered_im.convert('RGB').save(name + ".jpg")   
            
        elif mode == "x":
            filtergrid = [[-1,-1,-1],[0,0,0],[1,1,1]]
            name = "sobelX"
            filtered_im = self.__iterator(filtergrid)
            filtered_im.convert('RGB').save(name + ".jpg")
            
        elif mode =="xtheny":
            filtergrid = [[-1,-1,-1],[0,0,0],[1,1,1]]
            name = "sobelXthenY"
            filtered_im = self.__iterator(filtergrid)
            filtered_im.convert('RGB').save(name + ".jpg")
            imageprocessing = ImageProcessing(name + ".jpg")
            imageprocessing.sobelFilter("y")
            
        elif mode =="ythenx":
            filtergrid = [[-1,0,1],[-2,0,2],[-1,0,1]]
            name = "sobelYthenX"
            filtered_im = self.__iterator(filtergrid)
            filtered_im.convert('RGB').save(name + ".jpg")
            imageprocessing = ImageProcessing(name + ".jpg")
            imageprocessing.sobelFilter("x")
            
        
    
    
    def medianFilter(self, name="median"):
        new_image = self.image
        pix = new_image.load()
        filtered = np.empty([self.height, self.width])
        for x in range(self.width):
            for y in range(self.height):
                middle_value = []
                middle_value.append(pix[x,y])
                if (y+1 < self.height):
                    middle_value.append(pix[x,y+1])
                if (y-1 >= 0):
                    middle_value.append(pix[x,y-1])
                if (x+1 < self.width):
                    middle_value.append(pix[x+1,y])
                    if (y+1 < self.height):
                        middle_value.append(pix[x+1,y+1])
                    if (y-1 >= 0):
                        middle_value.append(pix[x+1,y-1])
                if (x-1 >= 0):
                    middle_value.append(pix[x-1,y])
                    if (y+1 < self.height):
                        middle_value.append(pix[x-1,y+1])
                    if (y-1 >= 0):
                        middle_value.append(pix[x-1,y-1])
                filtered[y][x] = int(np.median(np.array(middle_value)))
                
        filtered_im = Image.fromarray(filtered)
        filtered_im.convert('RGB').save(name + ".jpg")
        new_image.convert("RGB").save(name + ".bmp")
    
    def __iterator(self, filtergrid, constant=1, scale=1):
        new_image = self.image.copy()
        #pix = self.image.load()
        #pix = new_image.load()
        pix = np.asarray(new_image)
        filtered = np.empty([self.height, self.width])
        print self.width
        print self.height
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):
                middle_value = 0
                middle_value += pix[y][x] * filtergrid[1][1]
                middle_value += pix[y+1][x] * filtergrid[2][1]
                middle_value += pix[y-1][x] * filtergrid[0][1]
                middle_value += pix[y][x+1] * filtergrid[1][2]
                middle_value += pix[y+1][x+1] * filtergrid[2][2]
                middle_value += pix[y-1][x+1] * filtergrid[0][2]
                middle_value += pix[y][x-1] * filtergrid[1][0]
                middle_value += pix[y+1][x-1] * filtergrid[2][0]
                middle_value += pix[y-1][x-1] * filtergrid[0][0]
                filtered[y][x] = (int(middle_value / constant)) + scale
        return Image.fromarray(filtered)
        



        
if __name__ == "__main__":
    #imageprocessing = ImageProcessing("shapes.jpg")
    imageprocessing = ImageProcessing("Boston_Normal.bmp")
    #imageprocessing = ImageProcessing("wdg4.gif")
    #imageprocessing.outputImageAs("Test")
    #imageprocessing.linearSmoothingFilter()
    #imageprocessing.linearSmoothingFilter(weighted=True)
    imageprocessing.gaussianFilter(0.5)
    #imageprocessing.medianFilter()
    #imageprocessing.laplacianFilter()
    #imageprocessing.laplacianFilter(False)
    #imageprocessing.sobelFilter("x")
    #imageprocessing.sobelFilter("y")
    #imageprocessing.sobelFilter("xtheny")
    #imageprocessing.sobelFilter("ythenx")