# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

for i in range(11, 42):
	try:
		df = pd.read_csv("user" + str(i) + "_spoon_description_eating.csv", header=[0,1])
		non_df = pd.read_csv("user" + str(i) + "_spoon_description_non_eating.csv", header=[0,1])

		eating_length = len(df)
		non_eating_length = len(non_df)
		eating_gt_df = pd.DataFrame({'groundtruth' : 'eating'}, index = range(1))
		eating_gt_df =  pd.concat([eating_gt_df] * eating_length, ignore_index=True)
		non_eating_gt_df = pd.DataFrame({'groundtruth' : 'non-eating'}, index = range(1))
		non_eating_gt_df =  pd.concat([non_eating_gt_df] * non_eating_length, ignore_index=True)
		both_gt = [eating_gt_df, non_eating_gt_df]
		groundtruth = pd.concat(both_gt, ignore_index=True)

		activities = ["eating"] * len(df) + ["non_eating"] * len(non_df)
		frames = [df, non_df]
		result = pd.concat(frames)
		# print(np.where(np.isnan(result)))
		result = np.nan_to_num(result)
		pca = PCA(n_components=30)
		principalComponents = pca.fit_transform(result)
		# print(principalComponents)

		# print(groundtruth)
		principalDf = pd.DataFrame(data = principalComponents)
		principalDf = pd.concat([principalDf, groundtruth], axis = 1)
		principalDf.to_csv("user" + str(i) + "_final_file.csv")
	except:
		continue
# exit()
# principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
# finalDf = pd.concat([principalDf, pd.DataFrame(data = activities, columns = ['class'])], axis=1)
# print(finalDf)
# exit(f)
# fig = plt.figure(figsize = (8,8))
# ax = fig.add_subplot(1,1,1) 
# ax.set_xlabel('Principal Component 1', fontsize = 15)
# ax.set_ylabel('Principal Component 2', fontsize = 15)
# ax.set_title('2 component PCA', fontsize = 20)
# targets = ['eating', 'non_eating']
# colors = ['r', 'g']
# for target, color in zip(targets,colors):
    # indicesToKeep = finalDf['class'] == target
    # ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1'],
    			# finalDf.loc[indicesToKeep, 'principal component 2'],
    			# c = color, s = 50)
# ax.legend(targets)
# ax.grid()
# plt.show()

# print(pca.explained_variance_ratio_)

"""
visualize pca components
"""
# pca = PCA(n_components=79)
# principalComponents = pca.fit_transform(result)

# for i in range(79):
	# plt.plot(pca.components_[i], 'r')
# plt.show()
# print(pca.explained_variance_ratio_)