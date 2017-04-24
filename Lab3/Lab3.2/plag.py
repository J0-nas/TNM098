import re
import string

vocabulary = []
hashed_sentences = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}

for i in range(1,11):
	if i < 10:
		filename = "0" + str(i)
	else:
		filename = str(i)

	file = open(filename + ".txt", "r")
	parsed = open(filename+"2.txt", "w+")
        lines = file.readlines()
        res = "".join(lines).lower()
        res = res.replace("[\n]+", "")
        #res = res.replace("\,", "")
        res = res.replace("[\r]+", "")
        res = re.sub("[^a-z^\.^0-9^\s]+", " ", res)
        res = re.sub("[\.]+", ".", res)
        res = re.sub("[\s]+", " ", res)
        lines = res.split(".")
        for iter, v in enumerate(lines):
            if v != "\n" and v != "\n\r" and v != "\r" and len(v.split(" ")) > 2:
                #print(v)
                parsed.write(v+"\n")
                numeric_line = ""

		for j, word in enumerate(v.split()):
			if word not in vocabulary:
				vocabulary.append(word)
			numeric_line += str(vocabulary.index(word))
			if j != len(v.split())-1:
				numeric_line += "-"
		 #print(numeric_line)

		if len(v) > 1: # why?
			hashed_sentences[i].append(numeric_line)

		out = open("output.txt", "w+")
		# Now compare against other lines
		if i != 0:
			for k in range(1,i):
				if numeric_line in hashed_sentences[k] and len(numeric_line) > 1:
					found = str(iter) + " - This line is plagiarized from: 0" + str(k) + ".txt" + " to 0" + str(i) + ".txt\n" + v
					print(found)
					#out.write(found)
					#out.flush()
					#out.write(line)
					break;
