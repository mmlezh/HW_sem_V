import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import itertools

volume_1d=[0]*4
volume_3d=[0]*4
v=[0]*4
#список из элементов симметрической группы S_n 
def generate_permutations(n):
    elements = list(range(1, n+1))
    permutations = list(itertools.permutations(elements))
    return permutations

#нарисовать отрезок, c-цвет, a-прозрачность
def draw_segment(point1, point2, c='blue', a=1, z=0):
    ax1.plot([point1[0], point2[0]], [point1[1], point2[1]], [point1[2], point2[2]], color=c, alpha=a, zorder=z)

#нарисовать точку, c-цвет, a-прозрачность
def draw_point(point, c='black', a=0.5):
    ax1.scatter(point[0], point[1], point[2], color=c, alpha=a)

#скалаярное произведение
def scalar_product(vector1, vector2):
    return  sum(x * y for x, y in zip(vector1, vector2))

#сумма всех векторов из массива vectors
def vector_addition(vectors):
    n = len(vectors[0]) 
    result = [0] * n 
    for vector in vectors:
        for i in range(n):
            result[i] += vector[i]
    return result

#координаты вектора vector в базисе basis
def coordinates(basis, vector):
    return [np.dot(vector, basis[0]),np.dot(vector, basis[1]),np.dot(vector, basis[2])]

#нарисовать параллелограмм
def draw_parallelogramm(o, v, c='blue', a=0.75):
    x = [o[0], o[0]+v[0][0], o[0]+v[0][0]+v[1][0], o[0]+v[1][0]]
    y = [o[1], o[1]+v[0][1], o[1]+v[0][1]+v[1][1], o[1]+v[1][1]]
    z = [o[2],o[2]+ v[0][2], o[2]+v[0][2]+v[1][2], o[2]+v[1][2]]
    vertices = [list(zip(x,y,z))]
    poly = Poly3DCollection(vertices, color=c, alpha=a)
    ax1.add_collection3d(poly)

#процесс ортогонализации системы векторов vectors
def gram_schmidt(vectors):
    basis = []
    for v in vectors:
        for b in basis:
            v = v - np.dot(v, b) / np.dot(b, b) * b
        if np.linalg.norm(v) > 1e-10:
            basis.append(v / np.linalg.norm(v))
    return basis

#нарисовать зонотоп в трехмерном пространстве с центром в origin и порождающими generators(это координаты x_i концов порождающих [-x_i, x_i])
def draw_zonotope(origin, generators, r, n, c1='blue', c2='blue', a=0.1):
    #print('draw_zonotope:')
    #print('origin', origin)
    #print('generators', generators)

    shift=vector_addition(generators)
    start=origin-shift
    '''
    print("shift")
    print(shift)
    print("start")
    print(start)
    '''
    for permutation in generate_permutations(r):
        path=[]
        for j in range(0, r):
            if j==0:
                path.append(start+2*generators[permutation[j]-1])
                draw_segment(start, path[j], c1, a)
            else:
                path.append(2*generators[permutation[j]-1]+path[j-1])
                draw_segment(path[j-1], path[j], c2 , a)
        for v in path:
            ax1.scatter(v[0], v[1], v[2], color='black', alpha=a, s=5)

#проекция зонотопа на плоскость ортогональную вектору generators[0](можно поменять в строке 36)
def zonotope_projection(origin, generators, r, n):
    vector=generators[0]
    print('zonotope_projection')
    ort=np.array(vector/np.linalg.norm(vector))
    print('ort',ort)
    draw_point(ort+origin, 'white')
    draw_segment(origin, origin+ort, 'red')
    new_generators=[]
    for i in range(0, r):
        new_generators.append(generators[i] - np.dot(generators[i], ort)* ort )
        draw_segment(origin, new_generators[i]+origin, 'grey')
        draw_point(new_generators[i]+origin, 'white')
        
    draw_zonotope(origin, new_generators, r, np.linalg.matrix_rank(new_generators), 'pink', 'orange', 0.5)
    return new_generators

