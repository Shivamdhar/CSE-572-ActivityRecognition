import numpy as np
import pandas as pd

user_indices_map = {}

data = []
count = 0
for i in range(9, 42):
	try:
		file = open("user" + str(i) + "_final_file.csv", "r")
		samples = file.readlines()
		data += samples[1:]
		user_indices_map[i] = (count, count+len(samples))
		count += len(samples)
	except:
		continue

print(user_indices_map)
print(len(user_indices_map))

file = open("combined_entire_independent.csv", "w")
for row in data:
	file.write(row)

from random import shuffle
users = list(user_indices_map.keys())
shuffle(users)

training_users = users[:18]
testing_users = users[18:]

training_data = []
for user in training_users:
	indices = user_indices_map[user]
	training_data += data[indices[0]:indices[1]]

for user in testing_users:
	indices = user_indices_map[user]
	test_data = data[indices[0]:indices[1]]
	test = open("test_user_independent_" + str(user) + ".csv", "w")
	test.write(",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,groundtruth\n")
	for row in test_data:
		test.write(row)
	test.close()

train = open("train_user_independent.csv", "w")
train.write(",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,groundtruth\n")
for row in training_data:
	train.write(row)

print(training_users)
print(testing_users)