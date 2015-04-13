import Image
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import spatialfilters #previous assignment is referenced

###############################
#
# FFT Filter
#
# Class is instantiated with an image path
# Methods allow for editing of image
# using frequency domain techniques
#
# instance variables:
# self.row: The width of the image
# self.column: The height of the image
# self.image: The image loaded from the path
# self.paddedimage: The image, padded with 0's
# self.fft: The fft of the image
# self.fshift: The shifted fft
#
################################


class fft_filter():
    
###############################
#
# Initialization
# Inputs: imagepath - path to image
# 
# Outputs: Loads self.row, self.column,self.paddedimage and
# self.image for use. Runs the private method
# __pad() to pad the image
# __fft() to take the fft of the image 
#
#
################################
    def __init__(self,imagePath):
        self.image = cv2.imread(imagePath,0)
        (self.rows, self.columns) = self.image.shape
        self.paddedimage = self.__pad(self.image)
        self.__fft()
###############################
#
# Method: graph
#
# This graphs the fft. 
# Used for debug to ensure FFT
# was being taken correctlly.
# Inputs: none
# Outputs: none
#
#
################################        
    def graph(self):
        plt.subplot(131),plt.imshow(self.image, cmap = 'gray')
        plt.subplot(132),plt.imshow(self.magnitudeSpec, cmap = 'gray')
        plt.subplot(133),plt.imshow(self.phaseSpec, cmap = 'gray')
        plt.show()
###############################
#
# Method: __pad()
# private method
# 
# This method pads the image for
# should be run before filtering takes
# place
# Inputs: image - the image to pad
# Outputs: the image, padded with 0's
#
#
################################       
    def __pad(self,image):
        
        #create an array of zeroes, twice as wide and tall
        padded_image = np.zeros((2*self.rows,2*self.columns), dtype=np.int)
        
        #put the image in the top right quadrant
        for row in range(self.rows):
            for column in range(self.columns):
                padded_image[row][column] = image[row][column]

        
        return padded_image 

        #can be uncommented to save the padded image.
        #useful for debugging.
        #im = Image.fromarray(np.uint8(padded_image))
        #im.convert('RGB').save("padded.jpg")
###############################
#
# Method: __fft()
# private method
# 
# This method pads the image for
# should be run before filtering takes
# place
# Inputs: none
# Outputs: the FFT image is saved.
# initializes self.fft, self.fshift,
# self.magnitudeSpec, and self.phaseSpec
#
# Returns None
#
################################
    def __fft(self):
        self.fft = np.fft.fft2(self.paddedimage)
        self.fshift = np.fft.fftshift(self.fft)
        self.magnitudeSpec = 20*np.log(np.abs(self.fshift))
        self.phaseSpec = 20*np.log(np.angle(self.fshift))
        im = Image.fromarray(np.uint8(self.magnitudeSpec))
        im.convert('RGB').save("FFT.jpg")
###############################
#
# Method: ideaLowpassFilter()
# 
# Runs the ideal Low Pass Filter of the image
# 
# acts as a wrapper for self.idealFilter
#
# Inputs: frequency
# Outputs: saves the image and the
# fft transform
#
#
################################        
    def idealLowpassFilter(self,frequency):
        self.idealFilter(frequency)

###############################
#
# Method: ideaHighpassFilter()
# 
# Runs the ideal High Pass Filter of the image
# 
# acts as a wrapper for self.idealFilter
#
# Inputs: frequency
# Outputs: saves the image and the
# fft transform
#
#
################################    
        
    def idealHighpassFilter(self,frequency):
        self.idealFilter(frequency,False)
###############################
#
# Method: gaussianLowpassFilter()
# 
# Runs the Gaussian Low Pass Filter 
# of the image
# 
# acts as a wrapper for self.gaussianFilter
#
# Inputs: frequency
# Outputs: saves the image and the
# fft transform
#
################################               
    def gaussianLowpassFilter(self,frequency):
        self.gaussianFilter(frequency)
        
###############################
#
# Method: gaussianHighpassFilter()
# 
# Runs the Gaussian High Pass Filter 
# of the image
# 
# acts as a wrapper for self.gaussianFilter
#
# Inputs: frequency
# Outputs: saves the image and the
# fft transform
#
################################      
    def gaussianHighpassFilter(self,frequency):
        self.gaussianFilter(frequency,False)
        
