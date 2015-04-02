import Image
import cv2
import numpy as np
import cmath
import math

###############################
#
# Class DFT
#
# Class is instantiated with an image path
# Optional Variable to change output name,
# Defaults to dft
#
# instance variables:
# self.M: The width of the image
# self.N: The height of the image
# self.imagePath: The image path
# self.name = the output name to append
# self.nonCenteredPix = the non centered image
# self.pix = the centered image array
# self.outputPower = the nonscaled Power
# self.scaledPower = the scaled power for display
# self.outputPhase = the nonscaled Phase
# self.scaledPhase = the scaled power for display
# self.outputIDFT = the Inverse DFT
# self.scaledIDFT = the scaled IDFT For display
###############################
class DFT:
    #initialize with a path and the name to save the image
    def __init__(self, imagePath, name="dft"):
        self.imagePath = imagePath
        self.name = name
        self.image = Image.open(imagePath).convert("L")
        (self.M, self.N) = self.image.size #set M and N based on the dimensions
        self.nonCenteredPix = np.asarray(self.image) 
        self.pix = np.empty([self.M, self.N])
        for x in range(self.M):
            for y in range(self.N):
                self.pix[x][y] = (self.nonCenteredPix[x][y])*(-1)**(x+y) #center the image

    #method used to take the DFT of the image, no input variables    
    def takeDft(self):
        self.outputPower = np.empty([self.M, self.N]) #initial storage
        self.scaledPower = np.empty([self.M, self.N]) #scaled output
        self.outputPhase = np.empty([self.M, self.N]) #initial storage
        self.scaledPhase = np.empty([self.M, self.N]) #scaled output
        
        max_value_power = 0 #used for scaling the image
        max_value_phase = 0
        
        for u in range(self.M):
            for v in range(self.N):
                complex = self.computePoint(u,v) #call method to compute the complex value
                
                self.outputPower[u][v] = abs(complex) #get abs for power plot
                if abs(complex) >= max_value_power:
                    max_value_power = abs(complex) #need max value for scaling
                
                self.outputPhase[u][v] = cmath.phase(complex) #get phase for phase plot
                if cmath.phase(complex) >= max_value_phase: 
                    max_value_phase = cmath.phase(complex) #need max value for scaling
        for u in range(self.M):
            for v in range(self.N):
                self.scaledPower[u][v] = int((255.0/math.log10(256))*(math.log10(1+
                        ((255.0*self.outputPower[u][v])/(max_value_power)))))
                self.scaledPhase[u][v] = int((255.0/math.log10(256))*(math.log10(1+
                        ((255.0*abs(self.outputPhase[u][v]))/(max_value_phase)))))
                #After calculating, scale the image to be displayed properly
        outputDFT_im = Image.fromarray(self.scaledPower) #convert to image and save
        outputDFT_im.convert('RGB').save(self.name + "dftPower.jpg")
   
        outputDFT_im = Image.fromarray(self.scaledPhase)
        outputDFT_im.convert('RGB').save(self.name + "Phase.jpg")
            
    def computePoint(self,u,v):
        #set point to 0, needs to be a float
        #A lot of weird errors were cause by rounding, so everything is kepy
        #as a float for as long as possible
        outputPoint = 0.0
        for x in range(self.M):
            for y in range(self.N):
                point = self.pix[x][y] #get the value at that point
                #get the exponential separately
                exponent =  cmath.exp(- 1j * cmath.pi * 2.0 * (float(u * x) / self.M + float(v * y)  / self.N))
                outputPoint += point * exponent #multiply the two together and save
        return (outputPoint) #return once done
    
    #IDFT has one tag to handle using both (none)
    #just the phase (phase)
    #just the power (power)
    def takeIDFT(self,tag='none'):
        self.outputIDFT = np.empty([self.M, self.N]) #the actual values
        self.scaledIDFT = np.empty([self.M, self.N]) #the values scaled for display
        
        max_value = 0 #used to scaling the image
        
        for x in range(self.M):
            for y in range(self.N):
                value = self.computeIPoint(x,y,tag) #take the inverse of the point
                self.outputIDFT[x][y] = abs(int(value.real)) #save the real part, remove negatives
                if self.outputIDFT[x][y] >= max_value:
                    max_value = self.outputIDFT[x][y] #max value used for scaling
        
        for x in range(self.M):
            for y in range(self.N):
                self.scaledIDFT[x][y] = int((255.0/math.log10(256))*(math.log10(1+
                        ((255.0*abs(self.outputIDFT[x][y]))/(max_value)))))
        #After calculating, scale the image
        
        #save the scaled image with the name and tag to identify the plot
        outputiDFT_im = Image.fromarray(self.scaledIDFT)
        outputiDFT_im.convert('RGB').save(self.name + "idftImage"+ tag + ".jpg")                 
   
    def computeIPoint(self, x, y,tag):
        outputPoint = 0.0 #set the output to zero, as a flot
        for u in range(self.M):
            for v in range(self.N):
                if tag == 'none': #if none use both
                    point = cmath.rect(self.outputPower[u][v], self.outputPhase[u][v])
                if tag == 'phase': #if phase use only phase
                    point = self.scaledPhase[u][v]
                if tag == 'power': #if power use only power
                    point = self.outputPower[u][v]
                #combine chosen point with the exponent separately
                #remember to use opposite sign of computePoint
                exponent = cmath.exp(1j * cmath.pi * 2.0 *((float(u*x)/self.M)+(float(v*y)/self.N)))
                outputPoint += point * exponent
        #Divide by M and N since it was not done before
        return (outputPoint / (self.M * self.N))


if __name__ == "__main__":
    #Load the two images
    imagePath = "BWskull.jpg"
    imagePath2 = "sword.png"
    #imagePath = "elephant.png"
    #imagePath2 = "sheep.png"

    #load each
    dft = DFT(imagePath,"skull")
    dft2 = DFT(imagePath2,"sword")
    
    #take DFT/IDFT of one
    dft.takeDft() #take DFT
    dft.takeIDFT() #then take inverse, error if done first
    dft.takeIDFT("phase") #take just the phase
    dft.takeIDFT("power") #take just the power
    
    #take DFT/IDFT of second
    dft2.takeDft() #take DFT
    dft2.takeIDFT() #then take inverse
    dft2.takeIDFT("phase") #take just the phase
    dft2.takeIDFT("power") #take just the power
    
    #create a new array, and store one of the powers
    TEMPoutputPower = np.empty([dft.M, dft.N])
    TEMPoutputPower = dft.outputPower
    
    #change the name of the dft to create a unique
    #output file.
    dft.name = "SwitchedPhase1"
    dft2.name = "SwitchedPhase2"
    
    #Swap the output powers
    dft.outputPower = dft2.outputPower
    dft2.outputPower = TEMPoutputPower
    
    #take the inverse DFTs again
    dft2.takeIDFT()
    dft.takeIDFT()
    

    