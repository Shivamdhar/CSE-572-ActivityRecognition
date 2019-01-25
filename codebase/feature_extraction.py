import constants
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pywt
from scipy.fftpack import fft
from sklearn.preprocessing import MinMaxScaler


def add_windows_to_activity_samples():
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

			eating_file = files[8] # zeating.csv
			non_eating_file = files[9] # znon_eating.csv

			window_eating = open(constants.sample_path + "/" + user + "/" + folder + "/window_eating.csv", "w")
			window_non_eating = open(constants.sample_path + "/" + user + "/" + folder + "/window_non_eating.csv", "w")
			eating_data = open(constants.sample_path + "/" + user + "/" + folder + "/" + eating_file).readlines()
			non_eating_data = open(constants.sample_path + "/" + user + "/" + folder + "/" + non_eating_file).readlines()

			writing_sampled_dataset(window_eating, eating_data)
			writing_sampled_dataset(window_non_eating, non_eating_data)

def writing_sampled_dataset(output_file, data):
	output_file.write(data[0].strip() + ",Window\n")
	temp = data[1].split(",")
	prev_timestamp = int(temp[0])
	temp[-1] = temp[-1].strip() + ",0\n"
	count = 0
	window = [",".join(temp)]

	for row in range(2, len(data)):
		temp = data[row].split(",")
		if int(temp[0]) - prev_timestamp < 100:
			temp[-1] = temp[-1].strip() + "," + str(count) + "\n"
			window.append(",".join(temp))
		else:
			count += 1
			temp[-1] = temp[-1].strip() + "," + str(count) + "\n"
			for sample in window:
				output_file.write(sample) 
			window = []
			window.append(",".join(temp))
		prev_timestamp = int(temp[0])

def extract_roll_pitch_yaw():
	dirs = os.listdir(constants.sample_path)
	dirs.sort()
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

			eating_file = files[5] # eating.csv
			non_eating_file = files[6] # non_eating.csv

			eating_data = open(constants.sample_path + "/" + user + "/" + folder + "/" + eating_file).readlines()[1:]
			non_eating_data = open(constants.sample_path + "/" + user + "/" + folder + "/" + non_eating_file).readlines()[1:]

			out_eat = open(constants.sample_path + "/" + user + "/" + folder + "/" + "zeating_euler.csv", "w")
			out_non_eat = open(constants.sample_path + "/" + user + "/" + folder + "/" + "znon_eating_euler.csv", "w")

			out_eat.write("Timestamp,Orientation X,Orientation Y,Orientation Z,Orientation W,Accelerometer X,"\
							"Accelerometer Y,Accelerometer Z,Gyroscope X,Gyroscope Y,Gyroscope Z,EMG1,EMG2,EMG3,"\
							"EMG4,EMG5,EMG6,EMG7,EMG8,Roll,Yaw\n")
			out_non_eat.write("Timestamp,Orientation X,Orientation Y,Orientation Z,Orientation W,Accelerometer X,"\
								"Accelerometer Y,Accelerometer Z,Gyroscope X,Gyroscope Y,Gyroscope Z,EMG1,EMG2,EMG3,"\
								"EMG4,EMG5,EMG6,EMG7,EMG8,Roll,Yaw\n")
			
			for row in eating_data:
				euler_roll = roll(row)
				# euler_pitch = pitch(row)
				euler_yaw = yaw(row)
				out_eat.write(row.strip() + "," + euler_roll + "," + euler_yaw + "\n")

			for row in non_eating_data:
				euler_roll = roll(row)
				# euler_pitch = pitch(row)
				euler_yaw = yaw(row)
				out_non_eat.write(row.strip() + "," + euler_roll + "," + euler_yaw + "\n")

def roll(row):
	temp = row.strip().split(",")
	return str(math.atan2(2*(float(temp[4])*float(temp[1]) + float(temp[2]) * float(temp[3])), 1 - 2*(float(temp[1])**2 + float(temp[2])**2)))

# def pitch(row):
# 	temp = row.strip().split(",")
# 	print(temp)
# 	return str(math.asin(2*(float(temp[4])*float(temp[2]) - float(temp[3])*float(temp[1]))))

