import Image
import numpy as np
from math import exp, pi

###############################
#
# ImageProcessing
#
# Class is instantiated with an image path
# Methods allow for editing of image
#
# instance variables:
# self.width: The width of the image
# self.height: The height of the image
# self.image: The image loaded from the path
#
################################

class ImageProcessing:

###############################
#
# Initialization
# Inputs: imagepath - path to image
# 
# Outputs: Loads self.width, self.height, and
# self.image for use. Runs the private method
# __pad() to pad the image
#
#
################################

    def __init__(self, imagepath):
        self.image = Image.open(imagepath).convert("L")
        (self.width, self.height) = self.image.size
        #pad image
        self.__pad()
        
        
###############################
#
# Method: __pad()
# private method
# 
# This method pads the image for
# should be run before filtering takes
# place
# Inputs: none
# Outputs: the image, padded with 0's
#
#
################################

    def __pad(self):
        pix = self.image.load()
        #Padded array represents the new image
        padded_array = []
        #Add one row of 0's
        padded_array.append([0]*(self.width + 2))
        #Put one 0, then fill with the row information
        #Then put one more 0.
        for y in range(self.height):
            row = []
            for x in range(self.width + 2):
                if ((x <= 0) or (x - 1 >= self.width)):
                    row.append(0)
                else:
                    row.append(pix[x-1,y])
            padded_array.append(row)
        #One final row of 0's
        padded_array.append([0]*(self.width + 2))
        #Convert array back to an image
        im = Image.fromarray(np.uint8(padded_array))
        #Update instance variables.
        self.image = im
        (self.width, self.height) = self.image.size
        
###############################
#
#   Linear Smoothing Filter
# 
#   This method can perform both a weighted
#   and non-weighted linear filter
#
#   inputs: weighted - defaults to false,
#   if true will apply a weighted filter
#
#   outputs: saves the image according to
#   "name" variable.
################################        
        
    def linearSmoothingFilter(self, weighted=False):
        if weighted:
            filtergrid = [[1,2,1],[2,4,2],[1,2,1]]
            constant = 16 #linear filters are divided by sum of cells
            name = "weightedSmoothing"
            #uses the optional variable "constant"
            #with the __iterator method
            filtered_im = self.__iterator(filtergrid, constant)
            filtered_im.convert('RGB').save(name + ".jpg")
        else:
            filtergrid = [[1,1,1],[1,1,1],[1,1,1]]
            constant = 9 #linear filters are divided by sum of cells
            name = "linearSmoothing"
            #uses the optional variable "constant"
            #with the __iterator method
            filtered_im = self.__iterator(filtergrid, constant)
            filtered_im.convert('RGB').save(name + ".jpg") 
###############################
#
#   Gaussian Filter
# 
#   This method can perform both
#   a Gaussian Filter
#
#   inputs: variance - The desired
#   variance of the gaussian distribution
#
#   outputs: saves the image according to
#   "name" variable.
################################    
    def gaussianFilter(self, variance):
        #the value of the center has no exponential
        #component.
        center = 1 / (2 * pi * variance)
        #the exponential is stored separate.
        exponential = exp(-1.0/(2 * variance))
        #The edge and corner require different values
        edge = center * exponential
        corner = center * exp(-(2)/2  * variance)
        
        #stores all according to appropriate value
        #constant holds the sum of all values to be used
        #in the __iterator method.
        filtergrid = [[corner, edge, corner],[edge, center, edge],
                [corner, edge, corner]]
        constant = corner * 4 + edge * 4 + center
        name = "gaussian"
        filtered_im = self.__iterator(filtergrid, constant=constant)
        filtered_im.convert('RGB').save("SPATIALGaussian.jpg") 
###############################
#
#   Laplacian Filter
# 
#   This method can perform both laplacian
#   and isotropic filter.
#
#   inputs: laplacian - Defaults to True
#   to generate the laplacian, can be set
#   to false to generate isotropic. 
#
#   outputs: saves the image according to
#   "name" variable.
################################        
    def laplacianFilter(self, laplacian=True):
        if laplacian:
            filtergrid = [[0,-1,0],[-1,4,-1],[0,-1,0]]
            name = "laplacian"
            #The optional scale feature raises the center value
            #of the output image.
            filtered_im = self.__iterator(filtergrid, scale=150)
        else: 
            #otherwise isotropic
            filtergrid = [[1,1,1],[1,-8,1],[1,1,1]]
            name = "isotropic"
            #The optional scale feature raises the center value
            #of the output image.
            filtered_im = self.__iterator(filtergrid, scale=1)
        filtered_im.convert('RGB').save("SPATIALLaplacian.jpg")

