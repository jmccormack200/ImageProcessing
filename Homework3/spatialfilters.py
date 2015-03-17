import Image
import numpy as np
from math import exp, pi


class ImageProcessing:

    def __init__(self, imagepath):
        self.image = Image.open(imagepath).convert("LA")
        (self.width, self.height) = self.image.size 
        
    def outputImageAs(self, filename):
        self.image.convert("RGB").save(filename + ".bmp")
        
    def linearSmoothingFilter(self, weighted=False):
        if weighted:
            filtergrid = [[1,2,1],[2,4,2],[1,2,1]]
            constant = 16
            name = "weightedSmoothing"
            self.__iterator(filtergrid, constant, name)
        else:
            filtergrid = [[1,1,1],[1,1,1],[1,1,1]]
            constant = 9
            name = "linearSmoothing"
            self.__iterator(filtergrid, constant, name)
    
    def gaussianFilter(self, variance):
        constant = 1
        exponential = exp(-1.0/(2 * variance))
        edge = constant * exponential
        corner = edge * exponential
        constant += edge * 4 + corner * 4
        
        filtergrid = [[corner, edge, corner],[edge, constant, edge],
                [corner, edge, corner]]
        name = "gaussian"
        self.__iterator(filtergrid, constant, name)
        
    def laplacianFilter(self, laplacian=True):
        if laplacian:
            filtergrid = [[0,1,0],[1,-4,1],[0,1,0]]
            constant = 1
            name = "laplacian"
            self.__iterator(filtergrid, constant, name)
        else: 
            #otherwise isotropic
            filtergrid = [[1,1,1],[1,-8,1],[1,1,1]]
            constant = 1
            name = "isotropic"
            self.__iterator(filtergrid, constant, name)
        
    
    
    def medianFilter(self, name="median"):
        new_image = self.image
        pix = new_image.load()
        for x in range(self.width):
            for y in range(self.height):
                middle_value = []
                middle_value.append(pix[x,y][0])
                if (y+1 < self.height):
                    middle_value.append(pix[x,y+1][0])
                if (y-1 >= 0):
                    middle_value.append(pix[x,y-1][0])
                if (x+1 < self.width):
                    middle_value.append(pix[x+1,y][0])
                    if (y+1 < self.height):
                        middle_value.append(pix[x+1,y+1][0])
                    if (y-1 >= 0):
                        middle_value.append(pix[x+1,y-1][0])
                if (x-1 >= 0):
                    middle_value.append(pix[x-1,y][0])
                    if (y+1 < self.height):
                        middle_value.append(pix[x-1,y+1][0])
                    if (y-1 >= 0):
                        middle_value.append(pix[x-1,y-1][0])
                pix[x,y] = int(np.median(np.array(middle_value)))
        
        self.image.convert("RGB").save(name + ".bmp")
    
    def __iterator(self, filtergrid, constant, name):
        new_image = self.image.copy()
        old_pix = self.image.load()
        new_pix = new_image.load()
        middle_value = 0
        for x in range(self.width):
            for y in range(self.height):
                if (y+1 >= self.height or y-1 < 0 or x+1 >= self.width or x-2 <= self.height):
                    pass
                else:
                    middle_value += old_pix[x,y][0] * filtergrid[1][1]
                    middle_value += old_pix[x,y+1][0] * filtergrid[1][2]
                    middle_value += old_pix[x,y-1][0] * filtergrid[1][0]
                    middle_value += old_pix[x+1,y][0] * filtergrid[2][1]
                    middle_value += old_pix[x+1,y+1][0] * filtergrid[2][2]
                    middle_value += old_pix[x+1,y-1][0] * filtergrid[2][0]
                    middle_value += old_pix[x-1,y][0] * filtergrid[0][1]
                    middle_value += old_pix[x-1,y+1][0] * filtergrid[0][2]
                    middle_value += old_pix[x-1,y-1][0] * filtergrid[0][0]
                new_pix[x,y] = (int(middle_value / constant))            
                
        new_image.convert("RGB").save(name + ".bmp")
    """
        new_image = self.image.copy()
        old_pix = self.image.load()
        new_pix = new_image.load()
        middle_value = 0
        for x in range(self.width):
            for y in range(self.height):
                middle_value += old_pix[x,y][0] * filtergrid[1][1]
                if (y+1 < self.height):
                    middle_value += old_pix[x,y+1][0] * filtergrid[1][2]
                if (y-1 >= 0):
                    middle_value += old_pix[x,y-1][0] * filtergrid[1][0]
                if (x+1 < self.width):
                    middle_value += old_pix[x+1,y][0] * filtergrid[2][1]
                    if (y+1 < self.height):
                        middle_value += old_pix[x+1,y+1][0] * filtergrid[2][2]
                    if (y-1 >= 0):
                        middle_value += old_pix[x+1,y-1][0] * filtergrid[2][0]
                if (x-1 >= 0):
                    middle_value += old_pix[x-1,y][0] * filtergrid[0][1]
                    if (y+1 < self.height):
                        middle_value += old_pix[x-1,y+1][0] * filtergrid[0][2]
                    if (y-1 >= 0):
                        middle_value += old_pix[x-1,y-1][0] * filtergrid[0][0]
                new_pix[x,y] = (int(middle_value / constant))
    """


        
if __name__ == "__main__":
    imageprocessing = ImageProcessing("shapes.jpg")
    #imageprocessing.outputImageAs("Test")
    #imageprocessing.linearSmoothingFilter()
    imageprocessing.linearSmoothingFilter(weighted=True)
    #imageprocessing.gaussianFilter(0.5)
    #imageprocessing.medianFilter()
    #imageprocessing.laplacianFilter()
    #imageprocessing.laplacianFilter(False)