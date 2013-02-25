'''
Created on Feb 24, 2013

@author: Dday
'''
import struct,sys
from types import *
class GifExaminer:
    def __init__(self,filename):
        self.imageCount = 0
        self.images = []
        self.file = open(filename,'rb')
        self.readHeader()
        self.extensionBlockFunctions = {249 : self.readGraphicsControlBlock, 255 : self.readApplicationBlock}
        self.blockFunctions = {33 : self.determineExtensionBlock, 44 : self.readImageBlock, 59:self.exit}
        
        if self.globalPalette:
            self.readColorPalette(self.globalPaletteSize)
            
        while True:
            functionIdentifier = self.file.read(1)
            if functionIdentifier == '':
                break
            print ord(functionIdentifier)
            self.blockFunctions.get(ord(functionIdentifier),self.incorrectFormat)()
        
    
    def readNextBlock(self):
        self.file.read(1)
        
    def readHeader(self):
        name,self.width,self.height,packvar,self.backgroundColor,self.aspectRatio = struct.unpack('6shhsss',self.file.read(13))
        packvar = ord(packvar)
        print "GIF version:"
        print name
        print "canvas size:"
        print (self.width,self.height)
        print "pack byte:"
        print '{0:08b}'.format(packvar)
        
        #global color palette
        a =  self.extractIntFromByte(packvar, 0, 1)
        print "Global color palette: ",
        if a==1:
            self.globalPalette = True
            print "yes"
        else:
            self.globalPalette = False
            print "no"
            
        #global color palette color resolution
        print "color resolution:"
        self.globalPaletteColorResolution = self.extractIntFromByte(packvar, 1, 3)+1
        print self.globalPaletteColorResolution
        
        #global palette sort flag
        print "global palette sorted: ",
        a = self.extractIntFromByte(packvar, 4, 1)
        if a == 1:
            print "yes"
            self.globalPaletteSortFlag = True
        else:
            print "no"
            self.globalPaletteSortFlag = False
        
        #global color palette total size
        self.globalPaletteSize = 2**(self.extractIntFromByte(packvar, 5, 3)+1)*3
        print "global palette size (total) in bytes: "
        print self.globalPaletteSize
        
        #background color
        self.backgroundColor = ord(self.backgroundColor)
        print "background color palette index:"
        print self.backgroundColor
        
        #aspect ratio
        self.aspectRatio = ord(self.aspectRatio)
        print "aspect ratio:"
        print self.aspectRatio
        
    def readColorPalette(self,size):
        rawdata = self.file.read(size)
        palette = []
        for i in range(0,size/3):
            palette.append(tuple(map(ord,(rawdata[i*3],rawdata[i*3+1],rawdata[i*3+2]))))
        print "palette:"
        print palette
        
        return palette
            
        
    def extractIntFromByte(self,number,start,bitlength,littleendian = False):
        if (littleendian):
            number = self.reverseEndianness(number, 8)
            start = 8 - start - bitlength
        return (number & int('0'*start+'1'*bitlength+'0'*(8-start-bitlength),2)) >> 8-start-bitlength
    
    def reverseEndianness(self,a,size):
        b = 0
        for i in range(size):
            b <<= 1
            b |= a >> i & 1
        return b
    
    def determineExtensionBlock(self):
        controlchar = ord(self.file.read(1))
        print controlchar
        self.extensionBlockFunctions.get(controlchar,self.incorrectFormat)()
        
    def readGraphicsControlBlock(self):
        print "graphics control block"
        size = ord(self.file.read(1))
        assert size == 4
        
        packvar = ord(self.file.read(1))
        dispose = self.extractIntFromByte(packvar, 3, 3)
        print "disposal method: "
        print {0 : "no action", 1: "do not dispose", 2: "restore to background color" ,3: "restore to previous" }.get(dispose,"not defined or error")
        
        self.userinput = self.extractIntFromByte(packvar, 6, 1)
        print "user input: ",
        if self.userinput == 1:
            print "expected. um, what?"
            self.userinput = True
        else:
            print "not expected"
            self.userinput = False
        
        self.transparency = self.extractIntFromByte(packvar, 7, 1)
        print "transparency: ",
        if self.transparency == 1:
            print "specified"
            self.transparency = True
        else:
            print "none"
            self.transparency = False
            
        self.delayTime = struct.unpack('h',self.file.read(2))[0]
        print "delay time in 1/100ths of a second:"
        print self.delayTime
        
        self.currenttransparencyIndex = ord(self.file.read(1))
        print "transparency pallet index:"
        print self.currenttransparencyIndex
        
        assert ord(self.file.read(1)) == 0
        
        
        
        
    def readApplicationBlock(self):
        print "application extension block"
        size = ord(self.file.read(1))
        assert size == 11
        
        
        self.application = self.file.read(size)
        print "application:"
        print self.application
        
        applicationdatasize = ord(self.file.read(1))
        print "application information:"
        print self.file.read(applicationdatasize)
        
        assert 0 == ord(self.file.read(1))
        
    def readImageBlock(self):
        left,top,width,height,packvar = struct.unpack('hhhhs',self.file.read(9))
        packvar = ord(packvar)
        print "image position: "
        print (left,top)
        
        print "image wxh: "
        print (width,height)
        
        print "pack var:"
        print bin(packvar)
        
        LCTF,interlace,sort,LCTFsize = self.extractIntFromByte(packvar, 0, 1),\
                                       self.extractIntFromByte(packvar, 1, 1),\
                                       self.extractIntFromByte(packvar, 2, 1),\
                                       2**(self.extractIntFromByte(packvar, 5,3)+1)*3
        print "local color table: ",
        if LCTF == 1:
            print "yes"
        else:
            print "no"
            
        print "interlace: ",
        if interlace == 1:
            print "yes"
        else:
            print "no"
            
        print "sorted table: ",
        if sort == 1:
            print "yes"
        else:
            print "no"
        
        print "LCTF total size:"
        print LCTFsize
        
        if LCTF:
            LCTFarr = self.readColorPalette(LCTFsize)
        
        LZWminsize = ord(self.file.read(1))
        print "lzw minimum code size: "
        print LZWminsize
        
        imagedata = ""
        print "image encountered"
        while True:
        
            imageblocksize = ord(self.file.read(1))
            if imageblocksize == 0:
                self.imageCount += 1
                self.images.append(imagedata)
                print "got out of images"
                break
            #print "image block size: "
            #print imageblocksize
        
            imagedata += self.file.read(imageblocksize)
            #print "image data:"
            #print imagedata
            
    def exit(self):
        print self.imageCount
        print "file finished. exiting"
            
        
        
        
    
    def incorrectFormat(self):
        print "something went wrong"
        
        
        
a = GifExaminer('gifs/1348710922987.gif')
#b = GifExaminer('copy_1348710922987.gif')
