import regex as re

f = open("CoinToss.txt", "r")
lines = []
for line in f:
    lines += [line]

#print(len(lines[1]), "\n")
ones = []
for i, line in enumerate(lines):
    ones += [(len(''.join(c for c in line if c == '1')), i)]

print(ones)

ones_ = list(map(lambda x: (abs(100-x[0]), x[1]), ones))
#print(ones_, "\n\n")

ones_sorted = sorted(ones_)
print(ones_sorted)

def subsequences(line):
    total_2 = len(line) - 2
    total_3 = len(line) - 3
    
    _00 = len(re.findall(r'00', line, overlapped=True)) / total_2
    _01 = len(re.findall(r'01', line, overlapped=True)) / total_2
    _10 = len(re.findall(r'10', line, overlapped=True)) / total_2
    _11 = len(re.findall(r'11', line, overlapped=True)) / total_2
    
    
    _000 = len(re.findall(r'000', line, overlapped=True)) / total_3
    _001 = len(re.findall(r'001', line, overlapped=True)) / total_3
    _010 = len(re.findall(r'010', line, overlapped=True)) / total_3
    _011 = len(re.findall(r'011', line, overlapped=True)) / total_3
    _100 = len(re.findall(r'100', line, overlapped=True)) / total_3
    _101 = len(re.findall(r'101', line, overlapped=True)) / total_3
    _110 = len(re.findall(r'110', line, overlapped=True)) / total_3
    _111 = len(re.findall(r'111', line, overlapped=True)) / total_3

    return ((_00, _01, _10, _11),(_000, _001, _010, _011, _100, _101, _110, _111))

freq = []
for i, line in enumerate(lines):
    freq += [(subsequences(line), i)]


print(freq)
