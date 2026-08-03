"""
共享单车租用量预测 - 探索性数据分析（EDA）
数据集：UCI Bike Sharing Dataset (day.csv)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文显示（解决matplotlib中文乱码）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ========== 1. 加载数据 ==========
print("=" * 50)
print("1. 加载数据")
print("=" * 50)

df = pd.read_csv('day.csv')
print(f"数据集形状: {df.shape}")
print(f"\n前5行数据:")
print(df.head())
print(f"\n数据类型:")
print(df.dtypes)
print(f"\n缺失值统计:")
print(df.isnull().sum())

# ========== 2. 数据基本信息 ==========
print("\n" + "=" * 50)
print("2. 数据统计描述")
print("=" * 50)
print(df.describe())

# ========== 3. 目标变量分布图 ==========
print("\n" + "=" * 50)
print("3. 生成图2-1: 目标变量分布直方图")
print("=" * 50)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 直方图
axes[0].hist(df['cnt'], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_xlabel('租用量 (cnt)')
axes[0].set_ylabel('频数')
# axes[0].set_title('图2-1(a) 租用量分布直方图')  # 已注释
axes[0].axvline(df['cnt'].mean(), color='red', linestyle='--', label=f'均值: {df["cnt"].mean():.0f}')
axes[0].axvline(df['cnt'].median(), color='green', linestyle='--', label=f'中位数: {df["cnt"].median():.0f}')
axes[0].legend()

# 箱线图
axes[1].boxplot(df['cnt'], vert=True)
axes[1].set_ylabel('租用量 (cnt)')
# axes[1].set_title('图2-1(b) 租用量箱线图')  # 已注释

plt.tight_layout()
plt.savefig('图2-1_目标变量分布.png', dpi=150, bbox_inches='tight')
plt.show()

# ========== 4. 租用量随时间变化 ==========
print("\n" + "=" * 50)
print("4. 生成图2-2: 租用量随时间变化")
print("=" * 50)

# 转换日期格式
df['dteday'] = pd.to_datetime(df['dteday'])

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(df['dteday'], df['cnt'], linewidth=0.8, color='steelblue', alpha=0.7)
ax.set_xlabel('日期')
ax.set_ylabel('租用量 (cnt)')
# ax.set_title('图2-2 共享单车租用量随时间变化趋势 (2011-2012)')  # 已注释
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('图2-2_租用量时间序列.png', dpi=150, bbox_inches='tight')
plt.show()

# ========== 5. 季节对租用量的影响 ==========
print("\n" + "=" * 50)
print("5. 生成图2-3: 季节箱线图")
print("=" * 50)

season_map = {1: '春季', 2: '夏季', 3: '秋季', 4: '冬季'}
df['season_name'] = df['season'].map(season_map)

fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x='season_name', y='cnt', data=df, order=['春季', '夏季', '秋季', '冬季'], palette='Set2')
ax.set_xlabel('季节')
ax.set_ylabel('租用量 (cnt)')
# ax.set_title('图2-3 不同季节的租用量分布')  # 已注释
plt.tight_layout()
plt.savefig('图2-3_季节箱线图.png', dpi=150, bbox_inches='tight')
plt.show()

# 打印季节统计
print("\n各季节租用量统计:")
print(df.groupby('season_name')['cnt'].agg(['mean', 'median', 'std']))

# ========== 6. 天气对租用量的影响 ==========
print("\n" + "=" * 50)
print("6. 生成图2-4: 天气箱线图")
print("=" * 50)

weather_map = {1: '晴朗/多云', 2: '雾天/阴天', 3: '小雪/小雨', 4: '大雨/大雪'}
df['weather_name'] = df['weathersit'].map(weather_map)

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x='weather_name', y='cnt', data=df, palette='Set3')
ax.set_xlabel('天气状况')
ax.set_ylabel('租用量 (cnt)')
# ax.set_title('图2-4 不同天气状况下的租用量分布')  # 已注释
plt.tight_layout()
plt.savefig('图2-4_天气箱线图.png', dpi=150, bbox_inches='tight')
plt.show()

# 打印天气统计
print("\n各天气状况租用量统计:")
print(df.groupby('weather_name')['cnt'].agg(['mean', 'median', 'std']))

# ========== 7. 温度与租用量关系 ==========
print("\n" + "=" * 50)
print("7. 生成图2-5: 温度与租用量散点图")
print("=" * 50)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 原始温度（已标准化）
axes[0].scatter(df['temp'], df['cnt'], alpha=0.5, color='steelblue')
axes[0].set_xlabel('标准化温度 (temp)')
axes[0].set_ylabel('租用量 (cnt)')
# axes[0].set_title('图2-5(a) 温度与租用量散点图')  # 已注释

# 体感温度
axes[1].scatter(df['atemp'], df['cnt'], alpha=0.5, color='coral')
axes[1].set_xlabel('体感温度 (atemp)')
axes[1].set_ylabel('租用量 (cnt)')
# axes[1].set_title('图2-5(b) 体感温度与租用量散点图')  # 已注释

plt.tight_layout()
plt.savefig('图2-5_温度散点图.png', dpi=150, bbox_inches='tight')
plt.show()

# 计算相关系数
print("\n温度与租用量的相关系数:")
print(f"temp 与 cnt 的相关系数: {df['temp'].corr(df['cnt']):.4f}")
print(f"atemp 与 cnt 的相关系数: {df['atemp'].corr(df['cnt']):.4f}")

# ========== 8. 特征相关性热力图 ==========
print("\n" + "=" * 50)
print("8. 生成图2-6: 特征相关性热力图")
print("=" * 50)

# 选择数值型特征
numeric_cols = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday',
                'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
corr_matrix = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
            square=True, linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
# ax.set_title('图2-6 特征相关性热力图', fontsize=14)  # 已注释
plt.tight_layout()
plt.savefig('图2-6_相关性热力图.png', dpi=150, bbox_inches='tight')
plt.show()

# ========== 9. 与cnt相关性最高的特征 ==========
print("\n" + "=" * 50)
print("9. 特征相关性排序")
print("=" * 50)

corr_with_cnt = corr_matrix['cnt'].sort_values(ascending=False)
print("各特征与租用量(cnt)的相关系数:")
for feature, corr in corr_with_cnt.items():
    print(f"  {feature}: {corr:.4f}")

# ========== 10. 保存处理后的数据（用于后续建模） ==========
print("\n" + "=" * 50)
print("10. 保存预处理后的数据")
print("=" * 50)

# 删除临时列
df_clean = df.drop(['season_name', 'weather_name'], axis=1)
df_clean.to_csv('day_processed.csv', index=False)
print("已保存预处理后的数据到: day_processed.csv")
print(f"数据形状: {df_clean.shape}")

print("\n" + "=" * 50)
print("EDA完成！共生成6张图表，保存在当前目录。")
print("=" * 50)