import requests,time,json,re,random
from PIL import Image,ImageDraw,ImageFont
from StringIO import StringIO


class quoteMaker:
	
	def __init__(self):
		self.regexDict = {'gallery' : re.compile(r'(http://)?(imgur\.com/[a-zA-Z0-9#]*)'),#has to have the end because otherwise albums would match too
		                  'image' : re.compile(r'(http://)?i\.imgur\.com/.*'),
		                  'album' : re.compile(r'(http://)?(www\.)?imgur\.com/a/.*')}
		                  
		self.headers = {'User-Agent' : 'instant wallpaper quote bot by /u/wallpaperquotebot'}
		self.session = requests.session(headers=self.headers)
		payload = {'passwd' : "8Characters!",'user' : "wallpaperquotebot",'rem' : True}
		print(self.session.post('http://www.reddit.com/api/login',data=payload,headers=self.headers))
		time.sleep(2);
	def setPictureUrl(self):
		subject = self.session.get("http://www.reddit.com/r/wallpapers/random.json")#TODO: make one that pulls a random wallpaper from hot so we can use this on a daily basis (as it prolly wont pull the same one) and it will be of higher quality
		imageJson = subject.json[0]
		imageURL = imageJson[u'data'][u'children'][0][u'data'][u'url']
		print(imageURL)
		
		#begin imageURL parsing
		if "imgur.com" in imageURL:
			if self.regexDict["image"].match(imageURL):
				#good, no preprocessing
				self.imageURL = imageURL
				self.setPILImage()
				
			if self.regexDict["album"].match(imageURL):
				#well shoot. we're gonna try that again
				#self.setPictureURL()
				return
			if self.regexDict["gallery"].match(imageURL):
				#easy peasy
				self.imageURL = "http://i." + self.regexDict["gallery"].match(imageURL).group(2) + ".jpg"
				self.setPILImage()
		else:
			self.imageURL = imageURL
			#well, maybe it's an image
			self.setPILImage()
			
					
	def setPILImage(self):
		#this would be where we take self.imageURL, grab the data, and load an image file
		image = requests.get(self.imageURL)
		if "image" in image.headers['content-type']:
			self.im = Image.open(StringIO(image.content))
			#self.im.show()
			self.drawOnImage()
		else:
			print("not imgur gal or image and content type was not iamge. exiting")
	
	def drawOnImage(self):
		width,height = self.im.size
		font = ImageFont.truetype("Arial.ttf",48)
		self.getCommentString()
		draw = ImageDraw.Draw(self.im)
		strwidth,strheight = font.getsize(self.string)

		randWidth = random.randint(0,width/2)#,random.randint(width/2,width)
		#randWidth = randWidth[1] - randWidth[0]
		randHeight = random.randint(height/2,height-strheight)
		
		print("width {derp}".format(derp = height))
		

		draw.text((randWidth,randHeight),self.string,font=font)
		self.im.show()
	
	def getCommentString(self):
		sub = self.session.get("http://www.reddit.com/r/random").url#getting random subreddit
		print(sub)
		subreddit = re.match(r'http://www\.reddit\.com/r/(.*)',sub).group(1)
		
		time.sleep(2)
		article = self.session.get(sub+"/random.json")
		print(article.url)
		article = article.json
		child = article[1]['data']['children'][0]['data']['body']
		#print re.findall(r'.*?[\.?!]',child)#cool idea, but it gives even less context. ? and ! sentences have extremely contextual following sentences
		child = child.split(".")
		child.sort()
		sentence = child[-1]
		#sentence = child[random.randint(0,len(child)-1)].strip()
		print sentence
		self.string = sentence
		
		
q = quoteMaker()
#q.getCommentString()
q.setPictureUrl()
