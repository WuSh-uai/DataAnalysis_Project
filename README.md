 项目一：校园消费数据平台 (campus_consumption)

```markdown
 校园消费数据展示与分析平台

基于 Django + Streamlit 构建的校园消费数据管理与可视化系统。本项目为数据可视化课程实验，旨在通过Web应用和交互式仪表板，直观展示和分析学生的校园消费行为。

 功能特点

   数据管理后台：基于 Django Admin 构建，提供完整的消费记录增删改查（CRUD）功能。
   用户认证系统：安全的登录/登出机制，保护数据平台。
   数据筛选与分页：在消费列表页，可按“消费地点”和“消费类型”进行筛选，并支持数据分页浏览。
   交互式可视化大屏：集成 Streamlit，提供三个核心分析模块：
       消费类型分析：使用 Matplotlib 展示不同消费类型的金额占比。
       消费趋势分析：使用 Plotly 绘制交互式折线图，展示每日消费金额变化，并支持缩放查看。
       地点-金额关联分析：使用 Altair 绘制散点图，分析不同消费地点的消费次数与金额关系。
   响应式UI设计：前端采用 Bootstrap 5 框架，界面美观且适配移动设备。

 技术栈

   后端：Django 5.2, SQLite3
   前端：Bootstrap 5, Font Awesome 6
   可视化：Streamlit, Pandas, Matplotlib, Plotly, Altair

 快速开始

 环境准备
确保已安装 Python 3.8 或更高版本。

 安装与运行

1.  克隆项目
    ```bash
    git clone <你的仓库地址>
    cd campus_consumption
    ```

2.  安装依赖
    ```bash
    pip install -r requirements.txt
    ```

3.  数据库迁移
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  创建管理员用户 (用于登录后台)
    ```bash
    python manage.py createsuperuser
    ```

5.  运行Django开发服务器
    ```bash
    python manage.py runserver
    ```
    访问 `http://127.0.0.1:8000` 即可进入平台登录页。默认管理员账号为 `admin`，密码为 `123456`（或你创建时设置的密码）。

6.  运行Streamlit可视化面板
    在另一个终端中，进入项目根目录并运行：
    ```bash
    streamlit run dashboard.py
    ```
    访问 `http://localhost:8501` 即可查看交互式数据看板。

 项目结构

```
campus_consumption/
├── campus_consumption/       Django 项目配置
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── consumption/              核心应用
│   ├── migrations/
│   ├── templates/            HTML模板文件
│   ├── admin.py              后台管理配置
│   ├── models.py             消费数据模型
│   ├── views.py              视图逻辑
│   └── urls.py               应用路由
├── dashboard.py              Streamlit 可视化主程序
├── manage.py                 Django 管理脚本
└── db.sqlite3                SQLite 数据库文件
```

 主要数据模型

Consumption (消费记录)
   `student_id`: 学号
   `name`: 姓名
   `consumption_type`: 消费类型 (餐饮/文具/饮品/其他)
   `amount`: 消费金额
   `consumption_time`: 消费日期
   `location`: 消费地点 (一食堂/二食堂/校园超市/奶茶店)
作者 WuSh-uai

 许可证

本项目仅供学习交流使用。
```

---

 项目二：共享单车租用量预测 (BikeSharing)

```markdown
 共享单车租用量预测与分析

基于 UCI Bike Sharing Dataset 的完整数据科学项目。项目包含从数据探索（EDA）、可视化分析到机器学习建模（线性回归、决策树、随机森林）以及无监督聚类（K-Means）的全流程。

 项目目标

   深入探索影响共享单车租用量的关键因素（季节、天气、温度等）。
   构建并比较多种回归模型，预测每日的单车租用量。
   使用聚类算法对不同的环境模式进行划分，发现高需求与低需求场景。

 核心功能

 探索性数据分析 (EDA)
   目标变量分析：租用量的分布直方图与箱线图。
   时间序列分析：2011-2012年租用量变化趋势。
   环境因素分析：
       不同季节、天气状况下的租用量箱线图。
       温度与租用量的散点图。
       所有特征的相关性热力图。
   运行 `Data_Analysis.py` 即可生成全部6张可视化图表。

 机器学习建模
   模型：线性回归、决策树回归、随机森林回归。
   评估指标：均方误差（MSE）、均方根误差（RMSE）、决定系数（R²）。
   结果：随机森林模型表现最优，R² 评分最高。
   运行 `Model_Training.py` 完成模型训练、评估，并保存预测对比图。

 无监督聚类分析 (K-Means)
   基于温度、湿度、风速、季节、天气等环境特征进行聚类。
   使用肘部法则确定最佳聚类数（K=3）。
   分析不同簇的环境特征和租用量差异。
   运行 `K-Means.py` 生成肘部图、各簇租用量箱线图及聚类散点图。

 技术栈

   语言：Python 3.8+
   数据处理：Pandas, NumPy
   可视化：Matplotlib, Seaborn
   机器学习：Scikit-learn (LinearRegression, DecisionTreeRegressor, RandomForestRegressor, KMeans)

 快速开始

1.  克隆项目
    ```bash
    git clone <你的仓库地址>
    cd BikeSharing
    ```

2.  安装依赖
    ```bash
    pip install pandas numpy matplotlib seaborn scikit-learn
    ```

3.  运行数据分析 (EDA)
    ```bash
    python Data_Analysis.py
    ```
    将在当前目录生成 `图2-1` 至 `图2-6` 的所有分析图表。

4.  运行聚类分析
    ```bash
    python K-Means.py
    ```
    生成 `图4-2` 至 `图4-4` 的聚类结果图表，并在控制台输出各簇的分析信息。

5.  运行模型训练
    ```bash
    python Model_Training.py
    ```
    完成模型训练与评估，输出各模型的性能指标（MSE, RMSE, R²），并生成预测值与真实值的对比散点图。

 项目文件说明

   `day.csv` / `hour.csv`: UCI 原始数据集。
   `day_processed.csv`: 经过预处理（如添加季节/天气名称）后的日数据，供后续分析使用。
   `Data_Analysis.py`: 完整的 EDA 脚本。
   `Model_Training.py`: 机器学习模型训练、评估与对比脚本。
   `K-Means.py`: K-Means 聚类分析脚本。
   `model_results.csv`: 存储各模型性能指标的表格。
   `图2-.png` 至 `图4-.png`: 分析过程中生成的全部可视化图表。

 关键结论

   温度是影响租用量的最重要因素之一，与租用量呈正相关。
   季节影响显著，秋季租用量最高，春季最低。
   在回归模型中，随机森林的预测效果最佳（R² ≈ 0.8+）。
   通过K-Means聚类，可以将环境模式分为高温高需求、中温中需求和低温低需求三类典型场景。

作者 WuSh-uai
本项目仅供学习交流使用。
