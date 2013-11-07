miscellaneous
=============

miscellaneous projects and useful sripts that I have written.

This is actually where most of the fun happens :)

Conway's Game of Life:

  Game of Life simulator using a dictionary in Python as an infinitely extensible grid. each frame keeps track of all live cells and neighbors. It's never gonna beat a quadtree but it was a fun little day project
 
Automatic Quote Bot:
 
  bit of a hackish Reddit quote bot. Chooses a random wallpaper from /r/wallpapers and uses PIL to write a line from the top comment of a random post on a random subreddit on it. this is an older version that doesnt allow for selecting subreddits; I'll have to grab the new one off my raspi once I find it
 
gif2ascii:
  
  makes a gif into an ascii gif. Currently uses images2gif.py and the PIL to create a GIF. Unfortunately, images2gif does not really respect the GIF89a specification, and sticks a gigantic local color pallette in every frame. I'm working on creating my own GIF creator in python that will preserve global pallettes if they exist, stuck on LZW compression however
  
imageToAscii:
  
  beginning steps of the gif2ascii program that was actually entirely unrelated and done months before. creates a heatmap of an image's RGB intensity
  
issigon:
 
  before I found the email notifications on twitch.tv, I hooked this up to a cron job on my server to see if Siglemic was streaming
  
jsgallery:

  a javascript gallery I made for a friend. Uses some JQuery (but mostly CSS transitions) to create a scrolling image gallery with a large picture and full-window frame. Had a very rigid requirements specification, which made this project awesome
  
lolcode:

  lolcode is a defunct esoteric programming language written to sound like lolcats. It can't handle binary data, so I made a madelbrot heatmap generator in it. if ony the 1.3 spec were finished...
  
sinatraNotes:

  first attempt at writing a Ruby/Sinatra/Sequel application. Works pretty well!