#построение разбиение зонотопа с r=4 в трехмерном пространстве 
def zonotope_tiling(origin, generators, r, n, k=1):
    if k==-2:
        draw_zonotope(origin, generators, r, n, 'blue', 'blue',  1)
        return
    #print('zonotope_tiling')
    #print('origin', origin)
    #print('generators', generators)
    fixed=generators[0]
    generators1=generators[1:]
    draw_zonotope(origin-fixed, generators1, r-1, n, 'black', 'black',  1)
   
    shift=vector_addition(generators)
    start=origin-shift
    if k>=-1:
        draw_parallelogramm(start, [2*generators1[0], 2*generators1[1]], 'blue')
        draw_parallelogramm(start, [2*generators1[1], 2*generators1[2]], 'blue')
        draw_parallelogramm(start, [2*generators1[0], 2*generators1[2]], 'blue') 
    
    for permutation in generate_permutations(r):
        flag=0
        path=[]
        for j in range(0, r):
            if j==0:
                path.append(start+2*generators[permutation[j]-1])
                if flag==1:
                    draw_segment(start, path[j], (0.146,0.110,0.174), 1)
                
            else:
                path.append(2*generators[permutation[j]-1]+path[j-1])
                if flag==1:
                    draw_segment(path[j-1], path[j], (0.146,0.110,0.174), 1)
                if permutation[j]-1==0 and j>=1:
                    flag=1
                    if j+2<r:
                        if k>=-1:
                            draw_parallelogramm(path[j], [2*generators[permutation[j+1]-1], 2*generators[permutation[j+2]-1]], 'blue', 0.1)
                            draw_parallelogramm(path[j]-2*fixed, [2*generators[permutation[j+1]-1], 2*generators[permutation[j+2]-1]], 'blue', 0.1)
                    draw_segment(path[j-1], path[j], 'pink' , 1)

    #volume_3d[0]=np.dot(np.cross(generators1[0], generators1[1]), generators1[2])
    #volume_3d[0]=np.dot(np.cross(2*generators1[0], 2*generators1[1]), 2*generators1[2])

    if k>=0:
        for i in range(0, r-1):
            a=np.delete(generators1, i, axis=0)[0]
            b=np.delete(generators1, i, axis=0)[1]
            draw_parallelogramm(start+2*generators1[i], [2*generators[0], 2*a], color[i+1])
            draw_parallelogramm(start+2*generators1[i], [2*b, 2*generators[0]], color[i+1])
            #draw_parallelogramm(start+2*generators1[i], [2*a, 2*b], color[i+1])
            draw_parallelogramm(start+2*generators[0]+2*generators1[i], [2*a, 2*b], color[i+1])
            #print (a, b, generators[0])
            #volume_3d[i+1]=np.dot(np.cross(a, b), generators[0])
            #volume_3d[i+1]=np.dot(np.cross(2*a, 2*b), 2*generators[0])
    #print(generators)
    for i in range(0, r):
        a=np.delete(generators, i, axis=0)[0]
        b=np.delete(generators, i, axis=0)[1]
        c=np.delete(generators, i, axis=0)[2]
        volume_3d[i]=abs(np.linalg.det([2*a, 2*b, 2*c]))

