import re
import string
#Open all filenames
vocabulary = []
hashed_sentences = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}

for i in range(1,11):
	if i < 10:
		filename = "0" + str(i)
	else:
		filename = str(i)

	file = open(filename + ".txt", "r")
	#parsed = open(filename, "w+")
	for line in file:
		#print(line)
		# Delete all non-letter 
		res = line.translate(None, string.punctuation).lower()
		# TODO: convert single newlines into space
		#parsed.write(res)

		numeric_line = ""

		for j, word in enumerate(res.split()):
			if word not in vocabulary:
				vocabulary.append(word)
			numeric_line += str(vocabulary.index(word))
			if j != len(res.split())-1:
				numeric_line += "-"
		 #print(numeric_line)

		if len(res) > 1: # why?
			hashed_sentences[i].append(numeric_line)

		out = open("output.txt", "w+")
		# Now compare against other lines
		if i != 0:
			for k in range(1,i):
				if numeric_line in hashed_sentences[k] and len(numeric_line) > 1:
					found = "This line is plagiarized from: 0" + str(k) + ".txt" + " to 0" + str(i) + ".txt\n" + line
					print(found)
					#out.write(found)
					#out.flush()
					#out.write(line)
					break;


# Check if this line matches with some other line from previous files
# If so, print an informative message
# First make it to a series of numbers

