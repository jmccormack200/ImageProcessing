import Image
import cv2
import numpy as np
import cmath
import math

class DFT:
    
    def __init__(self, imagePath):
        self.imagePath = imagePath
        self.image = Image.open(imagePath).convert("L")
        (self.M, self.N) = self.image.size
        self.nonCenteredPix = np.asarray(self.image)
        self.pix = np.empty([self.M, self.N])
        for x in range(self.M):
            for y in range(self.N):
                self.pix[x][y] = self.nonCenteredPix[x][y]*(-1)**(x+y)

        
    def takeDft(self):
        outputPower = np.empty([self.M, self.N])
        outputPhase = np.empty([self.M, self.N])
        
        for u in range(self.M):
            for v in range(self.N):
                complex = self.computePoint(u,v)
                outputPower[v][u] = math.log10(int(cmath.sqrt(complex.real**2 + complex.imag**2).real)+1)
                #outputPhase[v][u] = cmath.atan(complex.imag/complex.real).real * 10 + 128
        
        for a in outputPower:
            print a

        outputDFT_im = Image.fromarray(outputPower)
        outputDFT_im.convert('RGB').save("dftPower.jpg")
       
        #outputDFT_im = Image.fromarray(outputPhase)
        #outputDFT_im.convert('RGB').save("dftPhase.jpg")
            
    def computePoint(self,v,u):
        outputPoint = 0.0
        for x in range(self.M):
            for y in range(self.N):
                point = self.pix[x][y]
                exponent =  cmath.exp(-2j*cmath.pi*((float(u*x)/self.M) + (float(v*y)/self.N)))
                outputPoint += point * exponent
        return (outputPoint)    


if __name__ == "__main__":
    #imagePath = "BWskull.jpg"
    #imagePath = "cln1.gif"
    #imagePath = "360e.png"
    imagePath = "inverseSkull.png"
    dft = DFT(imagePath)
    dft.takeDft()

    