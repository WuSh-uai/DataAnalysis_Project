import urllib.parse
from bs4 import BeautifulSoup
import requests
import os
import traceback
import pymysql

'''
index_url = 'https://search.dangdang.com/advsearch ' 方法：get
detail_url = 'https://search.dangdang.com/?medium=01&key3=%C7%E5%BB%AA%B4%F3%D1%A7%B3%F6%B0%E6%C9%E7&category_path=01.00.00.00.00.00 '
'''

index_url = 'https://search.dangdang.com/advsearch '

search_params = {
    "medium": "01",
    "key3": "清华大学出版社",
    "category_path": "01.00.00.00.00.00"
}

session = requests.session()
session_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
}



def read_list(txt_path):
    press_list = []
    f = open(txt_path,'r',encoding='utf-8')
    for line in f.readlines():
        press_list.append(line.strip('\n'))
    return press_list



def create_form(press_name):
    resp = session.get(index_url, headers=session_headers)
    resp.encoding = resp.apparent_encoding
    print("Response status code:", resp.status_code)
    soup_html = BeautifulSoup(resp.text, 'html.parser')
    input_tag_name = ''
    conditions = soup_html.select('.box.box2.clearfix > .detail_condition > label')
    print('共找到%d项基本条件,正在寻找<input>标签' % len(conditions))
    for item in conditions:
        text = item.select('span')[0].string
        if text == '出版社':
            input_tag_name = item.select('input')[0].get('name')
            print('已找到<input>标签,name:',input_tag_name)
    keyword = {
        'medium' : '01',
        input_tag_name : press_name.encode('gb2312'),
        'category_path' : '01.00.00.00.00.00',
        'sort_type' : 'sort_score_desc'
    }
    url = 'https://search.dangdang.com/? '
    url += urllib.parse.urlencode(keyword)
    print('入口地址:%s' % url)
    return url



def get_info(entry_url):
    res = requests.get(entry_url, headers=session_headers)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'html.parser')
    # 获取页数
    page_num = int(soup.select('.data > span')[1].text.strip('/'))
    print('共 %d 页待抓取' % page_num)
    page_num = 5
    page_now = '$page_index='
    # 书名 价格 出版日期 评论数量
    books_title = []
    books_price = []
    books_date = []
    books_comment = []
    for i in range(1, page_num + 1):
        now_url = entry_url + page_now + str(i)
        print('正在获取第 %d 页, URL: %s' % (i, now_url))
        res = requests.get(now_url, headers=session_headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        # 获取书名
        tmp_books_title = soup.select('ul.bigimg > li[ddt-pit] > a')
        for book in tmp_books_title:
            books_title.append(book.get('title'))
        # 获取价格
        tmp_books_price = soup.select('ul.bigimg > li[ddt-pit] > p.price > span.search_now_price')
        for book in tmp_books_price:
            books_price.append(book.text)
        # 获取评论数量
        tmp_books_comment = soup.select('ul.bigimg > li[ddt-pit] > p.search_star_line > a')
        for book in tmp_books_comment:
            books_comment.append(book.text)
        # 获取出版日期
        tmp_books_date = soup.select('ul.bigimg > li[ddt-pit] > p.search_book_author > span')
        for book in tmp_books_date[1::3]:
            books_date.append(book.text[2:])
    print(f"Title count: {len(books_title)}, Price count: {len(books_price)}, Date count: {len(books_date)}, Comment count: {len(books_comment)}")
    books_dict = {'title': books_title, 'price': books_price, 'date': books_date, 'comment': books_comment}
    return books_dict


def save_info_to_db(db_config, press_name, books_dict):
    try:
        # 连接数据库
        connection = pymysql.connect(host=db_config['host'],
                                     user=db_config['user'],
                                     password=db_config['passwd'],
                                     database=db_config['db'],
                                     port=db_config['port'],
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            for i in range(min(len(books_dict['title']), len(books_dict['price']), len(books_dict['date']), len(books_dict['comment']))):
                # 插入数据
                sql = """
                INSERT INTO `dangd` (`number`, `title`, `price`, `date`, `comments`)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (i + 1, books_dict['title'][i], books_dict['price'][i], books_dict['date'][i],
                                     books_dict['comment'][i]))

            # 提交事务
            connection.commit()
    except Exception as e:
        print('保存到数据库出错')
        print(e)
        traceback.print_exc()
    finally:
        # 关闭数据库连接
        connection.close()


# 入口
def start_spider(press_path, saved_file_dir, db_config):
    # 获取出版社列表
    press_list = read_list(press_path)
    for press_name in press_list:
        print('-------- 开始抓取 %s --------' % press_name)
        press_page_url = create_form(press_name)
        books_dict = get_info(press_page_url)
        save_info_to_db(db_config, press_name, books_dict)
        print('-------- 出版社: %s 抓取完毕 --------' % press_name)
    return


def main():
    # 出版社名列表示所在文件路径
    press_txt_path = r'E:\PythonFiles\Spider\press.txt'
    # 抓取信息保存路径
    saved_file_dir = r'E:\PythonFiles\Spider'
    # 数据库配置
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'passwd': 'root',
        'db': 'dangdang',
        'port': 3306
    }
    # 启动
    start_spider(press_txt_path, saved_file_dir, db_config)


if __name__ == '__main__':
    main()