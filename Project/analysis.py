import sys

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
    
def find_common_paths(db, minSupport):
    help = [([t[0]], 1, freq([t[0]], db), i) for i, t in enumerate(db)]
    res = []
    print(help)
    while help != []:
        newHelp = []
        for i, t in enumerate(help):
            n_seq = t[0] + [ db[t[3]][t[1]] ]
            n_i = t[1] +1
            n_freq = freq(n_seq, db)
            #check if seq equals path
            if n_i == len(db[t[3]]) and n_freq >= minSupport:
                new_res = (n_seq, n_freq) 
                if not new_res in res:
                    print("End of seq: ", new_res)
                    res += [ new_res ]
            elif n_freq < minSupport:
                new_res = (t[0], t[2])
                if not new_res in res:
                    print("too low supprt: ", new_res)
                    res += [ new_res ]
            else:
                newHelp += [ (n_seq, n_i, n_freq, t[3]) ]            
        help = newHelp
    return res

def apriori(db, minSupport):
    res = []
    
    seq_list = []
    for t in db:
        for i in t:
            if not i in seq_list:
                seq_list.append(i)

    seq_list = [ [i] for i in seq_list ]
    freq_list = [freq(s, db) for s in seq_list]
    min_length = 2
    while len(seq_list) > 1:
        n_seq = []
        #Regular apriori
        ''''for s, s_ in [ (s, s2) for s in seq_list for s2 in seq_list if s != s2]:
            #print(s, s_)
            for i in s_:
                candidate = s + [i]
                #print(candidate)
                if i not in s and not candidate in n_seq:
                    n_seq += [candidate]
                    break;
        '''
        candidates = []
        for s in seq_list:
            for i in s:
                if not i in candidates:
                    candidates += [i]
        for s in seq_list:
            for c in candidates:
                n_seq += [s + [c]]
            
        freq_list = [freq(s, db) for s in n_seq]
        del_list = [ j for j, i in enumerate(freq_list) if i < minSupport ]
        seq_list = [ i for j, i in enumerate(n_seq) if j not in del_list ]
        freq_list = [ i for j, i in enumerate(freq_list) if j not in del_list ]
        print("del list: ", len(del_list))
        print("candidate list len", len(n_seq))
        print("subres list len", len(seq_list))
        new_res = list(zip(seq_list, freq_list))
        #print("New results: ", new_res)
        if (new_res != []) and (len(new_res[0][0]) >= min_length):
            #print("New results: ", new_res)
            res += new_res
    return res


results = []

#f_name = sys.argv[1]
f_name = "multi_day_paths.csv"
#f_name = "single_day_paths.csv"

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

#print(paths[len(paths)-1])

#results = list(apriori(transactions))
#print(results)


#Build dicts of 
transitions = {}
car_type_transitions = {}
for p in paths:
    for i in range(0, len(p[4])-1):
        if p[4][i] in transitions:
            if p[4][i+1] in transitions[p[4][i]]:
                transitions[p[4][i]][p[4][i+1]] =  transitions[p[4][i]][p[4][i+1]] +1
            else:
                transitions[p[4][i]][p[4][i+1]] = 0
        else:
            transitions[p[4][i]] = {}

            
for key, value in transitions.items():
    for k, v in value.items():
        print("From: ", key, " to: ", k, " - ", v)


minsupp = 0.2
#res = find_common_paths(transactions, minsupp)
res = apriori(transactions, minsupp)

#s = ['general-gate3', 'camping1']
#s = ['general-gate1', 'ranger-stop0', 'general-gate7', 'ranger-stop2', 'general-gate4']
#print(freq(s, transactions))

print(res)

