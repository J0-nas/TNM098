import regex as re
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN


f = open("CoinToss.txt", "r")
lines = []
for line in f:
    lines += [line]

print(len(lines[1]), "\n")

def subseq_1_freq(line):
    # \n at the end
    total_1 = len(line) -1
    _0 = len(re.findall(r'0', line)) / total_1
    _1 = len(re.findall(r'1', line)) / total_1

    return (_0, _1)

def subseq_2_freq(line):
    #total number or pairs
    total_2 = len(line) - 2 -1

    _00 = len(re.findall(r'00', line, overlapped=True)) / total_2
    _01 = len(re.findall(r'01', line, overlapped=True)) / total_2
    _10 = len(re.findall(r'10', line, overlapped=True)) / total_2
    _11 = len(re.findall(r'11', line, overlapped=True)) / total_2

    return (_00, _01, _10, _11)

def subseq_3_freq(line):
    #because \n at the end
    total_3 = len(line) - 3 -1

    _000 = len(re.findall(r'000', line, overlapped=True)) / total_3
    _001 = len(re.findall(r'001', line, overlapped=True)) / total_3
    _010 = len(re.findall(r'010', line, overlapped=True)) / total_3
    _011 = len(re.findall(r'011', line, overlapped=True)) / total_3
    _100 = len(re.findall(r'100', line, overlapped=True)) / total_3
    _101 = len(re.findall(r'101', line, overlapped=True)) / total_3
    _110 = len(re.findall(r'110', line, overlapped=True)) / total_3
    _111 = len(re.findall(r'111', line, overlapped=True)) / total_3

    return (_000, _001, _010, _011, _100, _101, _110, _111)

#Sum of error for a subsequence
def to_1_err(tpl):
    return abs(tpl[0]-0.5) + abs(tpl[1]-0.5)

def to_2_err(tpl):
    return abs(tpl[0]-0.25) + abs(tpl[1]-0.25) + \
        abs(tpl[2]-0.25) + abs(tpl[3]-0.25)

def to_3_err(tpl):
    return abs(tpl[0]-0.125) + abs(tpl[1]-0.125) + abs(tpl[2]-0.125) + \
        abs(tpl[3]-0.125) + abs(tpl[4]-0.125) + abs(tpl[5]-0.125) + \
        abs(tpl[6]-0.125) + abs(tpl[7]-0.125)


def get_max_1_err(tpl):
    return abs(tpl[0])-0.5

def get_max_2_err(tpl):
    return max(abs(tpl[0]-0.25), abs(tpl[1]-0.25), abs(tpl[2]-0.25), \
               abs(tpl[3]-0.25))

def get_max_3_err(tpl):
    return max(abs(tpl[0]-0.125), abs(tpl[1]-0.125), abs(tpl[2]-0.125), \
               abs(tpl[3]-0.125), abs(tpl[4]-0.125), abs(tpl[3]-0.125), \
               abs(tpl[6]-0.125), abs(tpl[7]-0.125))

freq_1 = []
freq_2 = []
freq_3 = []
for i, line in enumerate(lines):
    freq_1 += [(subseq_1_freq(line), i)]
    freq_2 += [(subseq_2_freq(line), i)]
    freq_3 += [(subseq_3_freq(line), i)]

#freq_1 = sorted(freq_1)
#freq_2 = sorted(freq_2)
#freq_3 = sorted(freq_3)

print(sorted(freq_1))
err_1_list = (list(map(lambda x : (to_1_err(x[0]), x[1]), freq_1)))
err_2_list = (list(map(lambda x : (to_2_err(x[0]), x[1]), freq_2)))
err_3_list = (list(map(lambda x : (to_3_err(x[0]), x[1]), freq_3)))

max_err_1 = np.array(list(map(lambda x : get_max_1_err(x[0]), freq_1)))
max_err_2 = np.array(list(map(lambda x : get_max_2_err(x[0]), freq_2)))
max_err_3 = np.array(list(map(lambda x : get_max_3_err(x[0]), freq_3)))

