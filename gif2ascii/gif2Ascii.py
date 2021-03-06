'''
Created on Feb 21, 2013

@author: Dday
'''
import time
from PIL import Image, ImageSequence, ImageDraw, ImageFont
import sys, os, operator, math
from images2gif import writeGif

class gifToAscii:

    def __init__(self,f,scaling,color = False,font = "Courier.ttf"):
        
        self.start = time.time()
        #'Q','0','M', 'N', 'W', 'B', 'D', 'H', 'K',
        #self.brightness = [ '@', '$', 'U', '8', '&', 'A', 'O', 'k', 'Y', 'b', 'Z', 'G', 'P', 'X', 'g', 'E', '4', 'd', 'V', 'h', 'g', 'S', 'q', 'm', '6', 'p', 'F', '5', '2', '3', 'y', 'f', 'w', 'C', 'J', '#', 'T', 'n', 'u', 'L', 'j', 'z', '7', 'o', 'e', 'a', 't', '1', '[', ']', '!', '?', 'I', '}', '*', '{', 's', 'r', 'l', 'c', 'x', '%', 'v', 'i', ')', '>', '<', '\\', ')', '|', '"', '/', '+', '=', '^', ';', ',', ':', "'", '_', '-', '`', '.', ' '];
        self.brightness = list('@MND80Z$7I?+=~:,. ')
        self.scaling = scaling
        self.spacing = 3#font.getsize is not returning the correct height on windows
        self.fontsize = 12
        self.highestval = 255.0
        self.filename = f
        self.color = color
        self.font = ImageFont.truetype(font, self.fontsize)
        
        self.begin()
            
    
        
    def intensity(self,rgb):
        return .2126 * rgb[0]**2.2 + .7152 * rgb[1]**2.2 + .0722 * rgb[2]**2.2
    
    def getpalette(self,im):
        lut = im.resize((256, 1))
        lut.putdata(range(256))
        lut = lut.convert("RGB").getdata() 
        palette = list(lut)
        #print palette
        a = []
        for tuple in palette:
            a.extend(tuple)
        return a
        
    def calculate(self,im):
        i = 0
        previousframelist = None
        for frame in ImageSequence.Iterator(im):
            print i
            i+=1

            image = Image.new("P", (self.newwidth,self.newheight), 255)
            
            d_usr = ImageDraw.Draw(image)
            self.copy.append(frame.copy())
            framelist = list(frame.getdata())
            
            for y in range(0,self.scaledheight):
                line = ""
                for x in range(0,self.scaledwidth):
                    total = (0,0,0)
                    lineartotal = 0
                    for dy in range(0,self.scaling):
                        for dx in range(0,self.scaling):
                            xpos = x*self.scaling+dx
                            ypos = y*self.scaling+dy
                            paletteindex = framelist[xpos + ypos*self.width]
                            
                            if paletteindex == self.transparency:
                                paletteindex = previousframelist[xpos+ypos*self.width]
                                framelist[xpos+ypos*self.width] = paletteindex
                            
                            rgb = tuple(self.palette[paletteindex*3:paletteindex*3+3])
                            lineartotal += paletteindex
                            total = tuple(map(operator.add,rgb,total))
                    adji = self.highestval*(self.scaling**2)
                    intensity = self.intensity(tuple(map(operator.div,total,(adji,adji,adji))))
                    character = self.brightness[int(intensity*len(self.brightness))]#+" "
                    
                    
                    
                    if self.color:
                        d_usr.text((x*self.charwidth,y*self.charheight),character,fill=lineartotal/(self.scaling**2), font=self.font)    
                    else:
                        line += character
                if not self.color:
                    d_usr.text((0,y*self.charheight),line, fill=0, font=self.font)
                else:
                    image.putpalette(self.getpalette(frame))
                    #image.info["transparency"] = self.transparency
                
            self.images.append(image)
            previousframelist = framelist
    
    def begin(self):
        
        im = Image.open(self.filename)
        print "pallet"
        print len(im.getcolors())
        original_duration = im.info['duration']
        self.transparency = im.info.get('transparency',None)
        print im.info
        
        self.width,self.height = im.size
        self.scaledwidth,self.scaledheight = self.width/self.scaling,self.height/self.scaling
        print str(self.scaledwidth)+"x"+str(self.scaledheight)
        self.charwidth,self.charheight = self.font.getsize('7')
        self.charheight = self.charwidth + self.spacing#REMEMBER THIS
        
        self.newwidth = self.scaledwidth * self.charwidth#*2
        self.newheight = self.scaledheight * self.charheight

        print "calculating!"
        self.images = []
        self.copy = []
        
        
        assert im.mode == "P"
        self.palette = self.getpalette(im)
    
        print("asd")

        self.calculate(im)  
            
        print "writing!"
        print self.copy[1].info
        print im.getcolors() == self.copy[1].getcolors()
        writeGif("ascii_" + os.path.basename(self.filename), self.images, duration=original_duration/1000.0, dither=0, transparency = self.transparency)
        writeGif("copy_" + os.path.basename(self.filename), self.copy, duration=original_duration/1000.0, dither=0, transparency = self.transparency)
        print "done!"
        print "time diff " + str(time.time() - self.start)
        
    
a = gifToAscii('gifs/1348710922987.gif',1,True)
