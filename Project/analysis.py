import sys
import pytz
import datetime
import time
#import matplotlib.pyplot as plt

def seq_matches_path(path, seq):
    path_i = 0
    found = False
    for i in seq:
        #print(path_i)
        for j in range(path_i, len(path)):
            if i == path[j]:
                #print(i, " found in ", path)
                path_i = j+1
                found = True
                break
        if not found:
            #print(i, " not found in ", path)
            return False
        else:
            found = False
            
    #print(seq, " found in ", path)
    return True

def freq(seq, db):
    s = len(db)
    i = 0
    for t in db:
        if seq_matches_path(t, seq):
            i += 1

    #print("found seq ",  seq, " ", i, " times - ", s)
    if (i != 0):
        return i/s
    else:
        return 0
    
def apriori(db, minSupport, transitions, mode=1):
    res = []
    
    candidates = []
    for t in db:
        for i in t:
            if not i in candidates:
                candidates.append(i)

    seq_list = [ [i] for i in candidates ]
    #print(seq_list)
    freq_list = [freq(s, db) for s in seq_list]
    min_length = 2
    while len(seq_list) > 1:
        n_seq = []
        #optimization: only add allowed transitions
        if transitions == []:
            for s in seq_list:
                for c in candidates:
                    n_seq += [s + [c]]
        else:
            for s in seq_list:
                #print("s", s)
                #print("t", transitions[s[-1]].keys())
                for c in transitions[s[-1]].keys():
                    n_seq += [s + [c]]

            if mode == 2:
                for s in seq_list:
                    for c in transitions[s[-1]].keys():
                        for n_c in transitions[c].keys():
                            n_seq += [s + [n_c]]
            elif mode == 3:
                for s in seq_list:
                    for c in transitions[s[-1]].keys():
                        for n_c in transitions[c].keys():
                            if [s + [n_c]] not in n_seq:
                                n_seq += [s + [n_c]]
                            for nn_c in transitions[n_c].keys():
                                if [s + [nn_c]] not in n_seq:
                                    n_seq += [s + [nn_c]]

        n_seq = [s for s in n_seq if not any(s in r for r in res)]
        freq_list = [freq(s, db) for s in n_seq]
        del_list = [ j for j, i in enumerate(freq_list) if i < minSupport ]
        seq_list = [ i for j, i in enumerate(n_seq) if j not in del_list ]
        freq_list = [ i for j, i in enumerate(freq_list) if j not in del_list ]
        print("del list: ", len(del_list))
        print("candidate list len", len(n_seq))
        print("subres list len", len(seq_list))
        new_res = list(zip(freq_list, seq_list))
        #print("New results: ", new_res)
        if (new_res != []) and (len(new_res[0][1]) >= min_length) and (new_res not in res):
            #print("New results: ", new_res)
            res += new_res
    return res

def readData(f_name):
    paths = []
    transactions = []
    f = open(f_name)
    for line in f:
        line = line.strip()
        words = line.split(',')
        car_id = words[0]
        car_type = words[1]
        duration = words[2]
        loc = []
        ts = []
        for i in range(3, len(words)):
            elem = words[i].split(" ")
            ts += [elem[0]]
            loc += [elem[1]]
        paths += [(car_id, car_type, duration, ts, loc)]
        transactions += [loc]
    return (paths, transactions)

def buildTransitionMap(paths):
    transitions = {}
    for p in paths:
        for i in range(0, len(p[4])-1):
            if not p[4][i] in transitions:
                transitions[p[4][i]] = {}

            if p[4][i+1] in transitions[p[4][i]]:
                transitions[p[4][i]][p[4][i+1]] =  transitions[p[4][i]][p[4][i+1]] +1
            else:
                transitions[p[4][i]][p[4][i+1]] = 1

    for key, value in transitions.items():
        for k, v in value.items():
            print("From: ", key, " to: ", k, " - ", v)
    return transitions

def partitionDBByCar_type(paths):
    db_by_car_type = {}
    for p in paths:
        if not p[1] in db_by_car_type:
            db_by_car_type[p[1]] = [p[4]]
        else:
            db_by_car_type[p[1]] += [p[4]]
    return db_by_car_type

def computeAprioriForPartitionedDB(paths, minsupp, transitions, mode=0):
    car_type_seq = {}
    for k, v in paths.items():
        t_0 = time.time()
        car_type_seq[k] = sorted(apriori(v, minsupp, transitions, mode))
        t_1 = time.time()
        print("Computed apriori for " + k + " in ",  t_1-t_0)
    return car_type_seq
        
def writeAprioriResultToFile(f_name, res):
    f = open(f_name, 'w')
    for r in res:
        if len(r[1]) > 3:
            #print(r)
            f.write(str(r[0]) + ', ' + " ".join(r[1]) + "\n")

            
#f_name = sys.argv[1]
f_name = "multi_day_paths.csv"
o_prefix = "md_m=3"
#f_name = "single_day_paths.csv"
#o_prefix = "single_day_oa"


paths, transactions = readData(f_name)

#Build dicts of transitions
transitions = buildTransitionMap(paths)

minsupp = 0.18


t_0 = time.time()
res = sorted(apriori(transactions, minsupp, transitions, mode=2))
t_1 = time.time()
print("Computed All sequences in: ", t_1-t_0)
f_name = o_prefix + "_all_seq"
writeAprioriResultToFile(f_name, res)


print("Generate paths by car_type db...")
db_by_car_type = partitionDBByCar_type(paths)

print("Computing apriori for each car_type db...")
car_type_seq = computeAprioriForPartitionedDB(db_by_car_type, minsupp, transitions, mode=2)

for k, v in car_type_seq.items():
    f_name = o_prefix + "_" + str(k) + "_seq"
    writeAprioriResultToFile(f_name, v)


#piechart of paths
labs = []
vals = []
for k, v in db_by_car_type.items():
    labs.append(k)
    vals.append(len(v))
"""
s = sum(vals)
labs = [ "car_type " + x + " - " + str(y) + " paths" for (x, y) in zip(labs, vals)]
vals = list(map( lambda x: x/s, vals))
fix, ax1 = plt.subplots()
ax1.pie(vals, labels=labs, autopct='%1.1f%%')
ax1.axis('equal')
ax1.set_title("Paths by car_type")
plt.show()
"""


"""
car_id = paths[0][0]
first_ts = paths[0][3][0]
tz = pytz.timezone('Europe/London')
t = datetime.datetime.fromtimestamp(int(first_ts), tz)
print(t.weekday())
str_t = t.strftime('%Y-%m-%d %H:%M:%S')
print(car_id, first_ts, str_t)
print(paths[0])
print(paths[1])
"""
