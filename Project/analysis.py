import sys
#from apriori import apriori

#f_name = sys.argv[1]
f_name = "multi_day_paths.csv"

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