def yaw(row):
	temp = row.strip().split(",")
	return str(math.atan2(2*(float(temp[4])*float(temp[3]) + float(temp[1]) * float(temp[2])), 1 - 2*(float(temp[2])**2 + float(temp[3])**2)))

def RMS(x):
    return np.sqrt(sum(x**2/len(x)))

def extract_statistical_fetaures(user, eating_type):
	scaler = MinMaxScaler()
	eating_dataset = pd.read_csv(constants.sample_path + "/" + user + "/" + eating_type + "/window_eating.csv")
	non_eating_dataset = pd.read_csv(constants.sample_path + "/" + user + "/" + eating_type + "/window_non_eating.csv")
	df = pd.DataFrame(eating_dataset, columns=["Timestamp","Orientation X","Orientation Y","Orientation Z","Orientation W","Accelerometer X","Accelerometer Y","Accelerometer Z","Gyroscope X","Gyroscope Y","Gyroscope Z","EMG1","EMG2","EMG3","EMG4","EMG5","EMG6","EMG7","EMG8","Roll","Yaw","Window"])
	eating_dataset[["Orientation X","Orientation Y","Orientation Z","Orientation W","Accelerometer X","Accelerometer Y","Accelerometer Z","Gyroscope X","Gyroscope Y","Gyroscope Z","EMG1","EMG2","EMG3","EMG4","EMG5","EMG6","EMG7","EMG8","Roll","Yaw"]] = scaler.fit_transform(eating_dataset[["Orientation X","Orientation Y","Orientation Z","Orientation W","Accelerometer X","Accelerometer Y","Accelerometer Z","Gyroscope X","Gyroscope Y","Gyroscope Z", "EMG1","EMG2","EMG3","EMG4","EMG5","EMG6","EMG7","EMG8","Roll","Yaw"]])
	non_eating_dataset[["Orientation X","Orientation Y","Orientation Z","Orientation W","Accelerometer X","Accelerometer Y","Accelerometer Z","Gyroscope X","Gyroscope Y","Gyroscope Z","EMG1","EMG2","EMG3","EMG4","EMG5","EMG6","EMG7","EMG8","Roll","Yaw"]] = scaler.fit_transform(non_eating_dataset[["Orientation X","Orientation Y","Orientation Z","Orientation W","Accelerometer X","Accelerometer Y","Accelerometer Z","Gyroscope X","Gyroscope Y","Gyroscope Z", "EMG1","EMG2","EMG3","EMG4","EMG5","EMG6","EMG7","EMG8","Roll","Yaw"]])
	df = eating_dataset.groupby('Window').agg({'Orientation X':['mean','std', np.min, np.max, RMS],
											'Orientation Y':['mean','std', np.min, np.max, RMS],
											'Orientation Z':['mean','std', np.min, np.max, RMS],
											'Orientation W':['mean','std', np.min, np.max, RMS],
											'Accelerometer X':['mean','std', np.min, np.max, RMS],
											'Accelerometer Y':['mean','std', np.min, np.max, RMS],
											'Accelerometer Z':['mean','std', np.min, np.max, RMS],
											'Gyroscope X':['mean','std', np.min, np.max, RMS],
											'Gyroscope Y':['mean','std', np.min, np.max, RMS],
											'Gyroscope Z':['mean','std', np.min, np.max, RMS],
											'EMG1':['mean','std', np.min, np.max, RMS],
											'EMG2':['mean','std', np.min, np.max, RMS],
											'EMG3':['mean','std', np.min, np.max, RMS],
											'EMG4':['mean','std', np.min, np.max, RMS],
											'EMG5':['mean','std', np.min, np.max, RMS],
											'EMG6':['mean','std', np.min, np.max, RMS],
											'EMG7':['mean','std', np.min, np.max, RMS],
											'EMG8':['mean','std', np.min, np.max, RMS],
											'Roll':['mean','std', np.min, np.max, RMS],
											'Yaw':['mean','std', np.min, np.max, RMS]})
	df.to_csv("user09_fork_description_eating.csv")
	non_df = non_eating_dataset.groupby('Window').agg({'Orientation X':['mean','std', np.min, np.max, RMS],
											'Orientation Y':['mean','std', np.min, np.max, RMS],
											'Orientation Z':['mean','std', np.min, np.max, RMS],
											'Orientation W':['mean','std', np.min, np.max, RMS],
											'Accelerometer X':['mean','std', np.min, np.max, RMS],
											'Accelerometer Y':['mean','std', np.min, np.max, RMS],
											'Accelerometer Z':['mean','std', np.min, np.max, RMS],
											'Gyroscope X':['mean','std', np.min, np.max, RMS],
											'Gyroscope Y':['mean','std', np.min, np.max, RMS],
											'Gyroscope Z':['mean','std', np.min, np.max, RMS],
											'EMG1':['mean','std', np.min, np.max, RMS],
											'EMG2':['mean','std', np.min, np.max, RMS],
											'EMG3':['mean','std', np.min, np.max, RMS],
											'EMG4':['mean','std', np.min, np.max, RMS],
											'EMG5':['mean','std', np.min, np.max, RMS],
											'EMG6':['mean','std', np.min, np.max, RMS],
											'EMG7':['mean','std', np.min, np.max, RMS],
											'EMG8':['mean','std', np.min, np.max, RMS],
											'Roll':['mean','std', np.min, np.max, RMS],
											'Yaw':['mean','std', np.min, np.max, RMS]})
	non_df.to_csv("user09_fork_description_non_eating.csv")