###############################
#
# Method: idealFilter()
# 
# method for running high and low pass
# ideal filters. 
#
# if low is True: Low pass
# otherwsie: High pass
# 
#
# Inputs: frequency, low
# Outputs: saves the image and the
# fft transform
#
################################         
    def idealFilter(self,frequency,low=True):
        #Filter will hold the generated filter
        filter = np.zeros((2*self.rows, 2*self.columns), dtype=np.int)
        
        #cropped will be used to "unpad" the image
        cropped = np.zeros((self.rows, self.columns), dtype = np.int)
        
        #referenced to cut down on typing
        a = self.rows / 2
        b = self.columns / 2
        
        #for each point, generate the filter
        for row in range((-1*self.rows),self.rows):
            for column in range((-1*self.columns),self.columns):
                #if low, filter out everything but the specified region
                if low:
                    if (((row - a) ** 2) + ((column - b) ** 2) <= frequency ** 2):
                        filter[row + a][column + b] = 1
                #if high filter out the region
                else:
                    if (((row - a) ** 2) + ((column - b) ** 2) >= frequency ** 2):
                        filter[row + a][column + b] = 1
        
        #apply the filter
        outputFFT = np.multiply(self.fshift, filter)
        
        #save the images, adjusting the name accordingly
        im = Image.fromarray(np.uint8(20*np.log(np.abs(outputFFT))))
        if low:
            im.convert('RGB').save("IdealLPFFT.jpg")
        else:
            im.convert('RGB').save("IdealHPFFT.jpg")
        
        outputImage = np.fft.ifftshift(outputFFT)
        outputImage = np.fft.ifft2(outputImage)
        
        #crop the image before saving
        for row in range(self.rows):
            for column in range(self.columns):
                cropped[row][column] = abs(outputImage[row][column])
        
        im = Image.fromarray(np.uint8(cropped))
        if low:
            im.convert('RGB').save("IdealLP.jpg")
        else:
            im.convert('RGB').save("IdealHP.jpg")
###############################
#
# Method: gaussianFilter()
# 
# method for running high and low pass
# gaussian filters. 
#
# if low is True: Low pass
# otherwsie: High pass
# 
#
# Inputs: frequency, low
# Outputs: saves the image and the
# fft transform
#
################################ 
    def gaussianFilter(self, frequency, low=True):
        #Filter will hold the generated filter image
        filter = np.zeros((2*self.rows, 2*self.columns), dtype=np.float)
        #cropped will hold the "unpadded" image
        cropped = np.zeros((self.rows, self.columns), dtype = np.int)
        
        #use to save typing
        a = self.rows
        b = self.columns
        
        #used to modify the gaussian filter
        highLow = 0 if low else 1
        
        #apply the filter
        for row in range((-1*self.rows),self.rows):
            for column in range((-1*self.columns),self.columns):
                distance = math.sqrt(row**2 + column**2)
                filter[row + a][column + b] = highLow - (math.exp(-1.0*distance/((2.0*frequency)**2.0)))
        
        #output the applied filter
        outputFFT = np.multiply(self.fshift, filter)
        
        #save the image
        im = Image.fromarray(np.uint8(20*np.log(np.abs(outputFFT))))
        if low:
            im.convert('RGB').save("GaussianLPFFT.jpg")
        else:
            im.convert('RGB').save("GaussianHPFFT.jpg")
        
        outputImage = np.fft.ifftshift(outputFFT)
        outputImage = np.fft.ifft2(outputImage)
        
        #crop and save the image
        for row in range(self.rows):
            for column in range(self.columns):
                cropped[row][column] = abs(outputImage[row][column])
        
        im = Image.fromarray(np.uint8(cropped))
        if low:
            im.convert('RGB').save("GaussianLP.jpg")
        else:
            im.convert('RGB').save("GaussianHP.jpg")
