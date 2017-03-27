import regex as re

f = open("CoinToss.txt", "r")
lines = []
for line in f:
    lines += [line]

#print(len(lines[1]), "\n")
ones = []
for i, line in enumerate(lines):
    ones += [(len(''.join(c for c in line if c == '1')), i)]

#Assume 50/50 split of 0s/1s ~ sort for greatest diviation 
ones_ = list(map(lambda x: (abs(100-x[0]), x[1]), ones))
ones_sorted = sorted(ones_)
print(ones_sorted)

def subseq_1_freq(line):
    total_1 = len(line)
    _0 = len(re.findall(r'0', line)) / total
    _1 = len(re.findall(r'1', line)) / total

    return (_0, _1)

def subseq_2_freq(line):
    total_2 = len(line) - 2
    
    _00 = len(re.findall(r'00', line, overlapped=True)) / total_2
    _01 = len(re.findall(r'01', line, overlapped=True)) / total_2
    _10 = len(re.findall(r'10', line, overlapped=True)) / total_2
    _11 = len(re.findall(r'11', line, overlapped=True)) / total_2

    return (_00, _01, _10, _11)
    
def subseq_3_freq(line):
    total_3 = len(line) - 3
    
    _000 = len(re.findall(r'000', line, overlapped=True)) / total_3
    _001 = len(re.findall(r'001', line, overlapped=True)) / total_3
    _010 = len(re.findall(r'010', line, overlapped=True)) / total_3
    _011 = len(re.findall(r'011', line, overlapped=True)) / total_3
    _100 = len(re.findall(r'100', line, overlapped=True)) / total_3
    _101 = len(re.findall(r'101', line, overlapped=True)) / total_3
    _110 = len(re.findall(r'110', line, overlapped=True)) / total_3
    _111 = len(re.findall(r'111', line, overlapped=True)) / total_3

    return (_000, _001, _010, _011, _100, _101, _110, _111)

def to_2_err(tlp):
    return abs(tlp[0]-0.25) + abs(tlp[1]-0.25) + \
        abs(tlp[2]-0.25) + abs(tlp[3]-0.25) 

def to_3_err(tlp):
    return abs(tlp[0]-0.125) + abs(tlp[1]-0.125) + abs(tlp[2]-0.125) + \
        abs(tlp[3]-0.125) + abs(tlp[4]-0.125) + abs(tlp[5]-0.125) + \
        abs(tlp[6]-0.125) + abs(tlp[7]-0.125)

freq_2 = []
freq_3 = []
for i, line in enumerate(lines):
    freq_2 += [(subseq_2_freq(line), i)]
    freq_3 += [(subseq_3_freq(line), i)]

freq_2 = sorted(freq_2)
freq_3 = sorted(freq_3)

#print(freq_2)
#print(freq_3)

err_2_list = sorted(list(map(lambda x : (to_2_err(x[0]), x[1]), freq_2)))
err_3_list = sorted(list(map(lambda x : (to_3_err(x[0]), x[1]), freq_3)))

print("Err_2:\n", err_2_list)
print("Err_3:\n", err_3_list)
