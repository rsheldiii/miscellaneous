""" is Sig On?
I watch a lot of speedruns on twitch.tv. Their API doesn't include an
"is someone on?" function, which is a shame, because their flash players will periodically lose stream, meaning you can't even just leave them on and change tabs when you can hear them start playing. on the person's personal video page though they will have a little red circle indicating if they are live or not, which can be screen-scraped to see if they are on. This is an API for just that, providing a simple function for asynch or a command-line option"""


import requests,sys,time,os
from bs4 import BeautifulSoup as Soup


    
def twitchFind(name):
    # I wrote an entire program based on the team page which was wonky but worked, and then I figure out its this easy from the videos page, and works better.
    # uses the "this is live" img on a streamer's page to check whether they are live or not
    soup = Soup(requests.get('http://twitch.tv/'+name+'/videos').text)
    text = soup.find("img",alt = "This is live")
    if text : 
        try:#just in case. I'll make this platform-independant. Or you can, if you cut these four lines
            os.system("chromium-browser twitch.tv/"+name)# :p
        except:
            ""
        return True
    return False

        
def findLoop(name,wait):
    """intended for command-line and script use. loops name indefinitely waiting specified number of seconds between calls"""
    while not twitchFind(name):
        print("checking at " + time.asctime())
        time.sleep(wait)
    return True
  
  
if __name__ == "__main__":      

    if len(sys.argv) == 2:
        print(twitchFind(sys.argv[1]))
    elif "loop" in sys.argv:
        sys.argv.remove("loop")
        findLoop(sys.argv[1],60)
    else:
        print(twitchFind("Siglemic"))
    
    
    
    
"""just in case the other way turns out to be bad or something:
def SRLFind(name):
    "ajax and one-time lookup function for any member on the front page of SRL's team page. returns number of viewers"
    name = name.lower()
    soup = Soup(requests.get('http://twitch.tv/team/srl').text)
    
    text = soup.find(id="channel_"+name)#finding div for member
    
    if text is None : return 0
    
    text = soup.find("span",{ "class" : "channel_count" })#finding only viewercount span class
    
    if text is None: return 0
    
    os.system("chromium-browser twitch.tv/"+name)#chromium call :p
    return int(text.string.strip())#return number of viewers"""
