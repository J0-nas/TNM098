import matplotlib.pyplot as plt

file = open("output.txt", 'r')

lines = []
for i, line in enumerate(file):
    #print(line)
    line = line.split(',')
    lines += [line]

#print(lines[0])
print("len0", len(lines[0]))
print("len2", len(lines[2]))
x = [ x for x in range(256)]
print("len x", len(x))
print("lines", len(lines))
plt.scatter(x, lines[0])
plt.axis([0,260,0,105])
plt.show()

plt.scatter(x, lines[1])
plt.axis([0,260,0,105])
plt.show()

plt.scatter(x, lines[2])
plt.axis([0,260,0,105])
plt.show()
