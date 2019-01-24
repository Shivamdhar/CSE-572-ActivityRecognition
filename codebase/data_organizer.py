import constants
import os

def tag_samples_using_ground_truth():
	dirs = os.listdir(constants.ground_truth_path)
	for user in dirs:
		if(user == ".DS_Store"):
			continue
		folders = os.listdir(constants.ground_truth_path + "/" + user)
		for folder in folders:
			if(folder == ".DS_Store"):
				continue

			files = os.listdir(constants.ground_truth_path + "/" + user + "/" + folder)
			file = open(constants.ground_truth_path + "/" + user + "/" + folder + "/" + files[0], "r")

			start_samples = []
			end_samples = []
			data = file.readlines()
			file.close()

			for row in data:
				temp = row.split(",")
				if temp[0] == "\n":
					break
				start_samples.append((int(temp[0]) * 50)//30)
				end_samples.append((int(temp[1]) * 50)//30)

			files = os.listdir(constants.sample_path + "/" + user + "/" + folder)

			EMG_files = [i for i in files if i.endswith("_EMG.txt") and i.startswith("post")]
			EMG_file = open(constants.sample_path + "/" + user + "/" + folder + "/" + EMG_files[0], "r")

			output_file = open(constants.sample_path + "/" + user + "/" + folder + "/" + "annotated_" + EMG_files[0], "w")
			data = EMG_file.readlines()
			
			annotated_data = [row.strip() + ", 0\n" for row in data]

			for i in range(len(start_samples)):
				k = 1
				for j in range(start_samples[i], end_samples[i]):
					if j >= len(annotated_data):
						break
					temp = annotated_data[j].split(",")
					temp[-1] = " 1\n"
					annotated_data[j] = ",".join(temp)

			for row in annotated_data:
				output_file.write(row)

			EMG_file.close()
			output_file.close()

			IMU_files = [i for i in files if i.endswith("_IMU.txt") and not i.startswith("annotated")]
			IMU_file = open(constants.sample_path + "/" + user + "/" + folder + "/" + IMU_files[0], "r")

			output_file = open(constants.sample_path + "/" + user + "/" + folder + "/" + "annotated_" + IMU_files[0], "w")
			data = IMU_file.readlines()
			annotated_data = [row.strip() + ", 0\n" for row in data]

			for i in range(len(start_samples)):
				for j in range(start_samples[i], end_samples[i]):
					if j >= len(annotated_data):
						break
					temp = annotated_data[j].split(",")
					temp[-1] = "1\n"
					annotated_data[j] = ",".join(temp)

			for row in annotated_data:
				output_file.write(row)

			IMU_file.close()
			output_file.close()

"""
Removes alternate row from EMG file to synchronize the two sample datasets. 
"""
def EMG_IMU_sync():
	dirs = os.listdir(constants.sample_path)
	for user in dirs:
		if(user == ".DS_Store"):
			continue
		folders = os.listdir(constants.sample_path + "/" + user)
		folders = [folder for folder in folders if not folder.endswith(".csv")]
		for folder in folders:
			if(folder == ".DS_Store"):
				continue
			files = os.listdir(constants.sample_path + "/" + user + "/" + folder)
			EMG_files = [i for i in files if i.endswith("_EMG.txt") and not i.startswith("annotated")]
			EMG_file = open(constants.sample_path + "/" + user + "/" + folder + "/" + EMG_files[0], "r")

			output_file = open(constants.sample_path + "/" + user + "/" + folder + "/" + "post_duplicate_"\
								"removal_" + EMG_files[0], "w")
			data = EMG_file.readlines()
			for row in range(0, len(data), 2):
				output_file.write(data[row])

"""
Helper method to delete unwanted files created while preprocessing 
"""
def delete_unwanted_files():
	dirs = os.listdir(constants.sample_path)
	for user in dirs:
		if(user == ".DS_Store"):
			continue
		folders = os.listdir(constants.sample_path + "/" + user)
		# folders = [folder for folder in folders if not folder.endswith(".csv")]
		files = [file for file in folders if file.endswith(".csv")]
		[os.remove(constants.sample_path + "/" + user + "/" + file) for file in files if file.endswith(".csv")]
		# for folder in folders:
		# 	if(folder == ".DS_Store"):
		# 		continue
		# 	files = os.listdir(sample_path + "/" + user + "/" + folder)
		# 	[os.remove(sample_path + "/" + user + "/" + folder + "/" + file) for file in files if file.startswith("non")]

"""
Segregates eating and non-eating activities for each user. 
"""
def activity_division():
	dirs = os.listdir(constants.sample_path)
	for user in dirs:
		if(user == ".DS_Store"):
			continue
		folders = os.listdir(constants.sample_path + "/" + user)
		folders = [folder for folder in folders if not folder.endswith(".csv")]
		for folder in folders:
			if(folder == ".DS_Store"):
				continue
			files = os.listdir(constants.sample_path + "/" + user + "/" + folder)
			files.sort()

			emg_file = files[5] #retain annotated post duplicate removal EMG file
			imu_file = files[4] #retain annotated IMU file

			emg_data = open(constants.sample_path + "/" + user + "/" + folder + "/" + emg_file).readlines()
			imu_data = open(constants.sample_path + "/" + user + "/" + folder + "/" + imu_file).readlines()

			record_lengths = min(len(emg_data), len(imu_data))
			output_eating = open(constants.sample_path + "/" + user + "/" + folder + "/" + "eating.csv", "w")
			output_non_eating = open(constants.sample_path + "/" + user + "/" + folder + "/" + "non_eating.csv", "w")

			output_eating.write("Timestamp,Orientation X,Orientation Y,Orientation Z,Orientation W,Accelerometer X,"\
								"Accelerometer Y,Accelerometer Z,Gyroscope X,Gyroscope Y,Gyroscope Z,EMG1,EMG2,EMG3,"\
								"EMG4,EMG5,EMG6,EMG7,EMG8\n")
			output_non_eating.write("Timestamp,Orientation X,Orientation Y,Orientation Z,Orientation W,Accelerometer X"\
									",Accelerometer Y,Accelerometer Z,Gyroscope X,Gyroscope Y,Gyroscope Z,EMG1,EMG2,"\
									"EMG3,EMG4,EMG5,EMG6,EMG7,EMG8\n")

			for i in range(record_lengths):
				temp1 = emg_data[i].split(",")
				temp2 = imu_data[i].split(",")
				temp2 = temp2[:-1]

				if temp1[-1].strip() == "0":
					output_non_eating.write(",".join(temp2) + "," + ",".join(temp1[1:-1]) + "\n")
				else:
					output_eating.write(",".join(temp2) + "," + ",".join(temp1[1:-1]) + "\n")

# delete_unwanted_files()
EMG_IMU_sync()
print("****** Alternate row removed from EMG sample dataset ******\n")
tag_samples_using_ground_truth()
print("****** Sample dataset tagget using ground truth ******\n")
activity_division()
print("****** Separate activity dataset created ******\n")


# Below method no longer used as we are using fork and spoon dataset separately
# def aggregate_spoon_fork_activity_samples():
# 	prefix = "/home/shivam/Desktop/DM/Project/MyoData/MyoData"
# 	dirs = os.listdir(prefix)
# 	for user in dirs:
# 		if(user == ".DS_Store"):
# 			continue
# 		EMG_output_file = open(prefix + "/" + user + "/EMG_file.csv", "w")
# 		IMU_output_file = open(prefix + "/" + user + "/IMU_file.csv", "w")
# 		EMG_records = []
# 		IMU_records = []

# 		files = os.listdir(prefix + "/" + user + "/fork")
# 		EMG_file = [i for i in files if i.endswith("_EMG.txt") and i.startswith("annotated")]
# 		IMU_file = [i for i in files if i.endswith("_IMU.txt") and i.startswith("annotated")]
# 		EMG_records += open(prefix + "/" + user + "/fork/" +  EMG_file[0], "r").readlines()
# 		IMU_records += open(prefix + "/" + user + "/fork/" +  IMU_file[0], "r").readlines()

# 		files = os.listdir(prefix + "/" + user + "/spoon")
# 		EMG_file = [i for i in files if i.endswith("_EMG.txt") and i.startswith("annotated")]
# 		IMU_file = [i for i in files if i.endswith("_IMU.txt") and i.startswith("annotated")]
# 		EMG_records += open(prefix + "/" + user + "/spoon/" +  EMG_file[0], "r").readlines()
# 		IMU_records += open(prefix + "/" + user + "/spoon/" +  IMU_file[0], "r").readlines()

# 		EMG_records.sort(key=lambda x: int(x.split(",")[0]))
# 		IMU_records.sort(key=lambda x: int(x.split(",")[0]))

# 		EMG_output_file.write("Timestamp, EMG 1, EMG 2, EMG 3, EMG 4, EMG 5, EMG 6, EMG 7, EMG 8, Tag\n")
# 		for record in EMG_records:
# 			EMG_output_file.write(record)
# 		IMU_output_file.write("Timestamp, Orientation X, Orientation Y, Orientation Z, Orientation W, Accelerometer X, Accelerometer Y, Accelerometer Z, Gyroscope X, Gyroscope Y, Gyroscope Z, Tag\n")
# 		for record in IMU_records:
# 			IMU_output_file.write(record)

"""
Tags samples in MyoData as eating and non-eating based on ground truth available as video frames
"""
