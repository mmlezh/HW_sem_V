import numpy as np
from zone import Zone
import pylab as pl
import itertools as itools
from random import randint
from matplotlib import collections  as mc
from datetime import date
#############################################################	
# Проецирование на плоскости
def project(arr):
	Comp1 = []
	Comp2 = []
	for line in arr: # i = [[][]]
		line1 = []
		line2 = []
		for pt in line:
			pt1 = [pt[0], pt[1]]
			pt2 = [pt[2], pt[3]]
			line1.append(pt1)
			line2.append(pt2)
		Comp1.append(line1)
		Comp2.append(line2)

	return [np.array(Comp1), np.array(Comp2)]
#############################################################
# Считывание компонент
def getComps(dim, num_of_comps, file):
	line_comps = []
	begin = file.readline()
	bpt = [float(y) for y in begin.split()]
	for i in range(0, num_of_comps):
		line = []

		end = file.readline()
		ept = [float(y) for y in end.split()]

		line.append(bpt) # Добавили  
		line.append(ept)
		line_comps.append(line)

	return np.array(line_comps)

#############################################################	
# Матрица поворота
def RotMat(x1, x2, angle, dim):
	RotMat = np.zeros((dim, dim))

	for i in range(0, dim):
		for j in range(0, dim):
			if(i == j):
				RotMat[i][j] = 1
			if((i == x1) and (j == x1)):
				RotMat[i][j] = np.cos(angle)
			elif((i == x2) and (j ==x2)):
				RotMat[i][j] = np.cos(angle)
			elif((i == x1) and (j ==x2)):
				RotMat[i][j] = -np.sin(angle)
			elif((i == x2) and (j == x1)):
				RotMat[i][j] = np.sin(angle)
	return RotMat
#############################################################	
# Считает площадь
def Volume(Comps, dim, num_of_components):
	vects = []
	for i in range(0, num_of_components):
		# print(Comps[i])
		vects.append(Comps[i][1] - Comps[i][0])

	arr = list(itools.combinations(vects, dim))

	permut = np.array(arr)

	vol = 0;

	for i in permut:
		# print(i)
		# print(abs(np.linalg.det(i)))
		vol += abs(np.linalg.det(i))

	return vol

def VolZone(Cubes):
	Sum = 0
	for cube in Cubes:
		Sum += Volume(cube.Comps, 2, 2)
	return Sum 
#############################################################	
# Крутит кубик по вводным данным
def rotate(Comps, RotMat, num_of_components):

	RotComps = []

	vects = []

	bpt = Comps[0][0]
	# print(bpt)

	for i in range(0, num_of_components):
		vects.append(Comps[i][1] - Comps[i][0])

	vects = np.array(vects)
	# print(vects)

	for i in range(0, num_of_components):
		RotComps.append(np.dot(RotMat, vects[i]))

	line_comps = []
	for i in range(0, num_of_components):
		line = []
		ept = RotComps[i]
		line.append(bpt) # Добавили  
		line.append(ept)

		line_comps.append(line)

	return np.array(line_comps)

#############################################################	
# Случайный поворот кубика 
def randomRotate(Comps, dim, num_of_components):
	angles = []
	for i in range(0, 6):
		top = randint(1, 6)
		sub = randint(6, 24)
		angles.append(np.pi*top/sub)

	Mats = []
	
	Mats.append(RotMat(0 , 1, angles[0], dim))
	Mats.append(RotMat(2 , 3, angles[1], dim))
	Mats.append(RotMat(0 , 3, angles[2], dim))
	Mats.append(RotMat(1 , 2, angles[3], dim))
	Mats.append(RotMat(0 , 2, angles[4], dim))
	Mats.append(RotMat(1 , 3, angles[5], dim))


	for i in range(0, 6):
		Comps = rotate(Comps, Mats[i], num_of_components)

	# print(Comps)

	return Comps
#############################################################	
# Для иллюстраций: рисует ассоцированные
def AssosiatedCells(Zone1, Zone2):
	inds1 = [0, 1]
	inds2 = [2, 3]

	fig, (ax1, ax2)  = pl.subplots(ncols = 2, figsize=(12, 6))

	Zone1.plotZone(ax1, 'C1', True)
	Zone2.plotZone(ax2, 'C1', True)

	Comps1 = []
	Comps2 = []

	for i in inds1:
		Comps1.append(Zone1.Comps[i])

	for i in inds2:
		Comps2.append(Zone2.Comps[i])

	Cube1 = Zone(np.array(Comps1))
	Cube2 = Zone(np.array(Comps2))

	Cube1.plotZone(ax1, 'C0', False)
	Cube2.plotZone(ax2, 'C0', False)

	pl.show()
	today = date.today()
	fig.savefig('Pics/As-Cels-{}.png'.format(today),  dpi = 600)
	fig.savefig('Pics/As-Cels-{}.pdf'.format(today))
