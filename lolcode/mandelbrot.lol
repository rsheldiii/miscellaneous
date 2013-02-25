HAI 1.2
    CAN HAS STDIO?
    I HAS A XSIZE ITZ 256
    I HAS A YSIZE ITZ 256
    I HAS A MAXITERATIONZ ITZ 50
    I HAS A PIXELX ITZ 0
    
    IM IN YR LOOP UPPIN YR PIXELX TIL BOTH SAEM PIXELX AN SUM OF XSIZE AN 1 BTW // for pixelx in range(0,xsize)
    
        I HAS A PIXELY ITZ 0
        
        IM IN YR OTHERLOOP UPPIN YR PIXELY TIL BOTH SAEM PIXELY AN SUM OF YSIZE AN 1 BTW // for pixely in range(0,ysize)
            
            I HAS A X ITZ 0
            I HAS A Y ITZ 0
            I HAS A X0 ITZ DIFF OF QUOSHUNT OF PRODUKT OF 3.5 AN PIXELX AN XSIZE AN 2.5 BTW // X0 = 3.5 * PIXELX / XSIZE - 2.5
            I HAS A NUMBARYSIZE ITZ YSIZE
            MAEK NUMBARYSIZE A NUMBAR
            I HAS A Y0 ITZ DIFF OF QUOSHUNT OF PRODUKT OF 2.0 AN PIXELY AN YSIZE AN 1.0 BTW // Y0 = 2 * PIXELY / YSIZE - 1.0
            
            I HAS A ITERATIONZ ITZ 0
            
            IM IN YR ESCAPE
            
                I HAS A XTEMP ITZ SUM OF DIFF OF PRODUKT OF X AN X AN PRODUKT OF Y AN Y AN X0   BTW // XTEMP = X*X - Y*Y + X0
                Y R SUM OF PRODUKT OF PRODUKT OF 2 AN X AN Y AN Y0                              BTW // Y = 2*X*Y + Y0
                X R XTEMP
                
                BTW VISIBLE "X :{X} Y :{Y} CALC :{CALC}"
                
                I HAS A CALC ITZ SUM OF PRODUKT OF X AN X AN PRODUKT OF Y AN Y BTW // CALC = X*X + Y*Y
                
                DIFFRINT 4 AN BIGGR OF 4 AN CALC, O RLY?, YA RLY, GTFO BTW // if calc > 4: break
                OIC
                
                
                BOTH SAEM ITERATIONZ AN DIFF OF MAXITERATIONZ AN 1, O RLY?, YA RLY, GTFO BTW // if iterations == maxiterations: break
                OIC
                
                ITERATIONZ R SUM OF 1 AN ITERATIONZ BTW // iterationz += 1
                
            IM OUTTA YR ESCAPE
            
            VISIBLE QUOSHUNT OF ITERATIONZ AN QUOSHUNT OF MAXITERATIONZ AN 9! BTW // scaling number to be between 0 and 9. ! suppresses carriage return
            
        IM OUTTA YR OTHERLOOP
        
        VISIBLE "" BTW // carriage return for line
        
    IM OUTTA YR LOOP
KTHXBYE