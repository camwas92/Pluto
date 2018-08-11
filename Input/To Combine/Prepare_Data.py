import glob
import os

lines = []

fout = open('combined.csv', "w+")

for file in glob.glob("*.txt"):
    print(file)
    fin = open(file)
    for line in fin:
        line = line.replace("[", "")
        line = line.replace("]", "")
        fout.write(line)
    fin.close()
fout.close()
