def loadHisto(name):
    f = open(name)
    histo = f.readlines()
    #print(len(histo))
    for i in range(3):
        histo[i] = histo[i].split(",")
    return histo

def compareHisto(a, b):
    err = 0
    for i in range(3):
        for c in range(256):
            err += abs(float(a[i][c]) - float(b[i][c]))
    return err
            
ids = ["0" + str(x) if x < 10 else str(x) for x in range(1,13)]
print(ids)
start = 1

histo = loadHisto('out_'+ids[start-1])
histo_c = loadHisto('out_center_10-10_'+ ids[start-1])
histo_corner_00 = loadHisto('out_0-0_' + ids[start-1])
histo_corner_01 = loadHisto('out_0-1_' + ids[start-1])
histo_corner_10 = loadHisto('out_1-0_' + ids[start-1])
histo_corner_11 = loadHisto('out_1-1_' + ids[start-1])

print(len(histo_c[0]))
print(len(histo_corner_01[1]))
print(len(histo_corner_11[2]))

f = open('comparison_result', 'w+')
f.write("Result of comparing the "+ str(ids[start-1]) + " image with the other images\n")

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

    f.write("Error with " + id + "\n")
    f.write("histo " + str(err) + "\n")
    f.write("histo Center " + str(err_c) + "\n")
    f.write("\thisto_c_00 " + str(err_c_00) + "\n")
    f.write("\thisto_c_01 " + str(err_c_01) + "\n")
    f.write("\thisto_c_10 " + str(err_c_10) + "\n")
    f.write("\thisto_c_11 " + str(err_c_11) + "\n")
    f.write("Corner Sum " + str(err_c_sum) + "\n")
    
    f.write("\n")
