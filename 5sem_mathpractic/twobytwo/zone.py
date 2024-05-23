import numpy as np
import pylab as pl
from matplotlib import collections  as mc
from scipy.spatial import ConvexHull
from datetime import date

class Zone:
	def __init__(self, Comps):
		self.Comps = Comps
		
		Skeleton = constructSkeleton(Comps) # проверить
		
		self.Edges = Skeleton[0]
		self.Dots = Skeleton[1]

		self.Outline = []
		self.BorDots = []

		self.Dissec = []

		points = np.array(self.Dots)
		hull = ConvexHull(points)

		x = points[hull.vertices, 0]
		y = points[hull.vertices, 1]
		for i in range(0, len(x)):
			pt = [x[i], y[i]]
			self.BorDots.append(pt)

		for i in range(0, len(self.BorDots)):
			line = [self.BorDots[i], self.BorDots[(i+1)%len(self.BorDots)]]
			self.Outline.append(line)
		# line = [self.BorDots[len(self.BorDots)-1], self.BorDots[0]]
		# self.Outline.append(line)

	def plotZone(self, ax, clr, mode):
		draw = []
		CompDots = getAllDots(self.Comps.tolist())

		edges = mc.LineCollection(self.Edges, linewidths=1, color = clr, linestyle = 'dotted')

		cmps = mc.LineCollection(self.Comps, color='C3', linewidths=2)

		border = mc.LineCollection(self.Outline, linewidths=2, color = clr)
	
		draw.append(ax.set_title('Построенный зонотоп'))
		draw.append(ax.add_collection(edges))
		draw.append(ax.add_collection(border))
		draw.append(ax.add_collection(cmps))
		for i in self.Dots:
			draw.append(ax.plot(i[0], i[1], 'o', mec = 'C1' ,color='w', lw=1, markersize = 3))
	
		for i in CompDots:
			draw.append(ax.plot(i[0], i[1], '.', color=clr))
		for i in self.BorDots:
			draw.append(ax.plot(i[0], i[1], '.' ,color=clr))
		if mode:
			for i in range(0, len(self.Comps)):
				label ="e{}".format(i)
				draw.append(ax.annotate(label, self.Comps[i][1]))
		draw.append(ax.autoscale())
		return tuple(draw)

	def plotComps(self, ax):
		draw = []
		CompDots = getAllDots(self.Comps.tolist())

		edges = mc.LineCollection(self.Edges, linewidths=1, color = 'w', linestyle = 'dotted')
	
		cmps = mc.LineCollection(self.Comps, color='C3', linewidths=2)
	
		border = mc.LineCollection(self.Outline, linewidths=1, color = 'w')
	
		draw.append(ax.set_title('Компоненты зонотопа'))
		draw.append(ax.add_collection(edges))
		draw.append(ax.add_collection(border))
		draw.append(ax.add_collection(cmps))
		for i in CompDots:
			draw.append(ax.plot(i[0], i[1], '.', color='C3'))
		draw.append(ax.autoscale())
		return tuple(draw)

	def getBk(self, num):
		k_comp = np.array(self.Comps[num])

		B_k = [] 

		# print(len(self.Outline))
		for line in self.Outline:
			# print('Line = {}'.format(np.array(line)))
			dirLine = np.array([[0, 0], [line[1][0] - line[0][0],line[1][1] - line[0][1]]])
			if is_it_Ok(dirLine[1], k_comp[1]):
				B_k.append(line)

		return B_k	

	def getCube(self, num):
		CompsCube = []

		for ind in range(0, len(self.Comps)):
			if ind != num:
				CompsCube.append(self.Comps[ind])

		CubeZone = Zone(np.array(CompsCube))
		
		return CubeZone

	def getDissection(self, num):
		Cubes = []

		inds = [0, 1, 2, 3]

		Zk = self

		for i in range(0, len(self.Comps)-2):
			B_k = Zk.getBk(num)
			C_k = [] # монжество кубических клеток

			for edge in B_k:
				comp = [[0, 0], [edge[1][0] - edge[0][0],edge[1][1] - edge[0][1]]]
				# print('comp = {}'.format(np.array(comp)))
				# print('Zk.Comps[num] = {}'.format(np.array(np.array(Zk.Comps[num]))))
				CubeCell = Zone([np.array(comp), np.array(Zk.Comps[num])])
				Cubes.append(CubeCell)

			Zk = Zk.getCube(num)
			newinds = []
			for i in inds:
				if not i == num:
					newinds.append(i)
			inds = newinds
			num = inds[0]

		Cubes.append(Zk)
		return Cubes


	def plotDis(self, ax, num, step):
		draw = []

		if(step == 1):
			CompDots = []
			CompDots = getAllDots(self.Comps.tolist())
			
			CubeZone = self.getCube(num)

			cmps = mc.LineCollection(self.Comps, color='C3', linewidths=2, linestyle = '--')
			border = mc.LineCollection(self.Outline, linewidths=1, color = 'C1', linestyle='--')

			draw.append(ax.set_title("Первый шаг разбиения"))
			draw.append(ax.add_collection(border))

			hullCube = mc.LineCollection(CubeZone.Outline, linewidths=2, color = 'C1', linestyle = 'solid')
			comp_k = mc.LineCollection([self.Comps[num]], linewidths=2, color = 'C3', linestyle = 'solid')

			draw.append(ax.add_collection(hullCube))
	
			draw.append(ax.add_collection(cmps))

			draw.append(ax.add_collection(comp_k))

			for i in CompDots:
				draw.append(ax.plot(i[0], i[1], '.', color='C3'))
			for i in self.BorDots:
				draw.append(ax.plot(i[0], i[1], '.' ,color='C3'))
			for i in range(0, len(self.Comps)):
				label ="e{}".format(i)
				draw.append(ax.annotate(label, self.Comps[i][1]))
			draw.append(ax.autoscale())
		
		elif(step == 2):
			CompDots = []
			CompDots = getAllDots(self.Comps.tolist())

			CubeZone = self.getCube(num)

			B_k = self.getBk(num)
			C_k = [] # монжество кубических клеток

			cmps = mc.LineCollection(self.Comps, color='C3', linewidths=2, linestyle = '--')
			border = mc.LineCollection(self.Outline, linewidths=1, color = 'C1', linestyle='--')

			draw.append(ax.set_title("Второй шаг разбиения"))
			draw.append(ax.add_collection(border))

			hullCube = mc.LineCollection(CubeZone.Outline, linewidths=2, color = 'C1', linestyle = 'solid')
			comp_k = mc.LineCollection([self.Comps[num]], linewidths=2, color = 'C3', linestyle = 'solid')
			b_k = mc.LineCollection(B_k, linewidths=2, color = 'C1', linestyle = 'solid')

			draw.append(ax.add_collection(hullCube))
			draw.append(ax.add_collection(cmps))
			draw.append(ax.add_collection(comp_k))
			draw.append(ax.add_collection(b_k))

			for i in CompDots:
				draw.append(ax.plot(i[0], i[1], '.', color='C3'))	
			for i in self.BorDots:
				draw.append(ax.plot(i[0], i[1], '.' ,color='C3'))
			for i in range(0, len(self.Comps)):
				label ="e{}".format(i)
				draw.append(ax.annotate(label, self.Comps[i][1]))
			draw.append(ax.autoscale())

		elif(step == 3):
			CompDots = []
			CompDots = getAllDots(self.Comps.tolist())

			CubeZone = self.getCube(num)

			B_k = self.getBk(num)
			C_k = [] # монжество кубических клеток

			cmps = mc.LineCollection(self.Comps, color='C3', linewidths=2, linestyle = '--')
			border = mc.LineCollection(self.Outline, linewidths=2, color = 'C1', linestyle='--')

			draw.append(ax.set_title("Третий шаг разбиения"))
			# draw.append(ax.set_title("Разбиение"))
			draw.append(ax.add_collection(border))

			hullCube = mc.LineCollection(CubeZone.Outline, linewidths=2, color = 'C1', linestyle = 'solid')
			comp_k = mc.LineCollection([self.Comps[num]], linewidths=2, color = 'C3', linestyle = 'solid')
			b_k = mc.LineCollection(B_k, linewidths=2, color = 'C1', linestyle = 'solid')


			draw.append(ax.add_collection(hullCube))
			draw.append(ax.add_collection(comp_k))
	
			for edge in B_k:
				Cube = mnkSub(np.array(edge), np.array(self.Comps[num]))
				cube = mc.LineCollection(Cube, linewidths=2, color = 'C1', linestyle = 'solid')
				draw.append(ax.add_collection(cube))
				
			draw.append(ax.add_collection(cmps))

			for i in CompDots:
				draw.append(ax.plot(i[0], i[1], '.', color='C3'))	
			for i in self.BorDots:
				draw.append(ax.plot(i[0], i[1], '.' ,color='C3'))
			for i in range(0, len(self.Comps)):
				label ="e{}".format(i)
				draw.append(ax.annotate(label, self.Comps[i][1]))
			draw.append(ax.autoscale())

		elif(step == 4):
			Cube = self  

			inds = [0, 1, 2, 3]

			draw.append(ax.set_title("Разбиение"))
			for i in range(0, len(self.Comps)-2):
				CompDots = []
				CompDots = getAllDots(Cube.Comps.tolist())

				CubeZone = Cube.getCube(num)

				B_k = Cube.getBk(num)
				C_k = [] # монжество кубических клеток

				cmps = mc.LineCollection(Cube.Comps, color='C3', linewidths=2, linestyle = '--')
				border = mc.LineCollection(Cube.Outline, linewidths=2, color = 'C1', linestyle='--')

				draw.append(ax.add_collection(border))

				hullCube = mc.LineCollection(CubeZone.Outline, linewidths=2, color = 'C1', linestyle = 'solid')
				comp_k = mc.LineCollection([Cube.Comps[num]], linewidths=2, color = 'C3', linestyle = 'solid')
				b_k = mc.LineCollection(B_k, linewidths=2, color = 'C1', linestyle = 'solid')

				draw.append(ax.add_collection(hullCube))
				draw.append(ax.add_collection(comp_k))
			
				for edge in B_k:
					CubeCell = mnkSub(np.array(edge), np.array(Cube.Comps[num]))
					cubecell = mc.LineCollection(CubeCell, linewidths=2, color = 'C1', linestyle = 'solid')
					draw.append(ax.add_collection(cubecell))
				
				draw.append(ax.add_collection(cmps))
				for i in CompDots:
					draw.append(ax.plot(i[0], i[1], '.', color='C3'))	
				for i in Cube.BorDots:
					draw.append(ax.plot(i[0], i[1], '.' ,color='C3'))

				Cube = Cube.getCube(num) 
				newinds = []
				for i in inds:
					if not i == num:
						newinds.append(i)
				inds = newinds
				num = inds[0]

			for i in range(0, len(self.Comps)):
				label ="e{}".format(i)
				draw.append(ax.annotate(label, self.Comps[i][1]))
			draw.append(ax.autoscale())

		return tuple(draw)

	def getAll(self):
		print('Comps')
		print(self.Comps)
		print('Edges')
		print(self.Edges)
		print('Dots')
		print(self.Dots)
		print('Outline')
		print(self.Outline)
		print('BorDots')
		print(self.BorDots)
		print(self.Dissec)

