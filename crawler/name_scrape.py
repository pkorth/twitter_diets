import re, sys

#filename = "meat_data.txt"
filename = sys.argv[1]
infile = open(filename)
corpus = infile.read()
infile.close()

pattern = r"@([a-zA-Z0-9]+)  [A-Z][a-z][a-z]"
pattern2 = r"@([a-zA-Z0-9]+)  [0-9]+"

result = re.findall(pattern, corpus)
result += re.findall(pattern2, corpus)

for r in result:
    print r
