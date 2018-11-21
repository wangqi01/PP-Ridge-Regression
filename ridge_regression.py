import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.utils import shuffle


clf = Ridge(alpha=0.01)  # 正则化项系数
# 先进行数据的预处理,读取数据等操作
data = pd.read_excel('./data.xlsx')
data = shuffle(data)    # 打乱数据的顺序
print(data)
data_train = np.array(data[:])
train_x = data_train[:, :8]
train_y = data_train[:, -2:-1]
clf.fit(train_x, train_y)
coef = clf.coef_
print(coef)
print()

test_x = data_train[100:200, :8]
test_y = data_train[100:200, -2:-1]
print(clf.score(test_x, test_y))

