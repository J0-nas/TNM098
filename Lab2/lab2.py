import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from mpl_toolkits.mplot3d import Axes3D


file = open("EyeTrack-raw.tsv", 'r')

lines = []
for i, line in enumerate(file):
    if i != 0:
        lines += [line.split('\t')]

lines = list(map( lambda x: x[:6], lines))
lines = list(map( lambda x: list(map( lambda y: int(y), x)), lines))
#print(lines)

def getXPoints(lines):
    x_points = list(map( lambda x: x[4], lines))
    return x_points

def getYPoints(lines):
    y_points = list(map( lambda x: x[5], lines))
    return y_points

def getMaxDuration(lines):
    dur = list(map( lambda x: (x[2], x[1]), lines))
    return max(dur)

def getTime(lines):
    return list(map( lambda x: x[2], lines))

m = getMaxDuration(lines)
print(m[0])
times = getTime(lines)
sizes = list(map( lambda x: (x/m[0])*500, times))

x_p = getXPoints(lines)
y_p = getYPoints(lines)
print("x_max", max(x_p))

#print(getMaxDuration(lines))

#plt.plot(getYPoints(lines), getXPoints(lines), 'bx')

plt.scatter(x_p, y_p, s=sizes, alpha=0.3)
plt.axis([0,1920,0,1080])
plt.show()
'''
plt.plot(x_p, y_p, 'bx')
plt.axis([0,1920,0,1080])
plt.show
'''

x_y = np.array( list( map(lambda x: [x[0], x[1]], zip(x_p, y_p)) ))
Agg = AgglomerativeClustering(n_clusters=20)
Agg.fit(x_y)
labs = Agg.labels_
#print(labs)

cm = plt.get_cmap('Vega20')
print(type(cm))
colorList = [cm.colors[i] for i in labs]


plt.scatter(x_p, y_p, s=sizes, alpha=0.3, c=colorList)
plt.axis([0,1920,0,1080])
plt.show()

def expandedTime(lines):
    res = []
    for line in lines:
        t_in = line[0]
        t_out = t_in + line[2]
        res += [[line[4], line[5], t_in]]
        res += [[line[4], line[5], t_out]]
    return res

x_y_z = expandedTime(lines)
x = np.array( list ( map ( lambda x: x[0], x_y_z)))
y = np.array( list ( map ( lambda x: x[1], x_y_z)))
z = np.array( list ( map ( lambda x: x[2], x_y_z)))

cm = plt.get_cmap('RdYlBu')
fig = plt.figure()
ax = fig.gca(projection='3d')

length = len(x)
c = [cm(x/length) for x in range(length)]

'''
ax.plot(x, y, z, label='Eye movement')
ax.legend()
plt.show()
'''

ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, label='Eye movement', c=c)
ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Time')
ax.set_xlim3d(0, 1920)
ax.set_ylim3d(0,1080)
ax.set_zlim3d(0,300000)
plt.show()