#############################################################
def mnkSum(Zon1, Zon2):
	Sum = []
	if not Zon1.tolist():
		return Zon2.tolist()
	if not Zon2.tolist():
		return Zon1.tolist()

	for it in Zon1: # в линии
		for ind in range(0,2): # берем точки на которые будем сдвигать
			for jt in Zon2: # берем линии которые будем сдвигать
				line = [] # сдвигаем по компонетно
				# begin = ptSum(it[ind], jt[0]) 
				# end = ptSum(it[ind], jt[1])
				begin = it[ind] + jt[0]
				end = it[ind] + jt[1]
				line.append(begin)
				line.append(end)
				# if not line in Sum:
				Sum.append(line)

	for it in Zon2: # в линии
		for ind in range(0,2): # берем точки на которые будем сдвигать
			for jt in Zon1: # берем линии которые будем сдвигать
				line = []  # сдвигаем по компонетно
				# begin = ptSum(it[ind], jt[0])
				# end = ptSum(it[ind], jt[1])
				begin = it[ind] + jt[0]
				end = it[ind] + jt[1]
				line.append(begin)
				line.append(end)
				# if not line in Sum:
				Sum.append(line)	

	lines = np.array(Sum)
	result = lines.tolist()
	Sum = []

	for line in result:
		if not line in Sum:
			Sum.append(line) 			

	return Sum
