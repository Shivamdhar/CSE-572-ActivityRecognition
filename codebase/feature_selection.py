import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

df = pd.read_csv("user09_fork_description_eating.csv", header=[0,1])
non_df = pd.read_csv("user09_fork_description_non_eating.csv", header=[0,1])

activities = ["eating"] * len(df) + ["non_eating"] * len(non_df)
frames = [df, non_df]
result = pd.concat(frames)

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(result)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
finalDf = pd.concat([principalDf, pd.DataFrame(data = activities, columns = ['class'])], axis=1)

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = ['eating', 'non_eating']
colors = ['r', 'g']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['class'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1'],
    			finalDf.loc[indicesToKeep, 'principal component 2'],
    			c = color, s = 50)
ax.legend(targets)
ax.grid()
plt.show()

print(pca.explained_variance_ratio_)

"""
visualize pca components
"""
pca = PCA(n_components=54)
principalComponents = pca.fit_transform(result)

# print(principalComponents[0:10])
# print(pca.components_[0:10])

for i in range(3):
	plt.plot(pca.components_[i], 'r')
plt.show()