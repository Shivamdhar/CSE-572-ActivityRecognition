import os

dirs = os.listdir(".")

f = open("train_user_independent.csv","r")
f_array = f.readlines()

for i in dirs:
	if i.startswith("test_user_independent_"):
		file = open(i,"r")
		file_array = file.readlines()
		temp = i.replace("test_user_independent_","").replace(".csv","")
		f_write = open("combined_user_independent_"+str(temp)+".csv","w")
		for j in f_array:
			f_write.write(j)
		for k in range(1,len(file_array)):
			f_write.write(file_array[k])