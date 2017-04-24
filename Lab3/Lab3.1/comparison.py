def loadHisto(name):
    f = open(name)
    histo = f.readlines()
    #print(len(histo))
    for i in range(3):
        histo[i] = histo[i].split(",")
    return histo

def load_AvgColor_Lumi(name):
    f = open(name)
    avgColor = list(map(lambda x: float(x), f.readline().split(",")))
    lumi = float(f.readline())
    return (avgColor, lumi)

def compareHisto(a, b):
    err = 0
    for i in range(3):
        for c in range(256):
            err += abs(float(a[i][c]) - float(b[i][c]))
    return err

def compareAvgColor(a, b):
    err = 0
    for i in range(3):
        err += abs(a[i] - b[i])
    return err

                   
ids = ["0" + str(x) if x < 10 else str(x) for x in range(1,13)]
print(ids)
start = 1

#Load base image metrics 
histo = loadHisto('out_'+ids[start-1])
histo_c = loadHisto('out_center_10-10_'+ ids[start-1])
histo_corner_00 = loadHisto('out_0-0_' + ids[start-1])
histo_corner_01 = loadHisto('out_0-1_' + ids[start-1])
histo_corner_10 = loadHisto('out_1-0_' + ids[start-1])
histo_corner_11 = loadHisto('out_1-1_' + ids[start-1])
avg_color, lumi = load_AvgColor_Lumi(ids[start-1] + "_data.txt")

print(len(histo_c[0]))
print(len(histo_corner_01[1]))
print(len(histo_corner_11[2]))

f = open('comparison_result', 'w+')
f.write("Result of comparing the "+ str(ids[start-1]) + " image with the other images\n")
all_err = []
all_err_c = []
all_err_sum = []
all_err_avg = []
all_err_lumi = []

#For each image besides the base image, read the metrics and print the error into an output file
otherIds = [ids[i-1] for i in range(1,13) if (i!=start) ]
for id in otherIds:
    o_histo = loadHisto('out_'+id)
    o_histo_c = loadHisto('out_center_10-10_'+ id)
    o_histo_corner_00 = loadHisto('out_0-0_' + id)
    o_histo_corner_01 = loadHisto('out_0-1_' + id)
    o_histo_corner_10 = loadHisto('out_1-0_' + id)
    o_histo_corner_11 = loadHisto('out_1-1_' + id)
    err = compareHisto(histo, o_histo)
    err_c = compareHisto(histo_c, o_histo_c)
    err_c_00 = compareHisto(histo_corner_00, o_histo_corner_00)
    err_c_01 = compareHisto(histo_corner_01, o_histo_corner_01)
    err_c_10 = compareHisto(histo_corner_10, o_histo_corner_10)
    err_c_11 = compareHisto(histo_corner_11, o_histo_corner_11)
    err_c_sum = (err_c_00 + err_c_01 + err_c_10 + err_c_11)/4
    o_avg, o_lumi = load_AvgColor_Lumi(id + "_data.txt")
    err_avg = compareAvgColor(avg_color, o_avg)
    err_lumi = abs(lumi - o_lumi)

    f.write("Error with image: " + id + "\n")
    f.write("histo \t\t\t" + str(err) + "\n")
    f.write("histo Center \t\t" + str(err_c) + "\n")
    #f.write("\thisto_c_00 " + str(err_c_00) + "\n")
    #f.write("\thisto_c_01 " + str(err_c_01) + "\n")
    #f.write("\thisto_c_10 " + str(err_c_10) + "\n")
    #f.write("\thisto_c_11 " + str(err_c_11) + "\n")
    f.write("Corner Sum \t\t" + str(err_c_sum) + "\n")
    f.write("Avg color error \t" + str(err_avg) + "\n")
    f.write("Lumi error \t\t" + str(err_lumi) + "\n")
    f.write("\n")

    all_err += [(err, id)]
    all_err_c += [(err_c, id)]
    all_err_sum += [(err_c_sum, id)]
    all_err_avg += [(err_avg, id)]
    all_err_lumi += [(err_lumi, id)]

#Compute the max error for each metric
max_err = max(all_err)[0]
max_err_c = max(all_err_c)[0]
max_err_sum = max(all_err_sum)[0]
max_err_avg = max(all_err_avg)[0]
max_err_lumi = max(all_err_lumi)[0]

#Normalize the errors using the max error
n_all_err = [(x[0]/max_err, x[1]) for x in all_err]
n_all_err_c = [(x[0]/max_err_c, x[1]) for x in all_err_c]
n_all_err_sum = [(x[0]/max_err_sum, x[1]) for x in all_err_sum]
n_all_err_avg = [(x[0]/max_err_avg, x[1]) for x in all_err_avg]
n_all_err_lumi = [(x[0]/max_err_lumi, x[1]) for x in all_err_lumi]

print(sorted(n_all_err))
print(sorted(n_all_err_avg))

#print(n_all_err_sum, n_all_err_lumi)
#Zip the lists to a tuple
n_err_list = [(x[0][0], x[1][0], x[2][0], x[3][0], x[4][0], x[0][1]) for x in zip(n_all_err,n_all_err_c, n_all_err_sum, n_all_err_avg, n_all_err_lumi)]
#print(n_err_list)

#Define weights used to compute the total error of an image to the base
w1 = 0.2
w2 = 0.3
w3 = 0.2
w4 = 0.15
w5 = 0.15
summed = [ (w1*x[0]+w2*x[1]+w3*x[2]+w4*x[3]+w5*x[4], x[5])for x in n_err_list]

#Rank the images according to the total error
res = sorted(summed)
print(res)
