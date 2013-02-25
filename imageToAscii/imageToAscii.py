#python 2, remember
import Image,sys,os,time

def asciiArt():
    charArray = ["0","1","2","3","4","5","6","7","8","9"]#means something entirely different in C
    for imfile in sys.argv[1:]:
        im = Image.open(imfile)
        name,extension = os.path.splitext(imfile)
        xsize,ysize = im.size
        pixels = im.load()
               
        f = open(name+str(time.time())+".out","w")
   
        for y in range(0,ysize):
            for x in range(0,xsize):
                total = sum(pixels[(x,y)])
                f.write(charArray[int(((total / 765.0) * len(charArray))-1)])#i think makes the last character appear only on full white. round would be better
            f.write("\n")
        f.close()
  
asciiArt()

