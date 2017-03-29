import regex as re
import numpy as np
from sklearn.cluster import KMeans


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

def to_1_err(tpl):
    return abs(tpl[0]-0.5) + abs(tpl[1]-0.5)

def to_2_err(tpl):
    return abs(tpl[0]-0.25) + abs(tpl[1]-0.25) + \
        abs(tpl[2]-0.25) + abs(tpl[3]-0.25) 

def to_3_err(tpl):
    return abs(tpl[0]-0.125) + abs(tpl[1]-0.125) + abs(tpl[2]-0.125) + \
        abs(tpl[3]-0.125) + abs(tpl[4]-0.125) + abs(tpl[5]-0.125) + \
        abs(tpl[6]-0.125) + abs(tpl[7]-0.125)

def max_1_err(tpl):
    return abs(tpl[0])-0.5

def max_2_err(tpl):
    return max(abs(tpl[0]-0.25), abs(tpl[1]-0.25), abs(tpl[2]-0.25), \
               abs(tpl[3]-0.25))

def max_3_err(tpl):
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

err_1_list = (list(map(lambda x : (to_1_err(x[0]), x[1]), freq_1)))
err_2_list = (list(map(lambda x : (to_2_err(x[0]), x[1]), freq_2)))
err_3_list = (list(map(lambda x : (to_3_err(x[0]), x[1]), freq_3)))

#Remove remove index from tuple, gen numpy array, reshape it so that it can be used for kmeans
pure_err_array_1 = np.array(list(map(lambda x: x[0],err_1_list))).reshape(-1,1)
pure_err_array_2 = np.array(list(map(lambda x: x[0],err_2_list))).reshape(-1,1)
pure_err_array_3 = np.array(list(map(lambda x: x[0],err_3_list))).reshape(-1,1)

km = KMeans(n_clusters=2, max_iter=3000)
km_lab_1 = km.fit(pure_err_array_1).labels_
km_lab_2 = km.fit(pure_err_array_2).labels_
km_lab_3 = km.fit(pure_err_array_3).labels_

#Dummy output to check if the previous operations are correct
print("Err_1:\n", err_1_list)
print("P Err:\n", pure_err_array_1)
#print("Err_2:\n", err_2_list)
#print("Err_3:\n", err_3_list)
print("\n\nKMeans results for 1-3 len subsequence freq. err.\n1:\n", km_lab_1)
print("2:\n", km_lab_2)
print("3:\n", km_lab_3)
