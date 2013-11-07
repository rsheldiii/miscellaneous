import csv,time,random

class Life:
	def __init__(self):
		self.board = {}
		self.liveCells = []
		self.iteration = 0
		self.position = (0,0)
		self.height = 4
		self.width = 4
		self.duration = .30
		self.cartesianCollection = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
	
	def loadCSV(self,f,setParams = True):
		y = 0
		length = 0
		with open(f, newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in reader:
				width = max(len(row),width)
				for x in range(0,len(row)):
					if row[x] == '1':
						self.board[(x,y)] = 1
						self.liveCells.append((x,y))
				y += 1
		if setParams:
			self.width = width
			self.height = y
			
	def loadRandom(self,width,height,probability=0.5):
		self.clear()
		for y in range(0,height):
			for x in range(0,width):
				if random.random() < probability:
					self.board[(x,y)] = 1
					self.liveCells.append((x,y))
		self.width,self.height = width,height
					
	def start(self,iterations):
		self.pr()
		self.time = time.time()
		while iterations == 0 or self.iteration < iterations:
			self.run()
			self.pr()
			
			dur = self.duration - (time.time()-self.time)
			if dur > 0: time.sleep(dur)
			
			self.time = time.time()
					
	def getCell(self,key):
		return self.board.get(key,0)#returns 0 if cell does not exist
	
	def findNeighbors(self,cell):
		return [tuple(map(sum,zip(modifier,cell))) for modifier in self.cartesianCollection]
	
	def cellSum(self,cells):
		return sum([self.getCell(x) for x in cells])
			
	def run(self):
		self.iteration += 1
		newLiveCells = []
		neighbors = set()
		for cell in self.liveCells:
			cellNeighbors = self.findNeighbors(cell)
			if self.cellSum(cellNeighbors) in (2,3):
				newLiveCells.append(cell)
			neighbors |= set([x for x in cellNeighbors if self.getCell(x) == 0])
		
		for cell in neighbors:
			if self.cellSum(self.findNeighbors(cell)) == 3:
				newLiveCells.append(cell)
		
		self.clear()
		for cell in newLiveCells:
			self.board[cell] = 1
		self.liveCells = newLiveCells
		
	def pr(self):
		for y in range(self.position[1],self.height):
			for x in range(self.position[0],self.width):
				if self.getCell((x,y)) == 1:
					print("\u25A1",end='')
				else:
					print("\u25A0",end='')
			print()
		print("-"*self.width)
	
	def clear(self):
		self.board = {}
		self.liveCells = []
			
a = Life()
a.loadRandom(80,80,0.5)
a.start(70)# your code goes here
