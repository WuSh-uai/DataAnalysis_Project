🕷️ 爬虫项目合集

> 个人爬虫学习与实践项目集合，涵盖新闻资讯、电商图书等多源数据采集。

---

 📁 项目列表

| 项目 | 目标网站 | 技术栈 | 核心功能 |
|------|---------|--------|---------|
| [新华网教育新闻爬虫](./Xinhua_Spider/) | education.news.cn | Python, curl_cffi, lxml, PyMySQL | 新闻列表获取 → 详情页解析 → 数据去重入库 |
| [当当网图书爬虫](./Dangdang_Spider/) | search.dangdang.com | Python, requests, BeautifulSoup, PyMySQL | 出版社检索 → 分页抓取 → 图书信息入库 |

---

 📌 项目一：新华网教育新闻爬虫

目标：采集新华网教育频道的新闻标题、日期、来源、正文内容，存入 MySQL。

 核心实现

- 反爬绕过：使用 `curl_cffi` 模拟 Chrome 120 浏览器指纹
- 数据解析：基于 `lxml` 和 XPath 提取结构化数据
- 数据清洗：正则表达式去除正文中的 Unicode 特殊空白符
- 去重更新：字典存储 + `INSERT ... ON DUPLICATE KEY UPDATE` 实现增量更新

 技术栈

`Python 3.10+` | `curl_cffi` | `lxml` | `PyMySQL` | `re`

 快速开始

```bash
cd Xinhua_Spider
pip install curl_cffi lxml pymysql
```

执行前需创建数据库表：

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

修改数据库配置后运行：

```bash
python Xinhua_Spider.py
```

---

 📌 项目二：当当网图书爬虫

目标：根据出版社列表，爬取当当网该出版社的图书信息（书名、价格、出版日期、评论数），存入 MySQL。

 核心实现

- 动态参数构建：解析搜索页 HTML，动态获取 `input` 标签的 `name` 属性，拼接请求参数
- 分页遍历：自动识别总页数，循环爬取每一页数据
- 数据清洗：统一编码处理（GB2312 → UTF-8）
- 批量入库：使用 PyMySQL 批量插入图书数据

 技术栈

`Python 3.10+` | `requests` | `BeautifulSoup` | `PyMySQL` | `urllib.parse`

 快速开始

```bash
cd Dangdang_Spider
pip install requests beautifulsoup4 pymysql
```

准备出版社列表文件 `press.txt`（每行一个出版社名称）：

```
清华大学出版社
北京大学出版社
人民邮电出版社
```

创建数据库表：

```sql
CREATE DATABASE dangdang DEFAULT CHARACTER SET utf8mb4;
USE dangdang;
CREATE TABLE dangd (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number INT,
    title VARCHAR(255),
    price VARCHAR(50),
    date VARCHAR(50),
    comments VARCHAR(50)
);
```

修改 `main()` 中的文件路径和数据库配置后运行：

```bash
python Dangdang_Spider.py
```

---

 🛠️ 技术栈总览

| 类别 | 技术 |
|------|------|
| 语言 | Python 3.10+ |
| 请求库 | requests, curl_cffi |
| 解析库 | lxml, BeautifulSoup |
| 数据库 | MySQL + PyMySQL |
| 编码处理 | urllib.parse, re |
| 调试 | traceback |

---

 📁 目录结构

```
Spider_Project/
├── Xinhua_Spider/
│   ├── Xinhua_Spider.py
│   └── README.md
├── Dangdang_Spider/
│   ├── Dangdang_Spider.py
│   ├── press.txt
│   └── README.md
└── README.md                     总项目说明
```

---

 ⚠️ 注意事项

1. 合规使用：本合集所有爬虫仅供学习研究使用，请遵守各网站的 `robots.txt` 规定
2. 请求频率：请合理控制请求间隔，避免对目标网站造成压力
3. 编码问题：当当网搜索关键词需转为 `gb2312` 编码，注意区分
4. 数据库配置：所有项目均需在代码中修改数据库连接信息

---

 📝 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-07 | 新增新华网教育新闻爬虫（curl_cffi 指纹伪装） |
| v1.1 | 2026-07 | 新增当当网图书爬虫（分页抓取 + 批量入库） |

---

 👤 作者

WuSh · [GitHub](https://github.com/WuSh-uai)

---

 📄 License

本项目仅供学习交流使用，请勿用于商业用途。
