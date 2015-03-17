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
        padded_array.append([0]*(self.width + 4))
        padded_array.append([0]*(self.width + 4))
        for y in range(self.height):
            row = []
            for x in range(self.width + 4):
                if ((x <= 1) or (x - 2 >= self.width)):
                    row.append(0)
                else:
                    row.append(pix[x-2,y])
            padded_array.append(row)
        padded_array.append([0]*(self.width + 4))
        padded_array.append([0]*(self.width + 4))
        im = Image.fromarray(np.uint8(padded_array))
        self.image = im
        (self.width, self.height) = self.image.size
        
        
    def outputImageAs(self, filename):
        
        self.image.save(filename + ".bmp")
        
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
            filtergrid = [[0,-1,0],[-1,4,-1],[0,-1,0]]
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
        
        new_image.convert("RGB").save(name + ".bmp")
    
    def __iterator(self, filtergrid, constant, name):
        new_image = self.image.copy()
        #pix = self.image.load()
        #pix = new_image.load()
        pix = np.asarray(new_image)
        filtered = np.empty([self.height, self.width])
        print self.width
        print self.height
        for x in range(2, self.width-2):
            for y in range(2, self.height-2):
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
                #if middle_value < 0:
                #   middle_value *= -1
                filtered[y][x] = (int(middle_value / constant))
        filtered_im = Image.fromarray(filtered)
        filtered_im.convert('RGB').save(name + ".jpg")



        
if __name__ == "__main__":
    #imageprocessing = ImageProcessing("shapes.jpg")
    #imageprocessing = ImageProcessing("Boston_Normal.bmp")
    imageprocessing = ImageProcessing("wdg4.gif")
    #imageprocessing.outputImageAs("Test")
    imageprocessing.linearSmoothingFilter()
    #imageprocessing.linearSmoothingFilter(weighted=True)
    #imageprocessing.gaussianFilter(0.5)
    #imageprocessing.medianFilter()
    #imageprocessing.laplacianFilter()
    #imageprocessing.laplacianFilter(False)