###############################
#
#   Sobel Filter
# 
#   This method performs a soble
#   filter, or 1st derivative
#   filter. 
#
#   inputs: mode - defaults to "x"
#   has 4 different modes, listed inline
#   below. 
#
#   outputs: saves the image according to
#   "name" variable.
################################     
    def sobelFilter(self, mode="x"):
        #selects a Y only sobel filter
        if mode == "y":
            filtergrid = [[-1,0,1],[-2,0,2],[-1,0,1]]
            name = "sobelY"
            filtered_im = self.__iterator(filtergrid)
            filtered_im.convert('RGB').save(name + ".jpg")   
        #selects an x only sobel filter.
        elif mode == "x":
            filtergrid = [[-1,-1,-1],[0,0,0],[1,1,1]]
            name = "sobelX"
            filtered_im = self.__iterator(filtergrid)
            filtered_im.convert('RGB').save(name + ".jpg")
        #selects an x, then a y sobel filter
        #Must run __iterator twice. 
        elif mode =="xtheny":
            filtergrid = [[-1,-1,-1],[0,0,0],[1,1,1]]
            name = "sobelXthenY"
            filtered_im = self.__iterator(filtergrid)
            filtered_im.convert('RGB').save(name + ".jpg")
            imageprocessing = ImageProcessing(name + ".jpg")
            imageprocessing.sobelFilter("y")
        #selects a y, then an x sobel filter
        #Must run __iterator twice.            
        elif mode =="ythenx":
            filtergrid = [[-1,0,1],[-2,0,2],[-1,0,1]]
            name = "sobelYthenX"
            filtered_im = self.__iterator(filtergrid)
            filtered_im.convert('RGB').save(name + ".jpg")
            imageprocessing = ImageProcessing(name + ".jpg")
            imageprocessing.sobelFilter("x")
            
        
###############################
#
#   median filter
# 
#   This method can perform both laplacian
#   and isotropic filter.
#
#   inputs: none
#
#   This is the only function that does not
#   use __iterator, as it needed to save
#   the values differently for analysis.
#
#   outputs: saves the image according to
#   "name" variable.
################################    
  
    def medianFilter(self):
        name = "median"
        new_image = self.image
        pix = new_image.load()
        filtered = np.empty([self.height, self.width])
        for x in range(self.width):
            for y in range(self.height):
                #scans each value in a grid
                #saves to "middle value" array
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
                #median of the array is placed into the image
                filtered[y][x] = int(np.median(np.array(middle_value)))
        #new filtered image is saved.        
        filtered_im = Image.fromarray(filtered)
        filtered_im.convert('RGB').save(name + ".jpg")
###############################
#
#   iterator
#   private method
#   
#   This method applies the filter to
#   the image. 
#
#   inputs: 
#   filtergrid - The filter to be applied
#   constant - defaults to 1 to have no effect.
#       this value is applied to the summation
#       to adjust the value for certain filters.
#   scale - defaults to 1 to have no effect.
#        this value is applied to the summation
#        to adjust the brightness level. 
#
#   outputs: the image which is NOT saved
#   to a file. 
################################    
    def __iterator(self, filtergrid, constant=1, scale=1):
        #copy the image
        new_image = self.image.copy()
        pix = np.asarray(new_image)
        #create an empty array. 
        filtered = np.empty([self.height-2, self.width-2])
        #iterate through, ignoring the padding and starting on the image
        #apply the filter to each spot. 
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
        #if the filter requires a constant or a scale, it is applied here. 
                filtered[y-1][x-1] = (int(middle_value / constant)) + scale
        #return the image, but the method which calls this must save it.
        
        max_value = np.amax(filtered)
        for x in range(0,len(filtered)):
            for y in range(0,len(filtered[0])):
                filtered[y][x] = (float(filtered[y][x])/float(max_value))*255
                
        return Image.fromarray(filtered)
        



        
if __name__ == "__main__":
    #main function, parts can be uncommented to test various features.
    #imageprocessing = ImageProcessing("shapes.jpg")
    imageprocessing = ImageProcessing("Boston_Normal.bmp")
    #imageprocessing = ImageProcessing("wdg4.gif")
    
    
    #imageprocessing.linearSmoothingFilter()
    #imageprocessing.linearSmoothingFilter(weighted=True)
    
    #imageprocessing.gaussianFilter(0.5)
    
    #imageprocessing.medianFilter()
    
    #imageprocessing.laplacianFilter()
    #imageprocessing.laplacianFilter(False)
    
    #imageprocessing.sobelFilter("x")
    #imageprocessing.sobelFilter("y")
    #imageprocessing.sobelFilter("xtheny")
    #imageprocessing.sobelFilter("ythenx")