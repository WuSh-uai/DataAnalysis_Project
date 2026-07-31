import requests
from lxml import etree
import re

def fetch_html():
    my_url = "https://movie.douban.com/review/best/"
    my_headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "cookie": "_vwo_uuid_v2=D4C78AB6BB009A4A61787F394FCE5566E|5289f68eb2f6d2d9d58d6436ae11a739; ll=\"118201\"; bid=woVmuAScB3E; _pk_id.100001.4cf6=d8a968a04fcec4c4.1757405350.; __yadk_uid=dGNpZLeA1x78Vj14yfJxbFNAeL0UfYob; _vwo_uuid_v2=D4C78AB6BB009A4A61787F394FCE5566E|5289f68eb2f6d2d9d58d6436ae11a739; __utmc=30149280; __utmc=223695111; ap_v=0,6.0; __utma=30149280.1955326356.1696081963.1758009381.1758014828.12; __utmz=30149280.1758014828.12.5.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=30149280.1.10.1758014828; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1758014831%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=1; __utma=223695111.2089930094.1696081963.1758009383.1758014831.8; __utmz=223695111.1758014831.8.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmb=223695111.2.10.1758014831",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://movie.douban.com/",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Microsoft Edge\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
    }
    # my_proxies = {
    #     "https": "https://222.184.183.244:23515"
    # }
    response = requests.get(my_url, headers=my_headers)
    xpath_data = etree.HTML(response.text)
    target_range = xpath_data.xpath("//div[@data-cid]")
    for target_data in target_range:
        comment_title = target_data.xpath(".//h2/a/text()")[0]
        rid = target_data.xpath("./div[@class='main review-item']/@id")[0]
        target_url = f'https://movie.douban.com/j/review/{rid}/full'
        rp_redirect = requests.get(target_url, headers=my_headers)
        body = rp_redirect.json()["body"]
        body_page = etree.HTML(body)
        comment_content = body_page.xpath("//div[@class='review-content clearfix']//text()")
        comment_content = re.sub(r'\s', '',"".join(comment_content))
        print(f"\t{comment_title}\n{comment_content}\n")

def main():
    fetch_html()

if __name__ == '__main__':
    main()