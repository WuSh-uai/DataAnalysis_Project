from lxml import etree
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import html5lib
import json

def parse_html_xpath(processed_html):
    title = processed_html.xpath('//div[@id="second-title"]//text()')[0]
    date = processed_html.xpath('//span[@class="date"]/text()')[0]
    origin = processed_html.xpath('//span[@class="publish source"]/text()')[0]
    content = processed_html.xpath('//div[@class="article"]/p//text()')[1:]
    data = {"标题": title, "日期": date, "来源": origin, "内容": content}
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("已存储为json文件")

def parse_html_html5lib(processed_html):
    for elem in processed_html.iter():
        elem.tag = elem.tag.split('}', 1)[-1]
    title = next(e.text for e in processed_html.iter('div') if e.get('id') == 'second-title')
    date = next(e.text for e in processed_html.iter('span') if e.get('class') and 'date' in e.get('class'))
    origin = next(e.text for e in processed_html.iter('span') if e.get('class') and 'publish source' == e.get('class'))
    content = [e.text for e in processed_html.iter('p')][1:]
    data = {"标题": title, "日期": date, "来源": origin, "内容": content}
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parse_html_bs4(processed_html):
    title = processed_html.select_one('#second-title').get_text(strip=True)
    date = processed_html.select_one('.date').get_text(strip=True)
    origin = processed_html.select_one('.publish.source').get_text(strip=True)
    content = [p.get_text(strip=True) for p in processed_html.select('.article p')][1:]
    data = {"标题": title, "日期": date, "来源": origin, "内容": content}
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parse_html_PyQuery(processed_html):
    title = processed_html('#second-title').text()
    date = processed_html('.date').text()
    origin = processed_html('.publish.source').text()
    content = [pq(p).text() for p in processed_html('.article p')][1:]
    data = {"标题": title, "日期": date, "来源": origin, "内容": content}
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    with open('Class_html_report3.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    process_html = etree.HTML(html_content)
    parse_html_xpath(process_html)

    # parse_html_html5lib(html5lib.parse(html_content))

    # parse_html_bs4(BeautifulSoup(html_content, 'lxml'))

    # parse_html_PyQuery(pq(html_content))

if __name__ == '__main__':
    main()