def visualize_accelerometer_readings(property):
	df = pd.read_csv("user09_fork_description_eating.csv", header=[0,1])
	non_df = pd.read_csv("user09_fork_description_non_eating.csv", header=[0,1])
	plt.subplot(311)
	plt.plot(non_df["Accelerometer X"][property], 'r--', df["Accelerometer X"][property], 'b--')

	plt.subplot(312)
	plt.plot(non_df["Accelerometer Y"][property], 'r--', df["Accelerometer Y"][property], 'b--')

	plt.subplot(313)
	plt.plot(non_df["Accelerometer Z"][property], 'r--', df["Accelerometer Z"][property], 'b--')

	plt.show()

def visualize_orientation_readings(property):
	df = pd.read_csv("user09_fork_description_eating.csv", header=[0,1])
	non_df = pd.read_csv("user09_fork_description_non_eating.csv", header=[0,1])
	plt.subplot(411)
	plt.plot(non_df["Orientation X"][property], 'r--', df["Orientation X"][property], 'b--')

	plt.subplot(412)
	plt.plot(non_df["Orientation Y"][property], 'r--', df["Orientation Y"][property], 'b--')

	plt.subplot(413)
	plt.plot(non_df["Orientation Z"][property], 'r--', df["Orientation Z"][property], 'b--')

	plt.subplot(414)
	plt.plot(non_df["Orientation W"][property], 'r--', df["Orientation W"][property], 'b--')

	plt.show()

def visualize_gyroscope_readings(property):
	df = pd.read_csv("user09_fork_description_eating.csv", header=[0,1])
	non_df = pd.read_csv("user09_fork_description_non_eating.csv", header=[0,1])
	plt.subplot(311)
	plt.plot(non_df["Gyroscope X"][property], 'r--', df["Gyroscope X"][property], 'b--')

	plt.subplot(312)
	plt.plot(non_df["Gyroscope Y"][property], 'r--', df["Gyroscope Y"][property], 'b--')

	plt.subplot(313)
	plt.plot(non_df["Gyroscope Z"][property], 'r--', df["Gyroscope Z"][property], 'b--')

	plt.show()

extract_roll_pitch_yaw()
add_windows_to_activity_samples()
extract_statistical_fetaures("user09", "fork")
visualize_accelerometer_readings("mean")
visualize_accelerometer_readings("std")
visualize_accelerometer_readings("RMS")
visualize_accelerometer_readings("amin")
visualize_accelerometer_readings("amax")
visualize_orientation_readings("mean")
visualize_orientation_readings("std")
visualize_orientation_readings("RMS")
visualize_orientation_readings("amin")
visualize_orientation_readings("amax")
visualize_gyroscope_readings("mean")
visualize_gyroscope_readings("std")
visualize_gyroscope_readings("RMS")
visualize_gyroscope_readings("amin")
visualize_gyroscope_readings("amax")