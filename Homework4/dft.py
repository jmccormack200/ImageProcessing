import Image
import cv2
import numpy as np
import cmath
import math

class DFT:
    
    def __init__(self, imagePath, name="dft"):
        self.imagePath = imagePath
        self.name = name
        self.image = Image.open(imagePath).convert("L")
        (self.M, self.N) = self.image.size
        self.nonCenteredPix = np.asarray(self.image)
        self.pix = np.empty([self.M, self.N])
        for x in range(self.M):
            for y in range(self.N):
                self.pix[x][y] = (self.nonCenteredPix[x][y])*(-1)**(x+y)

        
    def takeDft(self):
        self.outputPower = np.empty([self.M, self.N])
        self.scaledPower = np.empty([self.M, self.N])
        self.outputPhase = np.empty([self.M, self.N])
        self.scaledPhase = np.empty([self.M, self.N])
        
        max_value_power = 0
        max_value_phase = 0
        
        for u in range(self.M):
            for v in range(self.N):
                complex = self.computePoint(u,v)
                
                self.outputPower[u][v] = abs(complex)
                if abs(complex) >= max_value_power:
                    max_value_power = abs(complex)
                
                self.outputPhase[u][v] = cmath.phase(complex)
                if cmath.phase(complex) >= max_value_phase:
                    max_value_phase = cmath.phase(complex)

        for u in range(self.M):
            for v in range(self.N):
                self.scaledPower[u][v] = int((255.0/math.log10(256))*(math.log10(1+
                        ((255.0*self.outputPower[u][v])/(max_value_power)))))
                self.scaledPhase[u][v] = int((255.0/math.log10(256))*(math.log10(1+
                        ((255.0*abs(self.outputPhase[u][v]))/(max_value_phase)))))
            
        outputDFT_im = Image.fromarray(self.scaledPower)
        outputDFT_im.convert('RGB').save(self.name + "dftPower.jpg")
   
        outputDFT_im = Image.fromarray(self.scaledPhase)
        outputDFT_im.convert('RGB').save(self.name + "Phase.jpg")
            
    def computePoint(self,u,v):
        outputPoint = 0.0
        for x in range(self.M):
            for y in range(self.N):
                point = self.pix[x][y]
                exponent =  cmath.exp(- 1j * cmath.pi * 2.0 * (float(u * x) / self.M + float(v * y) / self.N))
                outputPoint += point * exponent
        return (outputPoint)

    def takeIDFT(self,tag='none'):
        self.outputIDFT = np.empty([self.M, self.N])
        
        for x in range(self.M):
            for y in range(self.N):
                value = self.computeIPoint(x,y,tag)
                self.outputIDFT[x][y] = abs(int(value.real))
        
        
        outputiDFT_im = Image.fromarray(self.outputIDFT)
        outputiDFT_im.convert('RGB').save(self.name + "idftImage"+ tag + ".jpg")                 
   
    def computeIPoint(self, x, y,tag):
        outputPoint = 0.0
        for u in range(self.M):
            for v in range(self.N):
                if tag == 'none':
                    point = cmath.rect(self.outputPower[u][v], self.outputPhase[u][v])
                if tag == 'phase':
                    point = self.outputPhase[u][v]
                if tag == 'power':
                    point = self.outputPower[u][v]
                exponent = cmath.exp(1j * cmath.pi * 2.0 *((float(u*x)/self.M)+(float(v*y)/self.N)))
                outputPoint += point * exponent
        return (outputPoint / (self.M * self.N))


if __name__ == "__main__":
    imagePath = "BWskull.jpg"
    imagePath2 = "sword.png"
    #imagepath = "lenna.gif"
    #imagePath2 = "cln1.gif"

    dft = DFT(imagePath,"skull")
    dft2 = DFT(imagePath2,"sword")
    dft.takeDft()
    dft.takeIDFT()
    #dft.takeIDFT("phase")
    #dft.takeIDFT("power")
    
    #dft2.takeDft()
    #dft2.takeIDFT()
    #dft2.takeIDFT("phase")
    #dft2.takeIDFT("power")
    
    #TEMPscaledPower = np.empty([dft.M, dft.N])
    #TEMPscaledPower = dft.scaledPower
    #dft.scaledPower = dft2.scaledPower
    #dft2.scaledPower = TEMPscaledPower
    
    #dft2.takeIDFT()
    #dft.takeIDFT()
    

    