#для данного базиса basis 3-мерного подпространства 4-мерного пространства строится проекция 4-мерного куба 
def projections_of_4_dimensional_cube(basis, generators, r, n, l=1):
    for vector in basis:
        vector=vector/np.linalg.norm(vector)

    print('projections_of_4_dimensional_cube')
    print('generators\n', generators)
    print('basis\n', basis)
    ort_basis = gram_schmidt(basis)
    #print('ort_basis', ort_basis)

    _, _, V = np.linalg.svd(ort_basis)
    ort_vector = V[-1]
    ort_vector=ort_vector/np.linalg.norm(ort_vector)
    #print('ort_v', ort_vector)
    projections=[]
    for generator in generators:
        projections.append(generator - np.dot(generator, ort_vector)*ort_vector)
    projections=np.array(projections)
    #print('projections of generators', projections)

    generators_3=[]
    for projection in projections:
        generators_3.append(np.array(coordinates(ort_basis, projection)))

    generators_3=np.array(generators_3)
    print('projections of generators with coordinates in basis of 3-dimensional subspace\n', generators_3)
    origin_3=np.array([0, 0, 0])
    b=[]
    k=0
    for i in range(0, r):
        if np.linalg.norm(generators_3[i])>1e-10:
            b.append(generators_3[i])
            k+=1
    '''if k!=r:
        draw_zonotope(origin_3, b, k, n, 'blue', 'blue',1)
        return
    '''
    test=generators_3[0]
    for i in range(0, r):
        if scalar_product(test, generators_3[i])<0:
            generators_3[i]=-generators_3[i]
   
    first=generators_3[0]
    indexes=[0, 1, 2, 3]
    color=['blue', 'green', 'red', 'yellow']
    for i in range(0, r):
        a=np.delete(indexes, i, axis=0)[0]
        b=np.delete(indexes, i, axis=0)[1]
        c=np.delete(indexes, i, axis=0)[2]
        n=[]
        if np.linalg.norm(generators_3[i])>1e-5:
            ort=np.array(generators_3[i]/np.linalg.norm(generators_3[i]))
        n.append(generators_3[a]-scalar_product(ort, generators_3[a])*ort)
        n.append(generators_3[b]-scalar_product(ort, generators_3[b])*ort)
        n.append(generators_3[c]-scalar_product(ort, generators_3[c])*ort)

        if (scalar_product(n[0], n[1])<0 and scalar_product(n[0], n[2])<0) or (scalar_product(n[1], n[0])<0 and scalar_product(n[1], n[2])<0) or (scalar_product(n[2], n[1])<0 and scalar_product(n[2], n[0])<0):
            first=generators_3[i]
            generators_3=[first, generators_3[a], generators_3[b], generators_3[c]]

    #print('reoganized generators_3', generators_3)
    
        
    #рисуем порождающие и центр зонотопа
    if l<=-1:
        for i in range(0, r):
                draw_segment(origin_3-generators_3[i], origin_3+generators_3[i], 'red', 1, 2)
        draw_point(origin_3, 'red')

    draw_zonotope(origin_3, generators_3, r, n)
    zonotope_tiling(origin_3, generators_3, r, n, l)
    if l<1:
        return

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, projection='3d')        
    generators_1=[]
    #print('ort_vector', ort_vector)
    for i in range(0, r):
        generators_1.append(np.dot(generators[i], ort_vector))
        #print(np.dot(generators[i], ort_vector))
    generators_1=np.array(generators_1)
    print('projections of generators with coordinates in basis of 1-dimensional subspace\n', generators_1)
    
    test=generators_1[0]
    for i in range(0, r):
        if test*generators_1[i]<0:
            generators_1[i]=-generators_1[i]
    origin=0
    shift=generators_1[0]+generators_1[1]+generators_1[2]+generators_1[3]
    start=origin-shift
    #print(start)
    path=start
    for i in range(0, r):
        p=path
        ax2.scatter(0, 0, path, color='black', alpha=1, s=5)
        path+=2*generators_1[i]
        ax2.scatter(0, 0, path, color='black', alpha=1, s=5)
        ax2.plot([0, 0], [0, 0], [p, path], color=color[i], alpha=1, zorder=2)
        volume_1d[i]=2*generators_1[i]

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
color=['blue', 'green', 'red', 'yellow']

