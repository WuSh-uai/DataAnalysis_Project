from curl_cffi import requests
from lxml import etree
from urllib.parse import urljoin
import re
import json
import pymysql


class XinHuaCrawler:

    def __init__(self):
        self.session = requests.Session(impersonate="chrome120")
        self.index_url = 'https://education.news.cn/jsxw/index.htm'
        self.home_url = 'https://education.news.cn/'
        self.all_detail_url = 'https://education.news.cn/jsxw/ds_77e3127797e049bb8005edd395856264.json'
        self.referer_url = 'https://education.news.cn/jsxw/index.htm'
        # self.seen = set()   #v1.0:准备一个集合容器，为去掉重复具体页面网址做准备
        self.seen = {}        #v2.0:改为字典，之后的具体页面内容即使重复也直接用最新的内容覆盖更新
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'passwd': 'root',
            'db': 'xinhua',
            'port': 3306
        }
        self.conn = pymysql.connect(**self.config)
        self.cursor = self.conn.cursor()



    def get_index_html(self):
        try:
            self.html = self.session.get(self.all_detail_url)
            status_code = self.html.status_code
            if status_code == 200:
                print('请求成功！状态码为：200！')
            else:
                print(f"发送请求异常！状态码为{status_code}")
        except Exception as e:
            print(f"获取索引页面的html时异常终止！错误信息为：\n{e}")
        return self.html



    @staticmethod
    def parse_index_html(unprocessed_index_html):
        try:
            data = json.loads(unprocessed_index_html)
            for item in data.get('datasource', []):
                detail_url = item.get('publishUrl')
                if detail_url:
                    yield detail_url
        except Exception as e:
            print(f"解析索引页面时异常终止！错误信息为：\n{e}")

    def combine_urls(self, detail_url):
        return urljoin(self.home_url, detail_url)



    def get_target_html(self, real_url):
        try:
            real_html = self.session.get(real_url, headers={'Referer': self.referer_url})
            status_code = real_html.status_code
            if status_code == 200:
                print('详情页面请求成功！状态码为：200！')
                return real_html.text
            else:
                print(f"发送请求异常！状态码为{status_code}")
        except Exception as e:
            print(f"获取详细页面时异常终止！错误信息为：\n{e}")



    def parse_target_html(self, unprocessed_target_html):
        try:
            detail_html = etree.HTML(unprocessed_target_html)
            title = self.clean(detail_html.xpath('//div[@class="mheader domMobile"]//span[@class="title"]/text()'))
            if not title:
                print('未提取到标题')
                return
            date = self.clean(detail_html.xpath('//div[@class="info"]/text()'))
            source = self.clean(detail_html.xpath('//div[@class="info"]/span/text()'))
            chaos_content = detail_html.xpath('//div[@class="main-left left"]/div[@id="detail"]/span[@id="detailContent"]//text()')
            process_content = ''.join(chaos_content)
            clean_content = re.sub(r'[\u2002\u2003\u00A0\u202F\u205F\u3000]+', ' ', process_content.strip())
            self.seen[title] = {
                'title': title,
                'date': date,
                'source': source,
                'content': clean_content
            }
            self.seen[title] = {'title': title, 'date': date, 'source': source, 'content': clean_content}
        except Exception as e:
            print(f'解析异常：{e}')

    @staticmethod
    def clean(lst):
        return lst[0].strip() if lst else None



    def save_data(self):
        try:
            for v in self.seen.values():
                self.cursor.execute(
                    "INSERT INTO xinhua_news(标题,日期,来源,内容) VALUES (%s,%s,%s,%s) "
                    "ON DUPLICATE KEY UPDATE 日期=VALUES(日期),来源=VALUES(来源),内容=VALUES(内容)",
                    (v['title'], v['date'], v['source'], v['content'])
                )
            self.conn.commit()
        except Exception as e:
            print(f"数据入库时发生异常！\n{e}")



    def run(self):
        try:
            index_html = self.get_index_html()
            for url in self.parse_index_html(index_html.text):
                combine_url = self.combine_urls(url)
                html_text = self.get_target_html(combine_url)
                self.parse_target_html(html_text)
            self.save_data()
        except Exception as e:
            print(f"运行程序异常终止！错误信息为：\n{e}")
        finally:
            self.cursor.close()
            self.conn.close()
            self.session.close()


if __name__ == "__main__":
    XinHuaCrawler().run()
