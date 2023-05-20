import numpy as np
from sklearn.decomposition import FastICA

# 假设有一个二维数据集 X，形状为 (n_samples, n_features)
X = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

# 创建 FastICA 模型对象
ica = FastICA(n_components=3)

# 对数据集 X 进行 ICA 数据处理
X_processed = ica.fit_transform(X)

# 打印处理后的数据集
print(X_processed)