###############################
#
# Method: laplacianFilter()
# 
# method for running the laplacian filter
#
# if GaussFirst=True,
# run the Gaussian first
# 
#
# Inputs: frequency, GaussFirst
# Outputs: saves the image and the
# fft transform
#
################################           
    def laplacianFilter(self,GaussFirst=False,frequency=5):
        #filter holds the generated filter
        filter = np.zeros((2*self.rows, 2*self.columns), dtype=np.float)
        #cropped holds the "unpadded image"
        cropped = np.zeros((self.rows, self.columns), dtype = np.int)
    
        #max value is used to scale the image to be viewed
        a = self.rows
        b = self.columns
        max_value = 0
        
        #Generate the filter and save the max value
        for row in range(self.rows * 2):
            for column in range(self.columns * 2):
                filter[row][column] = math.sqrt(((row - a)**2 + (column - b)**2))
                if abs(filter[row][column]) >= max_value:
                    max_value = abs(filter[row][column])
        #scale the image accordingly for displaying
        for row in range(self.rows * 2):
            for column in range(self.columns * 2):
                filter[row][column] = (filter[row][column]/float(max_value))
        
        #The way the code was written, the Gauss needed to be written
        #a second time.
        if GaussFirst:
            gfilter = np.zeros((2*self.rows, 2*self.columns), dtype=np.float)
            for row in range((-1*self.rows),self.rows):
                for column in range((-1*self.columns),self.columns):
                    distance = math.sqrt(row**2 + column**2)
                    gfilter[row + a][column + b] = (math.exp(-1.0*distance/((2.0*frequency)**2.0)))
                
                #combine the filters first, then apply to update
                combinedFilter = np.multiply(gfilter, filter)
                outputFFT = np.multiply(self.fshift, combinedFilter)
        else:
            outputFFT = np.multiply(self.fshift, filter)
        #save image fft
        im = Image.fromarray(np.uint8(20*np.log(np.abs(outputFFT))))
        if GaussFirst:
            im.convert('RGB').save("GLFFT.jpg")
        else:
            im.convert('RGB').save("LaplacianFFT.jpg")

        #inverse fourier transform and save image
        outputImage = np.fft.ifftshift(outputFFT)
        outputImage = np.fft.ifft2(outputImage)
        
        #use the max_value to scale again
        max_value = abs(np.amax(outputImage))
        for row in range(self.rows):
            for column in range(self.columns):
                cropped[row][column] = (abs(outputImage[row][column])/max_value)*255
                
        
        im = Image.fromarray(np.uint8(cropped))
        if GaussFirst:
            im.convert('RGB').save("GLaplacian.jpg")
        else:
            im.convert('RGB').save("Laplacian.jpg")
###############################
#
# Method: compare()
# 
# method for comparing the spatial
# filters with the frequency filters
#
# Inputs: None
# Outputs: The comparison
#
################################         
    def compare(self):
        #open the appropriate files
        spatialGaussian = cv2.imread("SPATIALGaussian.jpg",0)
        FFTGaussian = cv2.imread("GaussianLP.jpg",0)
        
        #create an empty array and fill with the difference
        gaussCompare = np.zeros((self.rows, self.columns), dtype = np.int)
        gaussCompare = abs(np.subtract(spatialGaussian,FFTGaussian))
        
        #open the appropriate files
        spatialLaplacian = cv2.imread("SPATIALLaplacian.jpg",0)
        FFTLaplacian = cv2.imread("Laplacian.jpg",0)
        
        #create an empty array and fill with the difference
        lapCompare = np.zeros((self.rows, self.columns), dtype = np.int)
        lapCompare = abs(np.subtract(spatialLaplacian,FFTLaplacian))
        
        #use matplotlib to plot all on the same chart
        plt.subplot(231),plt.imshow(spatialGaussian, cmap = 'gray')
        plt.subplot(232),plt.imshow(FFTGaussian, cmap = 'gray')
        plt.subplot(233),plt.imshow(gaussCompare, cmap = 'gray')
        plt.subplot(234),plt.imshow(spatialLaplacian, cmap = 'gray')
        plt.subplot(235),plt.imshow(FFTLaplacian, cmap = 'gray')
        plt.subplot(236),plt.imshow(lapCompare, cmap = 'gray')
        
        #show the graph
        plt.show()
        

if __name__ == "__main__":
    #load the image
    fft = fft_filter("lenna.jpg") 
    
    #comment and uncomment as necessary to view different
    #features
    #fft.graph()
    #fft.idealLowpassFilter(50)
    #fft.idealHighpassFilter(20)
    fft.gaussianLowpassFilter(10)
    #fft.gaussianLowpassFilter(0.5)
    #fft.gaussianHighpassFilter(5)
    #fft.laplacianFilter()
    fft.laplacianFilter(True)
    
    spatial = spatialfilters.ImageProcessing("lenna.jpg")
    spatial.laplacianFilter()
    spatial.gaussianFilter(0.5)
    fft.compare()
    
    