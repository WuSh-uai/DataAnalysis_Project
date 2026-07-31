新华网教育频道新闻爬虫

> 基于 Python 的新华网教育新闻数据采集工具，支持自动抓取、解析和存储新闻内容。

📌 项目简介

本项目是一个针对**新华网教育频道**（`education.news.cn`）的新闻爬虫系统。通过模拟浏览器请求，自动获取新闻列表和详情页内容，并持久化存储到 MySQL 数据库中。

核心功能
- 自动获取新闻列表页的所有详情链接
- 模拟真实浏览器请求（`curl_cffi` 指纹伪装）
- 解析新闻标题、发布日期、来源和正文内容
- 数据去重更新（重复数据自动覆盖）
- 数据持久化存储至 MySQL

 🛠 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.10+ | 开发语言 |
| curl_cffi | 模拟浏览器指纹（绕过反爬） |
| lxml | HTML 解析（XPath 提取数据） |
| PyMySQL | MySQL 数据库操作 |
| re | 正文内容清洗 |

📁 项目结构

```
Spider_XinHua/
├── Xinhua_Spider.py      # 爬虫主程序
├── README.md             # 项目说明文档
└── requirements.txt      # 项目依赖（需自行创建）
```

🚀 快速开始

1. 克隆项目

```bash
git clone https://github.com/WuSh-ua/Spider_XinHua.git
cd Spider_XinHua
```

2. 安装依赖

```bash
pip install curl_cffi lxml pymysql
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

3. 配置数据库

在本地 MySQL 中创建数据库和表：

```sql
CREATE DATABASE xinhua DEFAULT CHARACTER SET utf8mb4;

USE xinhua;

CREATE TABLE xinhua_news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    标题 VARCHAR(255) UNIQUE,
    日期 VARCHAR(50),
    来源 VARCHAR(100),
    内容 TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

4. 修改数据库配置

打开 `Xinhua_Spider.py`，修改 `__init__` 方法中的数据库连接信息：

```python
self.config = {
    'host': 'localhost',      # 数据库地址
    'user': 'root',           # 用户名
    'passwd': 'root',         # 密码
    'db': 'xinhua',           # 数据库名
    'port': 3306              # 端口
}
```

5. 运行爬虫

```bash
python Xinhua_Spider.py
```

📊 数据字段说明

| 字段 | 说明 |
|------|------|
| 标题 | 新闻标题（作为唯一键，重复自动更新） |
| 日期 | 新闻发布日期 |
| 来源 | 新闻来源（如“新华网”） |
| 内容 | 清洗后的正文内容（去除特殊空白字符） |

⚙️ 核心逻辑说明

请求伪装
使用 `curl_cffi` 库模拟 `Chrome 120` 浏览器指纹，有效绕过部分反爬机制。

数据去重
采用 `字典` 结构存储数据，以**标题**为键，最新抓取的内容会自动覆盖旧数据，避免重复入库。

内容清洗
使用正则表达式 `re.sub(r'[\u2002\u2003\u00A0\u202F\u205F\u3000]+', ' ', content)` 去除正文中的各类特殊空白字符。

数据库 Upsert
使用 `INSERT ... ON DUPLICATE KEY UPDATE` 语法，当标题重复时自动更新日期、来源和内容，不产生冗余数据。

📝 版本迭代记录

| 版本 | 更新内容 |
|------|----------|
| v1.0 | 基础爬虫框架，使用 `set` 去重详情页 URL |
| v2.0 | 改用 `dict` 存储数据，支持内容覆盖更新 |

⚠️ 注意事项

1. **合规使用**：本爬虫仅用于学习和研究目的，请遵守新华网 `robots.txt` 规定，合理控制请求频率。
2. **反爬升级**：如遇反爬策略升级，可能需要调整 `impersonate` 参数或增加代理轮换。
3. **数据库编码**：建议使用 `utf8mb4` 编码，避免特殊字符（如 Emoji）入库报错。

🤝 贡献

欢迎提交 Issue 或 Pull Request，共同完善本项目。

📄 License

本项目仅供学习交流使用，请勿用于商业用途。

---

作者：WuSh  
GitHub：[WuSh-ua](https://github.com/WuSh-ua)