#Used for k-Means of max error for subsequences of length 1..3
max_err_1_in = max_err_1.reshape(-1,1)
max_err_2_in = max_err_2.reshape(-1,1)
max_err_3_in = max_err_3.reshape(-1,1)

#Used for k-Means of combined max errors of subsequences
max_1_2 = [ [x, y] for (x,y) in zip(max_err_1, max_err_2) ]
max_1_3 = [ [x, y] for (x,y) in zip(max_err_1, max_err_3) ]
max_2_3 = [ [x, y] for (x,y) in zip(max_err_2, max_err_3) ]
max_1_2_3 = [ [x, y, z] for (x, y, z) in zip(max_err_1, max_err_2, max_err_3) ]

#Remove remove index from tuple, gen numpy array, reshape it so that it can be used for kmeans
pure_err_array_1 = np.array(list(map(lambda x: x[0],err_1_list))).reshape(-1,1)
pure_err_array_2 = np.array(list(map(lambda x: x[0],err_2_list))).reshape(-1,1)
pure_err_array_3 = np.array(list(map(lambda x: x[0],err_3_list))).reshape(-1,1)

km = KMeans(n_clusters=2, max_iter=3000)
#km_lab_1 = km.fit(max_err_1).labels_
#km_lab_2 = km.fit(max_err_2).labels_
#km_lab_3 = km.fit(max_err_3).labels_
km_lab_1_2 = km.fit(max_1_2).labels_
km_lab_1_3 = km.fit(max_1_3).labels_
km_lab_2_3 = km.fit(max_2_3).labels_
km_lab_1_2_3 = km.fit(max_1_2_3).labels_

print("SS-1_2 humans:")
for i,v  in enumerate(km_lab_1_2):
    if v == 1:
        print(i)

print("SS-1_3 humans:")
for i,v  in enumerate(km_lab_1_3):
    if v == 1:
        print(i)

print("SS-2_3 humans:")
for i,v  in enumerate(km_lab_2_3):
    if v == 1:
        print(i)

print("SS-1_2_3 humans:")
for i,v  in enumerate(km_lab_1_2_3):
    if v == 1:
        print(i)

''''print("SS-1 humans:")
for i,v  in enumerate(km_lab_1):
    if v == 1:
        print(i)

print("SS-2 humans:")
for i,v in enumerate(km_lab_2):
    if v == 1:
        print(i)

print("SS-3 humans:")
for i,v in enumerate(km_lab_3):
    if v == 1:
        print(i)
'''
#Dummy output to check if the previous operations are correct
#print("Err_1:\n", err_1_list)
#print("P Err:\n", pure_err_array_1)
#print("Err_2:\n", err_2_list)
#print("Err_3:\n", err_3_list)
#print("\n\nKMeans results for 1-3 len subsequence freq. err.\n1:\n", km_lab_1)
#print("2:\n", km_lab_2)
#print("3:\n", km_lab_3)

db = DBSCAN()
#err_1_lab = db.fit(pure_err_array_1).labels_
#err_2_lab = db.fit(pure_err_array_2).labels_
#err_3_lab = db.fit(pure_err_array_3).labels_

#print("1:\n", err_1_lab)
#print("2:\n", err_2_lab)
#print("3:\n", err_3_lab)

labelList = list(range(1,61))



''''plt.plot(labelList, max_err_1, 'bx')
plt.axis([0,61,0,1])
plt.show()

plt.plot(labelList, max_err_2, 'bx')
plt.axis([0,61,0,1])
plt.show()

plt.plot(labelList, max_err_3, 'bx')
plt.axis([0,61,0,1])
plt.show()
'''
''''plt.plot(labelList, pure_err_array_1, 'ro')
plt.axis([0,61,0,1])
plt.show()

plt.plot(labelList, pure_err_array_2, 'go')
plt.axis([0,61,0,1])
plt.show()

plt.plot(labelList, pure_err_array_3, 'bo')
plt.axis([0,61,0,1])
plt.show()
'''
