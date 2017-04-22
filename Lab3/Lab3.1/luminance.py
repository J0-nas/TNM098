import cv2
import numpy as np

# One file per image with all the data
for imgn in range(1,13):
	if imgn < 10:
		filename = "0" + str(imgn)
	else:
		filename = str(imgn)
	img = cv2.imread(filename + ".jpg")
	data_file = open(filename + "_data.txt", "w+")

	# Average RGB
	avg = [0, 0, 0]
	avg_lumi = 0
	for x, line in enumerate(img):
		for y, px in enumerate(line):
			avg[0] += img[x][y][0]
			avg[1] += img[x][y][1]
			avg[2] += img[x][y][2]
	print(avg)
	avg = np.divide(avg, (len(img) * len(img[0])))
	avg_lumi += 0.2126 * avg[0] + 0.7152 * avg[1] + 0.0722 * avg[2]
	#avg_lumi = np.divide(avg_lumi, (len(img) * len(img[0])))
	print(avg)
	print(avg_lumi)
	data_file.write("# RGB (average, whole image)\n")
	data_file.write("R:" + str(avg[0]) + " G:" + str(avg[1]) + " B:" + str(avg[2]) + "\n")
	data_file.write("# Luminance (average, whole image)\n")
	data_file.write(str(avg_lumi))

# Luminance

