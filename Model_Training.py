# -*- coding: utf-8 -*-
"""
共享单车租用量预测 - 模型训练与评估
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import matplotlib.pyplot as plt

# ========== 1. 加载数据 ==========
df = pd.read_csv('day_processed.csv')

# ========== 2. 特征选择 ==========
# 排除：instant(序号), dteday(日期), casual, registered(预测时未知)
feature_cols = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday',
                'weathersit', 'temp', 'atemp', 'hum', 'windspeed']
X = df[feature_cols]
y = df['cnt']

print(f"特征集: {feature_cols}")
print(f"特征数量: {len(feature_cols)}")
print(f"样本数量: {len(X)}")

# ========== 3. 时间顺序划分 ==========
# 前80%训练，后20%测试
split_idx = int(len(X) * 0.8)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

print(f"\n训练集大小: {len(X_train)} (前80%)")
print(f"测试集大小: {len(X_test)} (后20%)")

# ========== 4. 训练三个模型 ==========
models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(max_depth=5, random_state=42),
    'XGBoost': xgb.XGBRegressor(n_estimators=100, learning_rate=0.1,
                                max_depth=5, random_state=42)
}

results = []

for name, model in models.items():
    print(f"\n{'=' * 40}")
    print(f"训练模型: {name}")
    print('=' * 40)

    # 训练
    model.fit(X_train, y_train)

    # 预测
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # 计算指标
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)

    # 时间序列交叉验证（5折）
    tscv = TimeSeriesSplit(n_splits=5)
    cv_scores = cross_val_score(model, X, y, cv=tscv, scoring='neg_root_mean_squared_error')
    cv_rmse_mean = -cv_scores.mean()
    cv_rmse_std = cv_scores.std()

    results.append({
        '模型': name,
        '训练RMSE': train_rmse,
        '测试RMSE': test_rmse,
        '训练MAE': train_mae,
        '测试MAE': test_mae,
        '训练R²': train_r2,
        '测试R²': test_r2,
        'CV RMSE均值': cv_rmse_mean,
        'CV RMSE标准差': cv_rmse_std
    })

    print(f"训练RMSE: {train_rmse:.2f}")
    print(f"测试RMSE: {test_rmse:.2f}")
    print(f"训练R²: {train_r2:.4f}")
    print(f"测试R²: {test_r2:.4f}")
    print(f"5折CV RMSE: {cv_rmse_mean:.2f} (±{cv_rmse_std:.2f})")

# ========== 5. 结果汇总表 ==========
print("\n" + "=" * 60)
print("模型性能对比汇总")
print("=" * 60)

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

# 保存结果
results_df.to_csv('model_results.csv', index=False)
print("\n结果已保存至: model_results.csv")

# ========== 6. 特征重要性（XGBoost） ==========
xgb_model = models['XGBoost']
importance = pd.DataFrame({
    '特征': feature_cols,
    '重要性': xgb_model.feature_importances_
}).sort_values('重要性', ascending=False)

print("\nXGBoost特征重要性:")
print(importance.to_string(index=False))

# ========== 7. 预测vs真实值散点图 ==========
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for i, (name, model) in enumerate(models.items()):
    y_pred = model.predict(X_test)
    axes[i].scatter(y_test, y_pred, alpha=0.5, s=20)
    axes[i].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=1)
    axes[i].set_xlabel('Actual Count')
    axes[i].set_ylabel('Predicted Count')
    # 移除标题，只显示RMSE值
    rmse_value = np.sqrt(mean_squared_error(y_test, y_pred))
    axes[i].text(0.05, 0.95, f'RMSE={rmse_value:.0f}',
                 transform=axes[i].transAxes, fontsize=10,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('图4-1_预测对比散点图.png', dpi=150, bbox_inches='tight')
plt.show()

# 打印完成信息
print("\n图片已保存至: 图4-1_预测对比散点图.png")