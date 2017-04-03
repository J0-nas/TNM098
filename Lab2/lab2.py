import matplotlib.pyplot as plt

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

plt.plot(getYPoints(lines), getXPoints(lines), 'bx')
plt.axis([0,1080,0,1920])
plt.show()

