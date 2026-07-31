import  requests
from lxml import etree

def get_html():
    my_url = "http://www.boxofficecn.com/boxoffice2025"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "connection": "keep-alive",
        "cookie": "__51cke__=; Hm_lvt_b6d45668276623ae0dd56fcf7dad2ead=1758195994; HMACCOUNT=90BA370063337630; __tins__4287866=%7B%22sid%22%3A%201758195994456%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201758197823143%7D; __51laig__=3; Hm_lpvt_b6d45668276623ae0dd56fcf7dad2ead=1758196023",
        "host": "www.boxofficecn.com",
        "pragma": "no-cache",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
    }
    response = requests.get(my_url, headers=headers)
    target_html = response.text
    return target_html

def parse_html(target_html):
    page = etree.HTML(target_html)
    target_range = page.xpath("//div[@class='entry-content']/table/tbody/tr")[1:]
    return target_range

def fetch_data(parser_data):
    # movies =[]
    for target_data in parser_data:
        rank = target_data.xpath(".//td[1]/text()")
        year = target_data.xpath(".//td[2]/text()")
        name = target_data.xpath(".//td[3]/text()")
        money = target_data.xpath(".//td[4]/text()")
        if rank or year or name or money:
            print(rank[0],year[0],name[0],money[0])
        else:
            print("")
            continue
    #     if rank and year and name and money and money[0] != '--' and rank and year and name and money and money[0] !=  None:
    #         movies.append((rank, year, name, money))
    # return movies


def main():
    url = get_html()
    parser_data = parse_html(url)
    data = fetch_data(parser_data)
    print(data)


if __name__ == "__main__":
    main()