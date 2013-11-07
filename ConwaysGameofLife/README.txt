python 3 only

currently set up for random input for 70 frames, but accepts CSVs as input as well

infinite extensible grid via a dictionary. as such large simulations are probably slow. I try to account for that by keeping track of all cells that have any chance of being alive next iteration, but there's only so much you can do with a dictionary