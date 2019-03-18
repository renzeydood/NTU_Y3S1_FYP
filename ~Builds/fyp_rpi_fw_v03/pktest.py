import pickle as pk


f = open('data.p', 'r')   # 'r' for reading; can be omitted
mydict = pk.load(f)         # load file content as mydict
f.close()

print(mydict)
print("Data pickled")
