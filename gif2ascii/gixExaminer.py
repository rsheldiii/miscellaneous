'''
Created on Feb 24, 2013

@author: Dday
'''
import struct,sys
from types import *
from bitstring import *
class GifExaminer:
    def __init__(self,filename):
        self.imageCount = 0
        self.images = []
        self.file = open(filename,'rb')
        self.readHeader()
        self.extensionBlockFunctions = {249 : self.readGraphicsControlBlock, 255 : self.readApplicationBlock}
        self.blockFunctions = {33 : self.determineExtensionBlock, 44 : self.readImageBlock, 59:self.exit}
        
        if self.globalPalette:
            self.globalPalette = self.readColorPalette(self.globalPaletteSize)
            
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
            
        
    def extractIntFromByte(self,number,start,bitlength):
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
        self.header("GRAPHICS CONTROL EXTENSION BLOCK")
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
        self.header("APPLICATION EXTENSION BLOCK")
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
        self.header("IMAGE BLOCK")
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
        
        imagestream = BitArray(bytes = imagedata)
        reversedstream = BitArray()
        for i in range(0,len(imagedata)):
            byte = BitArray(bytes = imagedata[i])
            byte.reverse()
            reversedstream.append(byte)
        
        self.lzwDecode(reversedstream,LZWminsize)
            
        
        
        
            
    def lzwDecode(self,imageblock,defaultcodesize):
        decompressedString = ""
        codesize = defaultcodesize + 1
        pointer = 0
        numtostr = {}
        strtonum = {}
        nextcodepoint = 2**codesize +2
        for i in range(0,2**(codesize)-1):
            numtostr[i] = chr(i)
            strtonum[chr(i)] = i
        
        clearcode = 2**defaultcodesize
        endcode = 2**defaultcodesize+1
        currentCode = ""    
        
        while True:
            word = imageblock[pointer:pointer+codesize]
            word.reverse()
            if word.uint == endcode:
                break;
            elif word.uint == clearcode:
                print "implement clear code"
            elif numtostr.get(word.uint,False) != False:
                currentCode += numtostr[word.uint]
                
                if strtonum.get(currentCode,False) == False:
                    decompressedString += currentCode
                    strtonum[currentCode] = nextcodepoint
                    numtostr[nextcodepoint] = currentCode
                    currentCode = numtostr[word.uint]
                    nextcodepoint +=1
                else:
                    ""
            else:#edge case
                print "whoopsie"
                
            pointer += codesize
            
        print self.globalPalette[ord(decompressedString[0])]
                
    
    def exit(self):
        print self.imageCount
        print "file finished. exiting"
            

    def incorrectFormat(self):
        print "something went wrong"
        
    def header(self,title):
        print "-"*80
        print title
        print "-"*80
        
a = GifExaminer('wkY1FUI.gif')
#b = GifExaminer('copy_1348710922987.gif')