#############################################################	
# Для иллюстраций: рисует полное разбиение, результат работы алгоритма
def FullDissections(Zone1, Zone2, num, num_of_components, dim):
	fig, (ax1, ax2)  = pl.subplots(ncols = 2, figsize=(12, 6))
	Vol1 = Volume(Zone1.Comps, dim, num_of_components)
	DisZone1 = Zone1.getDissection(num)	
	
	Zone1.plotDis(ax1, num, 4)
	ax1.set_xlabel('Объем равен {}'.format(Vol1))

	Vol2 = Volume(Zone2.Comps, dim, num_of_components)
	DisZone2 = Zone2.getDissection(num)
	Zone2.plotDis(ax2, num, 4)

	ax2.set_xlabel('Объем равен {}'.format(Vol2))

	pl.show()
	today = date.today()
	fig.savefig('Pics/Full-Dissections-{}.png'.format(today),  dpi = 600)
	fig.savefig('Pics/Full-Dissections-{}.pdf'.format(today))

#############################################################	
# Основная Часть

#file = open('Quaternion_by_Prasolov.txt', 'r') # в exam вводятся координаты компонент
#file = open('example.txt', 'r') # в exam вводятся координаты компонент
file = open('input.txt', 'r') # в input вводятся координаты компонент

dim = int(file.readline()) # размерность пространства 
num_of_components = int(file.readline()) # кол-во компонент

arr = getComps(dim, num_of_components, file)

#arr = randomRotate(arr, dim, num_of_components) # случайный поворот

Comps = project(arr) # проецируем на (*,*,0,0) и (0,0,*,*)

Zone1 = Zone(Comps[0])
Zone2 = Zone(Comps[1])

#Cubes = Zone1.getDissection(0)

# Пошаговая иллюстрация доказательства:
fig1, (ax0, ax1)  = pl.subplots(ncols =2, figsize=(12, 6)) # холсты для иходных зонотопов
fig2, ax2 = pl.subplots(figsize=(6, 6)) # холст для первого шага разбиения Zone1
fig3, ax3 = pl.subplots(figsize=(6, 6)) # холст для второго шага разбиения Zone1
fig4, ax4 = pl.subplots(figsize=(6, 6)) # холст для третьего шага разбиения Zone1
fig5, ax5 = pl.subplots(figsize=(6, 6)) # холст для четвертого шага разбиения Zone1

Zone1.plotZone(ax0, 'C1', True) # рисуем Zone1
Zone2.plotZone(ax1, 'C1', True) # рисуем Zone2

Zone1.plotDis(ax2, 0, 1) # рисуем первый шаг разбиения
Zone1.plotDis(ax3, 0, 2) # рисуем второй шаг разбиения
Zone1.plotDis(ax4, 0, 3) # рисует третий шаг разбиения 
Zone1.plotDis(ax5, 0, 4) # рисуем четвертый шаг разбиения

FullDissections(Zone1, Zone2, 0, num_of_components, 2) # отрисовываем полное разбиение

pl.show()

# для сохраниения иллюстраций алгоритма
# today = date.today()
# fig1.savefig('Pics/Step1-{}.png'.format(today),  dpi = 600)
# fig1.savefig('Pics/Step1-{}.pdf'.format(today))
# fig2.savefig('Pics/Step2-{}.png'.format(today),  dpi = 600)
# fig2.savefig('Pics/Step2-{}.pdf'.format(today))
# fig3.savefig('Pics/Step3-{}.png'.format(today),  dpi = 600)
# fig3.savefig('Pics/Step3-{}.pdf'.format(today))
# fig4.savefig('Pics/Step4-{}.png'.format(today),  dpi = 600)
# fig4.savefig('Pics/Step4-{}.pdf'.format(today))
# fig5.savefig('Pics/Step5-{}.png'.format(today),  dpi = 600)
# fig5.savefig('Pics/Step5-{}.pdf'.format(today))