#############################################################
def mnkSub(edge, k_comp):
	Sub = []
	# print('edge:')
	# print(np.array(edge))
	# print('k_comp:')
	# print(np.array(k_comp))
	for pt in k_comp:
		line = []
		for qt in edge:
			# print('{} - {} = '.format(qt, pt))
			point = qt - pt # qt - pt
			# print(point)
			line.append(point)
		# print('line = {}'.format(np.array(line)))
		Sub.append(line)

	for pt in edge:
		line = []
		for qt in k_comp:
			# print('{} - {} = '.format(qt, pt))
			point = pt- qt
			# print(point)
			line.append(point)
		# print('line = {}'.format(np.array(line)))
		Sub.append(line)
	return Sub 
#############################################################
def getAllDots(Edges):
	Dots = []
	for i in Edges:
		if not i[0] in Dots:
			Dots.append(i[0])
		if not i[1] in Dots:
			Dots.append(i[1])
	return Dots
#############################################################
def constructSkeleton(Comps):
	strComps = [] # составили множетво с которым будем работать
	for i in Comps: 
		Comp = [] 
		Comp.append(i) #[[btp, ept1]]
		strComps.append(Comp) #[, [[btp, ept1]] ]

	Edges = []

	for i in range(0, len(strComps)):
		Edges = mnkSum(np.array(strComps[i]), np.array(Edges)) 

	Dots = getAllDots(Edges)

	return [np.array(Edges), np.array(Dots)]
#############################################################
def is_it_Ok(a, b):
	n = np.array([a[1], -a[0]])
	k = np.array(b)
	# print('a = {}'.format(a))
	# print('b = {}'.format(b))
	# print('n = {}'.format(n))
	# print('k = {}'.format(k))
	# print('<n, k> = {}'.format(np.dot(n, k)))

	if np.dot(n, k) > 1e-12:
		return True
	else: 
		return False
#############################################################