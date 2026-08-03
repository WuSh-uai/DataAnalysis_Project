# -*- coding: utf-8 -*-
"""
共享单车租用量预测 - K-Means聚类分析（无监督学习）
对应章节：第4章 4.7节
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ========== 解决中文显示问题 ==========
# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# ========== 1. 加载数据 ==========
df = pd.read_csv('day_processed.csv')

print("=" * 60)
print("K-Means聚类分析")
print("=" * 60)

# ========== 2. 选择聚类特征 ==========
# 选择环境相关特征（与租用量密切相关）
cluster_features = ['temp', 'atemp', 'hum', 'windspeed', 'season', 'weathersit']
X_cluster = df[cluster_features]

print(f"聚类特征: {cluster_features}")
print(f"样本数量: {len(X_cluster)}")

# ========== 3. 肘部法则确定最佳K值 ==========
inertias = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_cluster)
    inertias.append(kmeans.inertia_)

# 绘制肘部图
plt.figure(figsize=(8, 5))
plt.plot(K_range, inertias, 'bo-', linewidth=2)
plt.xlabel('聚类数 K')
plt.ylabel('误差平方和 (Inertia)')
plt.xticks(K_range)
plt.grid(True, alpha=0.3)
plt.savefig('图4-2_肘部法则.png', dpi=150)  # 覆盖原文件
plt.show()

print("\n肘部图已保存: 图4-2_肘部法则.png")
print("建议K=3或K=4，本实验选取K=3")

# ========== 4. 执行K-Means聚类（K=3） ==========
k = 3
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X_cluster)

print(f"\n各簇样本数量:")
print(df['cluster'].value_counts().sort_index())

# ========== 5. 分析各簇特征 ==========
print("\n" + "=" * 60)
print("各簇环境特征均值")
print("=" * 60)

cluster_summary = df.groupby('cluster')[cluster_features].mean()
print(cluster_summary.round(4))

# ========== 6. 分析各簇租用量差异 ==========
print("\n" + "=" * 60)
print("各簇租用量统计")
print("=" * 60)

cnt_by_cluster = df.groupby('cluster')['cnt'].agg(['mean', 'median', 'std', 'count'])
print(cnt_by_cluster.round(2))

# ========== 7. 聚类结果可视化 ==========
# 图4-3 各簇租用量箱线图
plt.figure(figsize=(8, 5))
box_data = [df[df['cluster'] == i]['cnt'].values for i in range(k)]
plt.boxplot(box_data, tick_labels=[f'簇{i}' for i in range(k)])
plt.xlabel('聚类簇')
plt.ylabel('租用量 (cnt)')
plt.grid(True, alpha=0.3)
plt.savefig('图4-3_各簇租用量箱线图.png', dpi=150)  # 覆盖原文件
plt.show()

# 图4-4 聚类散点图（温度 vs 租用量）
plt.figure(figsize=(10, 6))
colors = ['red', 'green', 'blue']
for i in range(k):
    cluster_data = df[df['cluster'] == i]
    plt.scatter(cluster_data['temp'], cluster_data['cnt'],
                c=colors[i], label=f'簇{i}', alpha=0.6, s=30)
plt.xlabel('标准化温度')
plt.ylabel('租用量 (cnt)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('图4-4_聚类散点图.png', dpi=150)  # 覆盖原文件
plt.show()

# ========== 8. 结果解读 ==========
print("\n" + "=" * 60)
print("聚类结果解读")
print("=" * 60)

for i in range(k):
    cluster_cnt_mean = df[df['cluster'] == i]['cnt'].mean()
    cluster_temp_mean = df[df['cluster'] == i]['temp'].mean()
    cluster_hum_mean = df[df['cluster'] == i]['hum'].mean()
    cluster_season_mean = df[df['cluster'] == i]['season'].mean()

    print(
        f"\n簇{i}: 平均租用量={cluster_cnt_mean:.0f}, 平均温度={cluster_temp_mean:.3f}, 平均湿度={cluster_hum_mean:.3f}, 平均季节={cluster_season_mean:.1f}")

    if cluster_temp_mean > 0.6:
        print(f"  → 特征: 高温簇（夏季为主），租用量较高")
    elif cluster_temp_mean > 0.5:
        print(f"  → 特征: 中高温簇，租用量中等偏高")
    elif cluster_temp_mean < 0.3:
        print(f"  → 特征: 低温簇（冬季为主），租用量较低")
    else:
        print(f"  → 特征: 中温簇（春秋季为主），租用量中等")

print("\n" + "=" * 60)
print("分析完成！")
print("生成图片: 图4-2_肘部法则.png, 图4-3_各簇租用量箱线图.png, 图4-4_聚类散点图.png")
print("=" * 60)