#тут закомментировано создание произвольного зонотопа с порождающими generators и его разбиение
'''
#generators = np.array([ np.array([1, 1, 1]), np.array([0, 0, 1]), np.array([0, 1, 0]),  np.array([1, 0, 0])])
#generators = np.array([  np.array([0, 0, 1]), np.array([1, 1, 1]),np.array([0, 1, 0]),  np.array([1, 0, 0])])

#порождающиe (координаты x_i концов порождающих [-x_i, x_i])
generators = np.array([ np.array([-3, 2, 0]),  np.array([3, 5, 3]), np.array([0, 1, -3]),  np.array([1, -1, 0])])
#начало координат (центр зонотопа)
origin = np.array([0, 0, 0])

r=len(generators)
n=np.linalg.matrix_rank(generators)
print('r=', r)
print('n=', n)
print('origin', origin)
print('generators', generators)

for i in range(0, r):
    test=generators[0]
    if scalar_product(test, generators[i])<0:
        generators[i]=-generators[i]

first=generators[0]
indexes=[0, 1, 2, 3]

for i in range(0, r):
    a=np.delete(indexes, i, axis=0)[0]
    b=np.delete(indexes, i, axis=0)[1]
    c=np.delete(indexes, i, axis=0)[2]
    n=[]
    ort=np.array(generators[i]/np.linalg.norm(generators[i]))
    n.append(generators[a]-scalar_product(ort, generators[a])*ort)
    n.append(generators[b]-scalar_product(ort, generators[b])*ort)
    n.append(generators[c]-scalar_product(ort, generators[c])*ort)

    if (scalar_product(n[0], n[1])<0 and scalar_product(n[0], n[2])<0) or (scalar_product(n[1], n[0])<0 and scalar_product(n[1], n[2])<0) or (scalar_product(n[2], n[1])<0 and scalar_product(n[2], n[0])<0):
        first=generators[i]
        generators=[first, generators[a], generators[b], generators[c]]

print('reoganized generators', generators)

#рисуем зонотоп с центром в origin и порождающими generators(это координаты x_i концов порождающих [-x_i, x_i])
draw_zonotope(origin, generators, r, n, 'blue', 'blue',  0.5) 

#рисуем проекцию зонотопа на плоскость ортогональную первой порождающей(то есть ортогональную [-x_0, x_0])

#zonotope_projection(origin, generators, r, n) 

#рисуем разбиение зонотопа, последний параметр (здесь он равен 1) можно поменять на 0
#и получить промежуточный шаг для иллюстрации доказательства теоремы о разбиении зонотопа

zonotope_tiling(origin, generators, r, n, 1)
'''

#порождающие 4 мерного куба с центром в (0, 0, 0, 0) 
#cube =  np.array([ np.array([0, 0, 0, 1]),  np.array([0, 0, 1, 0]), np.array([0, 1, 0, 0]),  np.array([1, 0, 0, 0])])
cube =  np.array([ np.array([0, 0, 0, 0.5]),  np.array([0, 0, 0.5, 0]), np.array([0, 0.5, 0, 0]),  np.array([0.5, 0, 0, 0])])

#базис 3-мерного подпространства в 4-мерном пространстве

#basis = np.array([ np.array([1, -1, 0, 0]),  np.array([0, 1, -1, 0]), np.array([0, 0, 1, -1])])
basis = np.array([ np.array([0, 0, 1, 2]),  np.array([0, 2, 3, 0]), np.array([3, 4, 0, 0])])
if np.linalg.matrix_rank(basis)<3:
    print('векторы не линейно независимы и не задают 3-мерного подпространства')
r=4
n=3

#проекции 4-мерного куба на ортогональные 3-мерное и 1-мерное продпространства
#если последний параметр равен -2, то проекция на 3-мерное подпространство просто рисуется
#если он равен -1, то получается иллюстрация для доказательства теоремы о разбиении зонотопа
#если он равен 0, то выводится разбиение проекции на 3-мерное подпространство
#если он равен 1, то выводится разбиение проекции на 3-мерное подпространство и разбиение проекции на ортогональное 1-мерное подпространство
projections_of_4_dimensional_cube(basis, cube, r, n, 1)

print('объемы соответствующих клеток ассоциированных зонотопов')
print('объемы трехмерных клеток')
print(volume_3d)
print('объемы одномерных клеток')
print(volume_1d)

ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')

ax1.axis("equal")
ax1.grid(False)
plt.show()